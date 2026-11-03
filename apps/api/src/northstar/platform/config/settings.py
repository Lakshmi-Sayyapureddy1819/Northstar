"""Application configuration — env-only (ADR 0003, Cloud-Agnostic Infrastructure).

Config is read from environment variables (and a local `.env` for developer
convenience). Nothing here hardcodes a vendor or a deployment target; swapping
Postgres/Redis/host is a config change, never a code change.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["local", "test", "staging", "production"]


class Settings(BaseSettings):
    """Typed application settings, sourced from the environment."""

    model_config = SettingsConfigDict(
        env_prefix="NORTHSTAR_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "NorthStar API"
    version: str = "0.0.0"
    environment: Environment = "local"
    debug: bool = False

    # Infrastructure connection strings (behind ports; consumed in later phases).
    database_url: str = (
        "postgresql+psycopg://northstar:northstar@localhost:5432/northstar"
    )
    redis_url: str = "redis://localhost:6379/0"

    # Origins allowed to call the API from a browser (ADR 0004's Core tier is
    # anonymous and served to `apps/web`, a different origin in local dev).
    cors_allowed_origins: list[str] = ["http://localhost:3100"]


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide settings singleton."""
    return Settings()
