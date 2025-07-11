from flask import Flask, request, render_template
import os, mimetypes, re, fitz  # PyMuPDF for PDF text extraction
from werkzeug.utils import secure_filename
from send_verification_email import send_email  # ✅ IMPORT ADDED

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Helper: extract first email from a PDF file ---
def extract_email_from_pdf(pdf_path: str):
    email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
    with fitz.open(pdf_path) as doc:
        full_text = "".join(page.get_text() for page in doc)
    match = re.search(email_pattern, full_text)
    return match.group(0) if match else None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        sap_id = request.form['sap_id']
        reason = request.form['reason']
        file = request.files['file']

        if not file:
            return "❌ No file uploaded!"

        # Save file securely
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Detect MIME type to know if PDF or image
        mime_type, _ = mimetypes.guess_type(filepath)
        doctor_email = None

        if mime_type == 'application/pdf':
            doctor_email = extract_email_from_pdf(filepath)

        if doctor_email:
            # ✅ Call the email function here
            send_email(
                receiver_email=doctor_email,
                patient_name=name,
                date="17 May 2025",  # You can make this dynamic later
                diagnosis=reason,
                doctor_name="Doctor"  # You can extract real name later
            )

            return (f"✅ Uploaded for {name} ({sap_id}) — Reason: {reason}<br>"
                    f"📬 Verification email sent to: <b>{doctor_email}</b>")
        else:
            return (f"✅ Uploaded for {name} ({sap_id}) — Reason: {reason}<br>"
                    f"⚠️ No doctor email found in the document.")

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
