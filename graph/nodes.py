from services.company_tool import company_tool
from services.rag_service import ask_question


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
        return {
            "route": "company"
        }

    if any(
        word in question
        for word in [
            "latest",
            "today",
            "news",
            "current"
        ]
    ):
        return {
            "route": "web"
        }

    return {
        "route": "rag"
    }


def company_node(state):

    print("Company Node Started")

    answer = company_tool(
        state["question"]
    )

    print("Company Node Finished")

    return {
        "answer": answer
    }


def rag_node(state):

    question = state["question"]

    retriever = state["retriever"]

    answer, docs = ask_question(
        question,
        retriever
    )

    return {
        "answer": answer
    }


def web_node(state):

    return {
        "answer": "WEB Node Working"
    }