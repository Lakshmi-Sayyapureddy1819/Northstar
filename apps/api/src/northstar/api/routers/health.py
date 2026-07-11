"""Health endpoint — the Phase 0 liveness check (blueprint §7)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from northstar.api.dependencies import settings_provider
from northstar.platform.config import Settings

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Liveness payload."""

    status: str
    app_name: str
    version: str
    environment: str


@router.get("/health", response_model=HealthResponse, summary="Liveness check")
def health(settings: Annotated[Settings, Depends(settings_provider)]) -> HealthResponse:
    """Report that the application is up. No external dependencies checked."""
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version=settings.version,
        environment=settings.environment,
    )
