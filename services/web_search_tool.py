from tavily import TavilyClient
import os

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def tavily_search(query):

    try:

        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )

        results = response.get("results", [])

        if not results:
            return None

        content = ""

        for result in results:

            title = result.get("title", "")
            text = result.get("content", "")

            content += f"""
Title: {title}

{text}

-------------------
"""

        return content

    except Exception as e:

        print(e)
        return None