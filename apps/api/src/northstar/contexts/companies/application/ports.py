"""Ports the `companies` application layer depends on.

Infrastructure implements these; domain/application never import a concrete
driver (ADR 0003 — infra behind ports).
"""

from __future__ import annotations

from typing import Protocol

from northstar.contexts.companies.domain.company import Company
from northstar.contexts.companies.domain.value_objects import CompanyId, CompanySlug


class CompanyRepository(Protocol):
    """Persistence port for `Company` aggregates."""

    def get_by_id(self, company_id: CompanyId) -> Company | None: ...

    def get_by_slug(self, slug: CompanySlug) -> Company | None: ...

    def list_all(self, *, limit: int = 50, offset: int = 0) -> list[Company]: ...
