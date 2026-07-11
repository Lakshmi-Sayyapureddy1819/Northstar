"""Configuration platform capability — Pydantic Settings, env-only (ADR 0003)."""

from northstar.platform.config.settings import Environment, Settings, get_settings

__all__ = ["Environment", "Settings", "get_settings"]
