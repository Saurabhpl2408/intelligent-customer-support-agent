"""
Graph node functions.  Each function receives the full ``AgentState``
and returns a partial dict with the keys it wants to update.
"""

from __future__ import annotations

from app.agents.classifier import classify_intent
from app.agents.response_generator import generate_response
from app.core.constants import ESCALATION_REPLY, DEFAULT_FALLBACK_REPLY
from app.core.logging import logger
from app.graph.state import AgentState
from app.models.schemas import ConversationStatus
from app.services.rag_pipeline import run_rag_pipeline


def classify_node(state: AgentState) -> dict:
    logger.info("[node] classify — session=%s", state["session_id"])
    intent = classify_intent(state["message"])
    return {"intent": intent}


def retrieve_node(state: AgentState) -> dict:
    logger.info("[node] retrieve — intent=%s", state.get("intent"))
    rag_result = run_rag_pipeline(state["message"])
    return {
        "rag_context": rag_result.context,
        "sources": rag_result.sources,
    }




def respond_node(state: AgentState) -> dict:
    logger.info("[node] respond — context_len=%d", len(state.get("rag_context", "")))
    reply = generate_response(
        question=state["message"],
        context=state.get("rag_context", ""),
        history=state.get("history"),
    )
    return {"reply": reply, "status": ConversationStatus.ACTIVE}




def escalate_node(state: AgentState) -> dict:
    logger.info("[node] escalate — session=%s", state["session_id"])
    return {
        "reply": ESCALATION_REPLY,
        "status": ConversationStatus.ESCALATED,
    }



def route_after_classify(state: AgentState) -> str:
    """Return the name of the next node based on the detected intent."""
    intent = state.get("intent", "")

    if intent == "contact_human_agent":
        return "escalate"

    if intent in ("greeting", "goodbye"):
        return "respond"          

    return "retrieve"             