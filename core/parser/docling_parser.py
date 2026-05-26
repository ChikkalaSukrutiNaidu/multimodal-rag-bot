from docling.document_converter import DocumentConverter


class DoclingParser:

    def __init__(self):
        self.converter = DocumentConverter()

    def parse(self, file_path):

        result = self.converter.convert(file_path)

        return result.document.export_to_markdown()