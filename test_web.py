from services.web_search_tool import get_web_search_tool

search = get_web_search_tool()

results = search("Who is CEO of TCS?")

print(results)