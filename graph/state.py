from typing import TypedDict


class GraphState(TypedDict):
    question: str
    retriever: object

    route: str

    answer: str
    source: str
    docs: list