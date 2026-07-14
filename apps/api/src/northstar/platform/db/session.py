"""Engine/session management — the one place that knows the DB URL.

Sync SQLAlchemy engine (Simplicity principle: no async session complexity
until a concrete need outgrows it). `get_settings().database_url` is the only
source of the connection string (ADR 0003: config from env only).
"""

from __future__ import annotations

from collections.abc import Generator, Iterator
from contextlib import contextmanager
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from northstar.platform.config import get_settings


class Base(DeclarativeBase):
    """Declarative base shared by every context's SQLAlchemy models."""


@lru_cache
def get_engine() -> Engine:
    """Return the process-wide SQLAlchemy engine, built from settings."""
    return create_engine(get_settings().database_url, pool_pre_ping=True)


@lru_cache
def _session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), autoflush=False, expire_on_commit=False)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency: yield a request-scoped session."""
    session = _session_factory()()
    try:
        yield session
    finally:
        session.close()


@contextmanager
def session_scope() -> Iterator[Session]:
    """Context manager for a session outside a request (scripts, seeds)."""
    session = _session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
