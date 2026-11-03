"""Application assembly — router registration and DI wiring (blueprint §4.1).

This is the composition root of the modular monolith. It wires the thin HTTP
layer to platform capabilities and context contracts. It holds no business
logic itself.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from northstar.api.routers import companies, health
from northstar.platform.config import get_settings


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description=(
            "NorthStar API — modular monolith. See docs/architecture/blueprint.md."
        ),
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    app.include_router(health.router)
    app.include_router(companies.router)
    return app


app = create_app()
