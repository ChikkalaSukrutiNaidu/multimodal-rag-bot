from services.web_search_tool import web_search

def web_tool(query):

    results = web_search(query)

    if not results:
        return None

    answer = ""

    for result in results:

        title = result.get("title", "")
        body = result.get("body", "")

        answer += f"{title}\n{body}\n\n"

    return answer