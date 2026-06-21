from langgraph.graph import StateGraph
from langgraph.graph import END

from graph.state import GraphState

from graph.nodes import (
    router_node,
    company_node,
    calculator_node,
    date_node,
    rag_node,
    ipl_stats_node,
    web_node,
    reasoning_node,
    temporal_node
)

builder = StateGraph(GraphState)

builder.add_node("router", router_node)
builder.add_node("company", company_node)
builder.add_node("calculator", calculator_node)
builder.add_node("date", date_node)
builder.add_node("rag", rag_node)
builder.add_node("ipl_stats", ipl_stats_node)
builder.add_node("web", web_node)
builder.add_node("reasoning", reasoning_node)
builder.add_node("temporal", temporal_node)

builder.set_entry_point("router")


def decide_route(state):
    return state["route"]


builder.add_conditional_edges(
    "router",
    decide_route,
    {
        "company": "company",
        "calculator": "calculator",
        "date": "date",
        "rag": "rag",
        "ipl_stats": "ipl_stats",
        "web": "web",
        "reasoning": "reasoning",
        "temporal": "temporal"
    }
)

builder.add_edge("rag", END)
builder.add_edge("ipl_stats", END)
builder.add_edge("web", END)
builder.add_edge("reasoning", END)
builder.add_edge("temporal", END)

graph = builder.compile()