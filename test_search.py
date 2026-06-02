# test_search.py

from services.web_search_tool import web_search

results = web_search("current CEO of Wipro")

print("RESULTS:")
print(results)
print(type(results))