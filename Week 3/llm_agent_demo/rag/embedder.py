from sentence_transformers import SentenceTransformer
import fitz  # PyMuPDF

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join([page.get_text() for page in doc])

def embed_text(text):
    return model.encode([text])[0]
