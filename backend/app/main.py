"""
FastAPI application entry point.

Responsibilities:
- Create the app instance with lifespan management
- Mount CORS middleware
- Register route modules
- Preload the FAISS vectorstore on startup
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.logging import logger
from app.routes import chat_router, health_router
from app.services.retrieval import load_vectorstore


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown hooks."""
    settings = get_settings()
    logger.info("Starting %s v%s", settings.APP_NAME, settings.APP_VERSION)

    load_vectorstore()

    yield  

    logger.info("Shutting down %s", settings.APP_NAME)


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_router = None  
    app.include_router(health_router)
    app.include_router(chat_router, prefix="/api")

    return app


app = create_app()