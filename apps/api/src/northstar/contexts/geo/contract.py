"""Public contract for the `geo` context (Core tier).

This module is the ONLY surface other contexts may import. Access to
`geo`'s internals (domain / application / infrastructure) from another
context is forbidden and enforced by import-linter. Expose here only what
other contexts are permitted to consume.

Slice 2 (Seed Hyderabad Dataset) added `Location`, a validated
latitude/longitude value object. Slice 3 (Map Experience) adds the
nearby-query read models (`NearbyQuery`, `NearbyResult`) now that there's a
real caller (the `GET /companies/nearby` endpoint) — the read port the
Slice 1/2 reviews deliberately deferred until one existed. Application and
infrastructure import these shapes from here, mirroring how
`companies.contract` defines `CompanySummary`/`CompanyDetail` directly rather
than the other layers defining them and contract re-exporting.
"""

from __future__ import annotations

from dataclasses import dataclass

from northstar.contexts.companies.contract import CompanyId
from northstar.contexts.geo.domain.value_objects import Location

__all__ = ["Location", "NearbyQuery", "NearbyResult"]


@dataclass(frozen=True, slots=True)
class NearbyQuery:
    """Find companies within `radius_km` of `origin`."""

    origin: Location
    radius_km: float


@dataclass(frozen=True, slots=True)
class NearbyResult:
    """A company found by a nearby query, with its distance from the origin.

    Carries the company's own `Location` too — the map needs real
    coordinates to place a marker, not just a distance.
    """

    company_id: CompanyId
    location: Location
    distance_km: float
