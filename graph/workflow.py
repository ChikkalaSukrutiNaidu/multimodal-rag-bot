from langgraph.graph import StateGraph
from langgraph.graph import END

from graph.state import GraphState

from graph.nodes import (
    router_node,
    company_node,
    rag_node
)

builder = StateGraph(GraphState)

builder.add_node("router", router_node)
builder.add_node("company", company_node)
builder.add_node("rag", rag_node)

builder.set_entry_point("router")


def decide_route(state):
    return state["route"]


builder.add_conditional_edges(
    "router",
    decide_route,
    {
        "company": "company",
        "rag": "rag"
    }
)

builder.add_edge("company", END)
builder.add_edge("rag", END)

graph = builder.compile()