"""Companies router — exercised via TestClient with the repository dependency
overridden by an in-memory fake, so this test needs no live database."""

from dataclasses import dataclass, field

from fastapi.testclient import TestClient

from northstar.api.dependencies import company_repository_provider
from northstar.contexts.companies.domain.company import Company
from northstar.contexts.companies.domain.value_objects import CompanyId, CompanySlug
from northstar.main import app

client = TestClient(app)


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
