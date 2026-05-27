from langchain_community.document_loaders import PyPDFLoader


def load_pdf(pdf_path):

    loader = PyPDFLoader(
        pdf_path,
        extract_images=False
    )

    documents = loader.load()

    cleaned_docs = []

    for doc in documents:

        text = doc.page_content

        # CLEAN TEXT
        text = text.replace("\n", " ")

        text = " ".join(text.split())

        doc.page_content = text

        cleaned_docs.append(doc)

    return cleaned_docs