from langchain_community.document_loaders import PyPDFLoader

from pdf2image import convert_from_path
import pytesseract

from langchain_core.documents import Document


def load_pdf(pdf_path):

    documents = []

    # ================= NORMAL PDF TEXT =================

    try:

        loader = PyPDFLoader(pdf_path)

        documents = loader.load()

    except:
        pass

    # ================= OCR FOR SCANNED PDF =================

    try:

        images = convert_from_path(pdf_path)

        for i, image in enumerate(images):

            text = pytesseract.image_to_string(image)

            if text.strip():

                documents.append(

                    Document(

                        page_content=text,

                        metadata={
                            "page": i + 1
                        }

                    )

                )

    except:
        pass

    return documents