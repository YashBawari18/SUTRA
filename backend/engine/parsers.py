import io
import pandas as pd
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

def parse_pdf(file_bytes: bytes) -> str:
    """Extracts text from PDF."""
    text = ""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text("text") + "\n"
    except Exception as e:
        print(f"PDF parsing error: {e}")
    return text.strip()

def parse_csv(file_bytes: bytes) -> str:
    """Extracts structured text from CSV."""
    text = ""
    try:
        df = pd.read_csv(io.BytesIO(file_bytes))
        # Convert rows to a readable text representation for NLP
        for _, row in df.iterrows():
            text += ", ".join([f"{col}: {val}" for col, val in row.items()]) + "\n"
    except Exception as e:
        print(f"CSV parsing error: {e}")
    return text.strip()

def parse_txt(file_bytes: bytes) -> str:
    """Decodes TXT file."""
    try:
        return file_bytes.decode('utf-8')
    except Exception:
        try:
            return file_bytes.decode('latin-1')
        except Exception as e:
            print(f"TXT parsing error: {e}")
            return ""

def parse_image(file_bytes: bytes) -> str:
    """Extracts text from image using OCR."""
    text = ""
    try:
        img = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(img)
    except Exception as e:
        print(f"Image parsing error: {e}")
    return text.strip()

def parse_document(file_type: str, file_bytes: bytes) -> str:
    """Routes the document to the appropriate parser based on file extension."""
    if file_type == ".pdf":
        return parse_pdf(file_bytes)
    elif file_type == ".csv":
        return parse_csv(file_bytes)
    elif file_type == ".txt":
        return parse_txt(file_bytes)
    elif file_type in [".jpg", ".png"]:
        return parse_image(file_bytes)
    else:
        raise ValueError(f"Unsupported file type for parsing: {file_type}")
