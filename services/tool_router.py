from services.company_tool import company_tool
from services.web_search_tool import get_web_search_tool
from services.rag_service import ask_question

search = get_web_search_tool()

def route_question(question, retriever):

    print("Routing question:", question)

    # ======================
    # 1. MYSQL TOOL CHECK
    # ======================
    if any(word in question.lower() for word in ["ceo", "package", "eligibility", "company"]):
        result = company_tool(question)

        if result:
            return f"Company: {result['company_name']} | CEO: {result['ceo']} | Eligibility: {result['eligibility']} | Package: {result['package']}", "MYSQL"

    # ======================
    # 2. RAG CHECK
    # ======================
    if retriever is not None:
        try:
            answer, docs = ask_question(question, retriever)

            if answer and "not contain" not in answer.lower():
                return answer, "RAG"
        except:
            pass

    # ======================
    # 3. TAVILY WEB SEARCH
    # ======================
    try:
        results = search(question)

        if results:
            top = results[0]
            return top.get("content", "No content found"), "WEB"
    except Exception as e:
        print("Web error:", e)

    return "No information found", "NONE"