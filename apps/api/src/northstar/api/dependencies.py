"""FastAPI dependency providers for the thin HTTP layer.

The HTTP layer wires platform capabilities and context contracts into routers.
Keep it thin: no business logic here.
"""

from __future__ import annotations

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from northstar.contexts.companies.application.use_cases import GetCompany, ListCompanies
from northstar.contexts.companies.infrastructure.repository import (
    SqlAlchemyCompanyRepository,
)
from northstar.platform.config import Settings, get_settings
from northstar.platform.db import get_session


def settings_provider() -> Settings:
    """Provide application settings to routers via dependency injection."""
    return get_settings()


def db_session_provider() -> Generator[Session, None, None]:
    """Provide a request-scoped SQLAlchemy session."""
    yield from get_session()


def company_repository_provider(
    session: Annotated[Session, Depends(db_session_provider)],
) -> SqlAlchemyCompanyRepository:
    return SqlAlchemyCompanyRepository(session)


def get_company_use_case_provider(
    repository: Annotated[
        SqlAlchemyCompanyRepository, Depends(company_repository_provider)
    ],
) -> GetCompany:
    return GetCompany(repository=repository)


def list_companies_use_case_provider(
    repository: Annotated[
        SqlAlchemyCompanyRepository, Depends(company_repository_provider)
    ],
) -> ListCompanies:
    return ListCompanies(repository=repository)
