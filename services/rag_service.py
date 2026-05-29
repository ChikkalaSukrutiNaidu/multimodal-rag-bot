from core.embeddings import create_vectorstore
from core.retriever import get_retriever
from core.generation import generate_answer


def setup_rag(chunks):

    vectorstore = create_vectorstore(chunks)

    retriever = get_retriever(vectorstore)

    return retriever


def ask_question(question, retriever):

    answer, docs = generate_answer(
        question,
        retriever
    )

    return answer, docs