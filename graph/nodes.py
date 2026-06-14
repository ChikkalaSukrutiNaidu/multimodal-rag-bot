
from services.company_tool import company_tool
from services.rag_service import ask_question
from services.web_search_tool import tavily_search
from services.calculator_tool import calculator_tool
from services.date_tool import date_tool


def router_node(state):

    question = state["question"].lower()

    if any(
        word in question
        for word in [
            "ceo",
            "package",
            "eligibility",
            "company"
        ]
    ):
        return {"route": "company"}

    if any(
        word in question
        for word in [
            "calculate",
            "plus",
            "minus",
            "times",
            "divided",
            "+",
            "-",
            "*",
            "/"
        ]
    ):
        return {"route": "calculator"}

    if any(
        word in question
        for word in [
            "today",
            "date",
            "day",
            "month",
            "year"
        ]
    ):
        return {"route": "date"}

    if any(
        word in question
        for word in [
            "latest",
            "news",
            "current"
        ]
    ):
        return {"route": "web"}

    if state["retriever"] is not None:
        return {"route": "rag"}

    return {"route": "web"}


def company_node(state):

    answer = company_tool(
        state["question"]
    )

    return {
        "answer": answer,
        "source": "database",
        "docs": []
    }


def calculator_node(state):

    answer = calculator_tool(
        state["question"]
    )

    return {
        "answer": answer,
        "source": "calculator",
        "docs": []
    }


def date_node(state):

    answer = date_tool(
        state["question"]
    )

    return {
        "answer": answer,
        "source": "date",
        "docs": []
    }


def rag_node(state):

    retriever = state["retriever"]

    if retriever is None:

        return {
            "answer": "Please upload a PDF first.",
            "source": "pdf_rag",
            "docs": []
        }

    answer, docs = ask_question(
        state["question"],
        retriever
    )

    return {
        "answer": answer,
        "source": "pdf_rag",
        "docs": docs
    }


def web_node(state):

    answer = tavily_search(
        state["question"]
    )

    return {
        "answer": answer,
        "source": "web",
        "docs": []
    }