"""FastAPI dependency providers for the thin HTTP layer.

The HTTP layer wires platform capabilities and context contracts into routers.
Keep it thin: no business logic here.
"""

from __future__ import annotations

from northstar.platform.config import Settings, get_settings


def settings_provider() -> Settings:
    """Provide application settings to routers via dependency injection."""
    return get_settings()
