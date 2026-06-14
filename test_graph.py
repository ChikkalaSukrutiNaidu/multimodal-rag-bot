from graph.workflow import graph

result = graph.invoke(
    {
        "question": "2 plus 5",
        "retriever": None
    }
)

print(result)