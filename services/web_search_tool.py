from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def tavily_search(query):
    try:
        result = client.search(query=query, search_depth="basic")

        if result and "results" in result:
            top = result["results"][:3]

            answer = "\n\n".join([
                f"{r['title']} - {r['content']}"
                for r in top
            ])

            return answer

        return None

    except Exception as e:
        print("Tavily Error:", e)
        return None