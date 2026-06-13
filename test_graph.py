from graph.workflow import graph


result = graph.invoke(
    {
        "question": "Who is CEO of TCS?",
        "retriever": None
    }
)

print(result)