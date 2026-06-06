from tavily import TavilyClient
import os

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def tavily_search(query):

    try:

        response = client.search(
            query=query,
            max_results=1
        )

        results = response.get("results", [])

        if not results:
            return None

        first = results[0]

        title = first.get("title", "")
        content = first.get("content", "")

        return f"""
📌 {title}

{content[:500]}...
"""

    except Exception:

        return None