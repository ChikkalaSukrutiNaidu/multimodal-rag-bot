from graph.workflow import graph

result = graph.invoke(
    {
        "question": "latest AI news",
        "retriever": None
    }
)

print(result)