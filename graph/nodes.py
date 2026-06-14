def router_node(state):

    question = state["question"]

    if any(
        word in question.lower()
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

    return {
        "route": "rag"
    }

from services.company_tool import company_tool

def company_node(state):

    print("Company Node Started")

    answer = company_tool(state["question"])

    print("Company Node Finished")

    return {
        "answer": answer
    }

from services.rag_service import ask_question

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