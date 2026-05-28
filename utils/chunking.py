from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(

        chunk_size=2000,
        chunk_overlap=400,

        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_documents(documents)

    return chunks