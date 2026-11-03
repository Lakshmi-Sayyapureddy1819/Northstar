"""Companies router — exercised via TestClient with the repository dependency
overridden by an in-memory fake, so this test needs no live database."""

from dataclasses import dataclass, field

from fastapi.testclient import TestClient

from northstar.api.dependencies import (
    company_location_repository_provider,
    company_repository_provider,
)
from northstar.contexts.companies.domain.company import Company
from northstar.contexts.companies.domain.value_objects import CompanyId, CompanySlug
from northstar.contexts.geo.contract import NearbyQuery, NearbyResult
from northstar.contexts.geo.domain.value_objects import Location
from northstar.main import app

client = TestClient(app)


@dataclass
class FakeCompanyLocationRepository:
    """In-memory stand-in for `CompanyLocationRepository`, local to this test module."""

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
                distance_km=abs(loc.latitude - query.origin.latitude),
            )
            for cid, loc in self.locations.items()
        ]
        results.sort(key=lambda r: r.distance_km)
        return results[offset : offset + limit]


@dataclass
class FakeCompanyRepository:
    """In-memory stand-in for `CompanyRepository`, local to this test module."""

    companies: list[Company] = field(default_factory=list)

    def get_by_id(self, company_id: CompanyId) -> Company | None:
        return next((c for c in self.companies if c.id == company_id), None)

    def get_by_slug(self, slug: CompanySlug) -> Company | None:
        return next((c for c in self.companies if c.slug == slug), None)

    def list_all(self, *, limit: int = 50, offset: int = 0) -> list[Company]:
        return sorted(self.companies, key=lambda c: c.name)[offset : offset + limit]


def _company(name: str) -> Company:
    return Company.create(
        name=name,
        description="A company.",
        industry="Software",
        website="https://example.com",
    )


def _override_repository(repo: FakeCompanyRepository) -> None:
    app.dependency_overrides[company_repository_provider] = lambda: repo


def _override_location_repository(repo: FakeCompanyLocationRepository) -> None:
    app.dependency_overrides[company_location_repository_provider] = lambda: repo


def teardown_function() -> None:
    app.dependency_overrides.clear()


def test_list_companies_returns_seeded_companies():
    repo = FakeCompanyRepository(companies=[_company("Acme"), _company("Beta Corp")])
    _override_repository(repo)

    resp = client.get("/companies")

    assert resp.status_code == 200
    body = resp.json()
    assert [c["name"] for c in body["items"]] == ["Acme", "Beta Corp"]


def test_get_company_returns_detail():
    company = _company("Acme")
    _override_repository(FakeCompanyRepository(companies=[company]))

    resp = client.get(f"/companies/{company.id}")

    assert resp.status_code == 200
    body = resp.json()
    assert body["slug"] == "acme"
    assert body["website"] == "https://example.com"


def test_get_company_returns_404_when_missing():
    _override_repository(FakeCompanyRepository())

    resp = client.get("/companies/00000000-0000-0000-0000-000000000000")

    assert resp.status_code == 404


def test_get_company_by_slug_returns_detail():
    company = _company("Acme")
    _override_repository(FakeCompanyRepository(companies=[company]))

    resp = client.get("/companies/by-slug/acme")

    assert resp.status_code == 200
    assert resp.json()["name"] == "Acme"


def test_get_company_by_slug_returns_404_when_missing():
    _override_repository(FakeCompanyRepository())

    resp = client.get("/companies/by-slug/does-not-exist")

    assert resp.status_code == 404


def test_nearby_companies_returns_hydrated_results_ordered_by_distance():
    near, far = _company("Near Co"), _company("Far Co")
    _override_repository(FakeCompanyRepository(companies=[near, far]))
    location_repo = FakeCompanyLocationRepository()
    location_repo.set_for_company(near.id, Location(latitude=17.44, longitude=78.35))
    location_repo.set_for_company(far.id, Location(latitude=17.50, longitude=78.35))
    _override_location_repository(location_repo)

    resp = client.get("/companies/nearby?lat=17.44&lng=78.35&radius_km=50")

    assert resp.status_code == 200
    body = resp.json()
    assert [c["name"] for c in body["items"]] == ["Near Co", "Far Co"]
    assert body["items"][0]["distance_km"] == 0.0
    assert body["items"][0]["latitude"] == 17.44
    assert body["items"][0]["longitude"] == 78.35
    assert "industry" in body["items"][0]


def test_nearby_companies_requires_lat_lng():
    resp = client.get("/companies/nearby")

    assert resp.status_code == 422


def test_nearby_companies_rejects_non_positive_radius():
    resp = client.get("/companies/nearby?lat=17.44&lng=78.35&radius_km=0")

    assert resp.status_code == 422
