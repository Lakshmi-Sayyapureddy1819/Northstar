"""Public contract for the `companies` context (Core tier).

This module is the ONLY surface other contexts may import. Access to
`companies`'s internals (domain / application / infrastructure) from another
context is forbidden and enforced by import-linter. Expose here only what
other contexts are permitted to consume.

Slice 1 (Company Foundation) exposes: the stable `CompanyId` identity, two
read models (`CompanySummary` for card-sized views, `CompanyDetail` for full
profile views), and the `CompanyReader` port other contexts depend on instead
of reaching into `companies` internals. `Opportunity` (Slice 2) will hold a
`CompanyId` and nothing else from this context — no company fields are
duplicated into `opportunities`.

No concrete `CompanyReader` implementation ships yet — Slice 1 has no
cross-context consumer, so per Simplicity a concrete adapter is deferred
until Slice 2's `opportunities` actually needs to resolve a `CompanyId` into
a summary. Implement `CompanyReader` in `companies/infrastructure/` when that
need is real, not before.

Company-Intelligence fields (Slice 5) will extend `CompanyDetail` additively
— new optional fields — never by renaming or removing what's exposed here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from northstar.contexts.companies.domain.value_objects import CompanyId

__all__ = [
    "CompanyId",
    "CompanySummary",
    "CompanyDetail",
    "CompanyReader",
]


@dataclass(frozen=True, slots=True)
class CompanySummary:
    """Card-sized read model — enough to render a company card or list row."""

    id: CompanyId
    slug: str
    name: str
    industry: str
    description: str


@dataclass(frozen=True, slots=True)
class CompanyDetail:
    """Full read model — a company detail page."""

    id: CompanyId
    slug: str
    name: str
    description: str
    industry: str
    website: str
    careers_page_url: str | None
    founded_year: int | None


class CompanyReader(Protocol):
    """Read-only port other contexts depend on instead of `companies` internals."""

    def get_summary(self, company_id: CompanyId) -> CompanySummary | None: ...

    def get_detail(self, company_id: CompanyId) -> CompanyDetail | None: ...

    def list_summaries(
        self, *, limit: int = 50, offset: int = 0
    ) -> list[CompanySummary]: ...
