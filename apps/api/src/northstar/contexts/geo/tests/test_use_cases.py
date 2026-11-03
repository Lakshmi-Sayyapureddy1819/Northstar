"""SetCompanyLocation / GetCompanyLocation / FindNearbyCompanies against an
in-memory fake — no DB. The real PostGIS `ST_DWithin`/`ST_Distance` query is
verified live against a real database as part of Slice 3's manual
verification (same pattern as Slice 2), not duplicated here as a DB-coupled
automated test — keeps `pytest` DB-free in every environment, matching
Slices 1–2.
"""

import math
from dataclasses import dataclass, field

from northstar.contexts.companies.contract import CompanyId
from northstar.contexts.geo.application.use_cases import (
    FindNearbyCompanies,
    GetCompanyLocation,
    SetCompanyLocation,
)
from northstar.contexts.geo.contract import NearbyQuery, NearbyResult
from northstar.contexts.geo.domain.value_objects import Location
from northstar.shared_kernel import Err, Ok

_EARTH_RADIUS_KM = 6371.0


def _haversine_km(a: Location, b: Location) -> float:
    lat1, lat2 = math.radians(a.latitude), math.radians(b.latitude)
    dlat = math.radians(b.latitude - a.latitude)
    dlng = math.radians(b.longitude - a.longitude)
    h = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    )
    return 2 * _EARTH_RADIUS_KM * math.asin(math.sqrt(h))


@dataclass
class FakeCompanyLocationRepository:
    """In-memory stand-in for `CompanyLocationRepository`."""

    locations: dict[CompanyId, Location] = field(default_factory=dict)

    def get_by_company_id(self, company_id: CompanyId) -> Location | None:
        return self.locations.get(company_id)

    def set_for_company(self, company_id: CompanyId, location: Location) -> None:
        self.locations[company_id] = location

    def find_nearby(
        self, query: NearbyQuery, *, limit: int = 50, offset: int = 0
    ) -> list[NearbyResult]:
        results = [
            NearbyResult(
                company_id=cid,
                location=loc,
                distance_km=_haversine_km(query.origin, loc),
            )
            for cid, loc in self.locations.items()
        ]
        results = [r for r in results if r.distance_km <= query.radius_km]
        results.sort(key=lambda r: r.distance_km)
        return results[offset : offset + limit]


def test_set_then_get_round_trips():
    repo = FakeCompanyLocationRepository()
    company_id = CompanyId.new()
    location = Location(latitude=17.4483, longitude=78.3915)

    SetCompanyLocation(repository=repo).execute(company_id, location)
    result = GetCompanyLocation(repository=repo).execute(company_id)

    assert result == Ok(location)


def test_set_replaces_existing_location():
    repo = FakeCompanyLocationRepository()
    company_id = CompanyId.new()
    SetCompanyLocation(repository=repo).execute(
        company_id, Location(latitude=1, longitude=1)
    )

    new_location = Location(latitude=17.4483, longitude=78.3915)
    SetCompanyLocation(repository=repo).execute(company_id, new_location)

    assert GetCompanyLocation(repository=repo).execute(company_id) == Ok(new_location)


def test_get_returns_err_when_missing():
    result = GetCompanyLocation(repository=FakeCompanyLocationRepository()).execute(
        CompanyId.new()
    )

    assert isinstance(result, Err)
    assert result.error.code == "location_not_found"


def _gachibowli(offset_deg: float = 0.0) -> Location:
    return Location(latitude=17.4401 + offset_deg, longitude=78.3489 + offset_deg)


def test_find_nearby_orders_by_distance_ascending():
    repo = FakeCompanyLocationRepository()
    near, mid, far = CompanyId.new(), CompanyId.new(), CompanyId.new()
    repo.set_for_company(far, _gachibowli(0.05))
    repo.set_for_company(near, _gachibowli(0.001))
    repo.set_for_company(mid, _gachibowli(0.01))

    result = FindNearbyCompanies(repository=repo).execute(
        NearbyQuery(origin=_gachibowli(), radius_km=50)
    )

    assert isinstance(result, Ok)
    assert [r.company_id for r in result.value] == [near, mid, far]


def test_find_nearby_excludes_results_outside_radius():
    repo = FakeCompanyLocationRepository()
    close, distant = CompanyId.new(), CompanyId.new()
    repo.set_for_company(close, _gachibowli(0.001))
    repo.set_for_company(
        distant, Location(latitude=28.6139, longitude=77.2090)
    )  # Delhi

    result = FindNearbyCompanies(repository=repo).execute(
        NearbyQuery(origin=_gachibowli(), radius_km=10)
    )

    assert isinstance(result, Ok)
    assert [r.company_id for r in result.value] == [close]


def test_find_nearby_rejects_non_positive_radius():
    result = FindNearbyCompanies(repository=FakeCompanyLocationRepository()).execute(
        NearbyQuery(origin=_gachibowli(), radius_km=0)
    )

    assert isinstance(result, Err)
    assert result.error.code == "invalid_radius"


def test_find_nearby_rejects_invalid_pagination():
    result = FindNearbyCompanies(repository=FakeCompanyLocationRepository()).execute(
        NearbyQuery(origin=_gachibowli(), radius_km=10), limit=0
    )

    assert isinstance(result, Err)
    assert result.error.code == "invalid_pagination"
