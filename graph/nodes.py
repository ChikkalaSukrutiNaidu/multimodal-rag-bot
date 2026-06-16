from services.llm_service import llm
from services.company_tool import company_tool
from services.rag_service import ask_question
from services.web_search_tool import tavily_search
from services.calculator_tool import calculator_tool
from services.date_tool import date_tool


def router_node(state):

    question = state["question"].lower()

    # Company Queries
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

    # Calculator Queries
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

    # Date Queries
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

    # Live / Recent IPL Questions
    if any(
        word in question
        for word in [
            "latest",
            "news",
            "current",
            "recent",
            "2025",
            "2026",
            "winner",
            "won",
            "points table",
            "orange cap",
            "purple cap"
        ]
    ):
        return {"route": "web"}

    # IPL Dataset Questions
    if state["retriever"] is not None:
        return {"route": "rag"}

    # Fallback
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
            "answer": "IPL dataset not loaded.",
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

    question = state["question"]

    web_content = tavily_search(question)

    if not web_content:

        return {
            "answer": "No web results found.",
            "source": "web",
            "docs": []
        }

    summary = llm.invoke(
        f"""
        User Question:
        {question}

        Web Search Result:
        {web_content}

        Give a short direct answer.

        If the content contains rankings,
        points tables or statistics,
        summarize only the important information.

        Do not copy the entire webpage.
        """
    )

    return {
        "answer": summary.content,
        "source": "web",
        "docs": []
    }