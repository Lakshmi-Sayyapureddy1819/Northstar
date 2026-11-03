"""geo use cases: attach/read back a company's location, and (Slice 3) find
nearby companies.
"""

from __future__ import annotations

from dataclasses import dataclass

from northstar.contexts.companies.contract import CompanyId
from northstar.contexts.geo.application.ports import CompanyLocationRepository
from northstar.contexts.geo.contract import NearbyQuery, NearbyResult
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


@dataclass(frozen=True, slots=True)
class FindNearbyCompanies:
    """Find companies within a radius of an origin, ordered by distance."""

    repository: CompanyLocationRepository

    def execute(
        self, query: NearbyQuery, *, limit: int = 50, offset: int = 0
    ) -> Result[list[NearbyResult], DomainError]:
        if limit <= 0 or offset < 0:
            return Err(
                DomainError(
                    code="invalid_pagination",
                    message=(
                        f"limit must be > 0 and offset >= 0 (got {limit=}, {offset=})"
                    ),
                )
            )
        if query.radius_km <= 0:
            return Err(
                DomainError(
                    code="invalid_radius",
                    message=f"radius_km must be > 0 (got {query.radius_km})",
                )
            )
        return Ok(self.repository.find_nearby(query, limit=limit, offset=offset))
