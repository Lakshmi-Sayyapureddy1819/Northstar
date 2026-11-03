"""FastAPI dependency providers for the thin HTTP layer.

The HTTP layer wires platform capabilities and context contracts into routers.
Keep it thin: no business logic here.
"""

from __future__ import annotations

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from northstar.contexts.companies.application.use_cases import (
    GetCompany,
    GetCompanyBySlug,
    ListCompanies,
)
from northstar.contexts.companies.infrastructure.repository import (
    SqlAlchemyCompanyRepository,
)
from northstar.contexts.geo.application.use_cases import FindNearbyCompanies
from northstar.contexts.geo.infrastructure.repository import (
    SqlAlchemyCompanyLocationRepository,
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


def get_company_by_slug_use_case_provider(
    repository: Annotated[
        SqlAlchemyCompanyRepository, Depends(company_repository_provider)
    ],
) -> GetCompanyBySlug:
    return GetCompanyBySlug(repository=repository)


def company_location_repository_provider(
    session: Annotated[Session, Depends(db_session_provider)],
) -> SqlAlchemyCompanyLocationRepository:
    return SqlAlchemyCompanyLocationRepository(session)


def find_nearby_companies_use_case_provider(
    repository: Annotated[
        SqlAlchemyCompanyLocationRepository,
        Depends(company_location_repository_provider),
    ],
) -> FindNearbyCompanies:
    return FindNearbyCompanies(repository=repository)
