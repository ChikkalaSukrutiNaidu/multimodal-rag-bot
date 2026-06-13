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

from services.company_tool import company_tool

def company_node(state):

    print("Company Node Called")

    return {
        "answer": "Company Tool Reached"
    }


def rag_node(state):

    return {
        "answer": "RAG Node Working"
    }