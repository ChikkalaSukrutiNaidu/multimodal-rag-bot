from interfaces.retriever_interface import RetrieverInterface


class VectorRetriever(RetrieverInterface):

    def __init__(self, retriever):
        self.retriever = retriever

    def retrieve(self, query):
        return self.retriever.invoke(query)