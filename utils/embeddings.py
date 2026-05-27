import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ================= EMBEDDING MODEL =================

def get_embedding_model():

    return HuggingFaceEmbeddings(

        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",

        model_kwargs={
            "device": "cpu"
        },

        encode_kwargs={
            "normalize_embeddings": True
        }
    )


# ================= CREATE VECTORSTORE =================

def create_vectorstore(chunks):

    embeddings = get_embedding_model()

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    os.makedirs("vectorstore", exist_ok=True)

    vectorstore.save_local("vectorstore")

    return vectorstore


# ================= LOAD VECTORSTORE =================

def load_vectorstore():

    embeddings = get_embedding_model()

    vectorstore = FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore