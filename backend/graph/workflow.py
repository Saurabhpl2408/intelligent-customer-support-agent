"""
LangGraph workflow definition.

Graph topology
--------------

    START ──► classify ──┬──► retrieve ──► respond ──► END
                         │
                         ├──► respond  ──► END   (greeting / goodbye)
                         │
                         └──► escalate ──► END   (contact_human_agent)
"""

from __future__ import annotations

from langgraph.graph import StateGraph, END

from app.graph.state import AgentState
from app.graph.nodes import (
    classify_node,
    retrieve_node,
    respond_node,
    escalate_node,
    route_after_classify,
)
from app.core.logging import logger


def build_graph() -> StateGraph:
    """Construct and compile the support-agent state graph."""

    graph = StateGraph(AgentState)

    graph.add_node("classify", classify_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("respond", respond_node)
    graph.add_node("escalate", escalate_node)

    graph.set_entry_point("classify")

    graph.add_conditional_edges(
        "classify",
        route_after_classify,
        {
            "retrieve": "retrieve",
            "respond": "respond",
            "escalate": "escalate",
        },
    )

    graph.add_edge("retrieve", "respond")
    graph.add_edge("respond", END)
    graph.add_edge("escalate", END)

    logger.info("LangGraph workflow compiled successfully")
    return graph.compile()


support_agent_graph = build_graph()