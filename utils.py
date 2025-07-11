# utils.py
import re
import fitz  # PyMuPDF

def extract_email_from_pdf(pdf_path: str) -> str | None:
    """
    Returns the first email address found in a PDF, or None if not found.
    """
    email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"

    with fitz.open(pdf_path) as doc:
        full_text = ""
        for page in doc:
            full_text += page.get_text()

    match = re.search(email_pattern, full_text)
    return match.group(0) if match else None
