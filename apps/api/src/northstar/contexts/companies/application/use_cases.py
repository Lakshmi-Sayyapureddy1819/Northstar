"""Slice-1 use cases: read access to companies.

Thin orchestration only — all business rules live in the domain (`Company`,
`CompanySlug`). Returns `Result` rather than raising, per shared-kernel
convention (`apps/api/CLAUDE.md`).
"""

from __future__ import annotations

from dataclasses import dataclass

from northstar.contexts.companies.application.ports import CompanyRepository
from northstar.contexts.companies.domain.company import Company
from northstar.contexts.companies.domain.value_objects import CompanyId
from northstar.shared_kernel import DomainError, Err, Ok, Result


@dataclass(frozen=True, slots=True)
class GetCompany:
    """Fetch a single company by its stable identity."""

    repository: CompanyRepository

    def execute(self, company_id: CompanyId) -> Result[Company, DomainError]:
        company = self.repository.get_by_id(company_id)
        if company is None:
            return Err(
                DomainError(
                    code="company_not_found",
                    message=f"no company with id {company_id}",
                )
            )
        return Ok(company)


@dataclass(frozen=True, slots=True)
class ListCompanies:
    """List companies, paginated."""

    repository: CompanyRepository

    def execute(
        self, *, limit: int = 50, offset: int = 0
    ) -> Result[list[Company], DomainError]:
        if limit <= 0 or offset < 0:
            return Err(
                DomainError(
                    code="invalid_pagination",
                    message=(
                        f"limit must be > 0 and offset >= 0 (got {limit=}, {offset=})"
                    ),
                )
            )
        return Ok(self.repository.list_all(limit=limit, offset=offset))
