"""
Health-check endpoint for container orchestrators and monitoring.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.core.config import get_settings
from app.models.schemas import HealthResponse
from app.services.retrieval import is_vectorstore_ready

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        vectorstore_loaded=is_vectorstore_ready(),
    )