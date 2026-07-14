"""SQLAlchemy implementation of `CompanyRepository`."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from northstar.contexts.companies.domain.company import Company
from northstar.contexts.companies.domain.value_objects import CompanyId, CompanySlug
from northstar.contexts.companies.infrastructure.models import CompanyModel


def _to_domain(row: CompanyModel) -> Company:
    return Company(
        id=CompanyId(row.id),
        slug=CompanySlug(row.slug),
        name=row.name,
        description=row.description,
        industry=row.industry,
        website=row.website,
        careers_page_url=row.careers_page_url,
        founded_year=row.founded_year,
    )


def _to_model(company: Company) -> CompanyModel:
    return CompanyModel(
        id=company.id.value,
        slug=str(company.slug),
        name=company.name,
        description=company.description,
        industry=company.industry,
        website=company.website,
        careers_page_url=company.careers_page_url,
        founded_year=company.founded_year,
    )


class SqlAlchemyCompanyRepository:
    """Postgres-backed `CompanyRepository` (ADR 0003: a swappable adapter)."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, company_id: CompanyId) -> Company | None:
        row = self._session.get(CompanyModel, company_id.value)
        return _to_domain(row) if row is not None else None

    def get_by_slug(self, slug: CompanySlug) -> Company | None:
        row = self._session.scalar(
            select(CompanyModel).where(CompanyModel.slug == str(slug))
        )
        return _to_domain(row) if row is not None else None

    def list_all(self, *, limit: int = 50, offset: int = 0) -> list[Company]:
        rows = self._session.scalars(
            select(CompanyModel).order_by(CompanyModel.name).limit(limit).offset(offset)
        )
        return [_to_domain(row) for row in rows]

    def add(self, company: Company) -> None:
        self._session.add(_to_model(company))
