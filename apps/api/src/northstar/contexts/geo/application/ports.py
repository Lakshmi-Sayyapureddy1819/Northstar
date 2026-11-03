"""Ports the `geo` application layer depends on.

`CompanyId` is imported from `companies.contract` — the only permitted
cross-context edge (ADR 0001) — never from `companies` internals. `geo`
otherwise knows nothing about what a "company" is, only that it can be given
an opaque, stable identifier and a `Location`.
"""

from __future__ import annotations

from typing import Protocol

from northstar.contexts.companies.contract import CompanyId
from northstar.contexts.geo.contract import NearbyQuery, NearbyResult
from northstar.contexts.geo.domain.value_objects import Location


class CompanyLocationRepository(Protocol):
    """Persistence port for a company's location (one per company, MVP)."""

    def get_by_company_id(self, company_id: CompanyId) -> Location | None: ...

    def set_for_company(self, company_id: CompanyId, location: Location) -> None: ...

    def find_nearby(
        self, query: NearbyQuery, *, limit: int = 50, offset: int = 0
    ) -> list[NearbyResult]: ...
