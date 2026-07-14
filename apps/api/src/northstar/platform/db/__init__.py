"""Database platform capability (Postgres + PostGIS + pgvector).

Owns connection/session management and the SQLAlchemy declarative base.
Concrete repositories live in each context's infrastructure layer — this
module never contains business logic, only the technical means to reach the
database (ADR 0003: infra behind ports, config from env only).
"""

from __future__ import annotations

from northstar.platform.db.session import Base, get_engine, get_session, session_scope

__all__ = ["Base", "get_engine", "get_session", "session_scope"]
