from typing import TypedDict


class GraphState(TypedDict):

    question: str

    retriever: object

    history: str

    route: str

    answer: str

    docs: list

    source: str