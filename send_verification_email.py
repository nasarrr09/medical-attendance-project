import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(receiver_email, patient_name, date, diagnosis, doctor_name="Doctor"):
    # Configuration (use environment variables in production)
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    sender_email = "medicalexemption02@gmail.com"
    app_password = "nvnbvkltrhycoovz"

    # Email content
    subject = f"Verification request for prescription dated {date}"
    body = f"""
Dear {doctor_name},

Our attendance-relief platform received a prescription you issued for {patient_name} (dated {date}, diagnosis: {diagnosis}).
Could you kindly confirm its authenticity by replying “Verified” or “Not verified” to this email?

disclaimer: This message and any accompanying documents are intended solely for the use of the addressee and may contain confidential student health information.
If you are not the intended recipient, please delete this email and notify the sender. By replying, you acknowledge that any information provided will be used only to 
verify the authenticity of the attached prescription and for no other purpose, in compliance with applicable privacy laws

Thank you for your time.

Best regards,  
Medical Exemption Team
"""

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        

        
