import pdfplumber


def extract_pdf_text(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()  # Use empty string if None

    with open("temp/intro_pdf_text.txt", "a") as f:
        f.write(text)

    return text


extract_pdf_text("temp/intro.pdf")
