from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingSingleton:

    _instance = None

    @staticmethod
    def get_instance():

        if EmbeddingSingleton._instance is None:

            EmbeddingSingleton._instance = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

        return EmbeddingSingleton._instance