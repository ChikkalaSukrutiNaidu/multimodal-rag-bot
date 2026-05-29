from core.loader import load_pdf
from core.chunking import split_documents


def process_pdf(pdf_path):

    documents = load_pdf(pdf_path)

    chunks = split_documents(documents)

    return chunks