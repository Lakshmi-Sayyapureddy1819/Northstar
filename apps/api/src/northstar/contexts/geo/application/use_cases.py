"""Slice-2 use cases: attach and read back a company's location.

Deliberately minimal — the nearby-query use case (`find_nearby`) is Slice 3's
job, not this slice's (no unused abstractions, per the Slice 1 Boundary
Review lesson).
"""

from __future__ import annotations

from dataclasses import dataclass

from northstar.contexts.companies.contract import CompanyId
from northstar.contexts.geo.application.ports import CompanyLocationRepository
from northstar.contexts.geo.domain.value_objects import Location
from northstar.shared_kernel import DomainError, Err, Ok, Result


@dataclass(frozen=True, slots=True)
class SetCompanyLocation:
    """Persist (or replace) the location for a company."""

    repository: CompanyLocationRepository

    def execute(
        self, company_id: CompanyId, location: Location
    ) -> Result[None, DomainError]:
        self.repository.set_for_company(company_id, location)
        return Ok(None)


@dataclass(frozen=True, slots=True)
class GetCompanyLocation:
    """Read back a company's location."""

    repository: CompanyLocationRepository

    def execute(self, company_id: CompanyId) -> Result[Location, DomainError]:
        location = self.repository.get_by_company_id(company_id)
        if location is None:
            return Err(
                DomainError(
                    code="location_not_found",
                    message=f"no location for company {company_id}",
                )
            )
        return Ok(location)
