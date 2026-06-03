from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def tavily_search(query):

    try:

        response = client.search(
            query=query,
            search_depth="basic",
            max_results=3
        )

        results = response.get("results", [])

        if not results:
            return None

        first = results[0]

        title = first.get("title", "")
        content = first.get("content", "")

        answer = f"""
Title: {title}

Summary:
{content[:300]}...
"""

        return answer

    except Exception as e:

        print("Tavily Error:", e)

        return None