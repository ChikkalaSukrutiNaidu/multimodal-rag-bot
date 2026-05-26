from langchain_community.vectorstores import FAISS
from core.embeddings.embedding_model import EmbeddingSingleton


class VectorStoreManager:

    def create(self, chunks):

        embeddings = EmbeddingSingleton.get_instance()

        return FAISS.from_texts(chunks, embeddings)