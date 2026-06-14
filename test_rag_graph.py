from langchain_core.documents import Document

from core.embeddings import create_vectorstore
from core.retriever import get_retriever

from graph.workflow import graph

docs = [
    Document(
        page_content="""
Normalization is the process of organizing data
in a database to reduce redundancy.
"""
    )
]

vectorstore = create_vectorstore(docs)

retriever = get_retriever(vectorstore)

result = graph.invoke(
    {
        "question": "What is normalization?",
        "retriever": retriever
    }
)

print(result)