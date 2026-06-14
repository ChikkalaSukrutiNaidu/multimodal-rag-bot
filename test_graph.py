from graph.workflow import graph

result = graph.invoke(
    {
        "question": "Explain DBMS normalization",
        "retriever": None
    }
)

print(result)