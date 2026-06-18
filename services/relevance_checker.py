from services.llm_service import llm


def is_relevant(question, context):

    response = llm.invoke(
        f"""
Question:
{question}

Context:
{context}

Can the question be answered from the context?

Reply only:

YES

or

NO
"""
    )

    return "YES" in response.content.upper()