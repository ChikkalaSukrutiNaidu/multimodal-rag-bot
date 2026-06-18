from services.llm_service import llm
from services.ipl_stats_tool import is_ipl_stats_query
from services.company_tool import company_tool
from services.rag_service import ask_question
from services.web_search_tool import tavily_search
from services.calculator_tool import calculator_tool
from services.date_tool import date_tool
from services.memory import get_history
from services.relevance_checker import is_relevant

def router_node(state):

    question = state["question"].lower()

    reasoning_keywords = [
    "compare",
    "difference",
    "both",
    "highest and",
    "most runs and",
    "most wickets and",
    "top batsman and top bowler",
    "better",
    "average",
    "he",
    "him",
    "his",
    "they",
    "them",
    "that player",
    "that team"
]

    if any(keyword in question for keyword in reasoning_keywords):
        return {"route": "reasoning"}

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

    if is_ipl_stats_query(question):
        return {"route": "ipl_stats"}

    if state["retriever"] is not None:
        return {"route": "rag"}

    return {"route": "web"}


def company_node(state):

    answer = company_tool(state["question"])

    return {
        "answer": answer,
        "source": "database",
        "docs": []
    }


def calculator_node(state):

    answer = calculator_tool(state["question"])

    return {
        "answer": answer,
        "source": "calculator",
        "docs": []
    }


def date_node(state):

    answer = date_tool(state["question"])

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

    docs = retriever.invoke(
        state["question"]
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    if not is_relevant(
        state["question"],
        context
    ):
        return web_node(state)

    answer, docs = ask_question(
        state["question"],
        retriever
    )

    return {
        "answer": answer,
        "source": "pdf_rag",
        "docs": docs
    }


def ipl_stats_node(state):

    retriever = state["retriever"]

    if retriever is None:
        return {
            "answer": "IPL dataset not loaded.",
            "source": "ipl_stats",
            "docs": []
        }

    docs = retriever.invoke(
        state["question"]
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    if not is_relevant(
        state["question"],
        context
    ):
        return web_node(state)

    answer, docs = ask_question(
        state["question"],
        retriever
    )

    return {
        "answer": answer,
        "source": "ipl_stats",
        "docs": docs
    }


def reasoning_node(state):

    retriever = state["retriever"]

    if retriever is None:
        return {
            "answer": "IPL dataset not loaded.",
            "source": "reasoning",
            "docs": []
        }

    docs = retriever.invoke(
        state["question"]
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    # OUT OF CONTEXT CHECK
    if not is_relevant(
        state["question"],
        context
    ):
        return {
            "answer": "This question is outside the IPL dataset.",
            "source": "fallback",
            "docs": []
        }

    history = state.get(
        "history",
        ""
    )

    response = llm.invoke(
        f"""
You are an IPL analytics assistant.

Previous Conversation:
{history}

IPL Context:
{context}

Current Question:
{state['question']}

...
"""
    )

    return {
        "answer": response.content,
        "source": "reasoning",
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

        Web Search Results:
        {web_content}

        Rules:
        - Give only the final answer.
        - Maximum 5 lines.
        - Do not copy website content.
        - Summarize important facts only.
        """
    )

    return {
        "answer": summary.content,
        "source": "web",
        "docs": []
    }