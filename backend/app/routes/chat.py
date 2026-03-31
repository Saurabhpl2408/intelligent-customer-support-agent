"""
Chat endpoint — accepts a user message, runs it through the LangGraph
support-agent workflow, and returns the structured response.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.core.logging import logger
from app.graph.workflow import support_agent_graph
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    ConversationStatus,
    SourceDocument,
)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process a single conversational turn.

    1. Build the initial graph state from the request payload.
    2. Invoke the compiled LangGraph workflow.
    3. Map the final state back to a ``ChatResponse``.
    """
    logger.info(
        "Incoming message — session=%s len=%d history_turns=%d",
        request.session_id,
        len(request.message),
        len(request.history),
    )

    initial_state = {
        "session_id": request.session_id,
        "message": request.message,
        "history": request.history,
        "intent": "",
        "rag_context": "",
        "sources": [],
        "reply": "",
        "status": ConversationStatus.ACTIVE,
    }

    try:
        final_state = support_agent_graph.invoke(initial_state)
    except Exception as exc:
        logger.error("Graph execution failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Agent processing error")

    response = ChatResponse(
        session_id=request.session_id,
        reply=final_state.get("reply", ""),
        intent=final_state.get("intent"),
        sources=final_state.get("sources", []),
        status=final_state.get("status", ConversationStatus.ACTIVE),
    )

    logger.info(
        "Response ready — session=%s intent=%s status=%s",
        response.session_id,
        response.intent,
        response.status,
    )
    return response