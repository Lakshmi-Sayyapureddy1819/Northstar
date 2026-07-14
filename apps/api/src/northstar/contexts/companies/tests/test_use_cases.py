"""GetCompany / ListCompanies against an in-memory fake repository — no DB."""

from dataclasses import dataclass, field

from northstar.contexts.companies.application.use_cases import GetCompany, ListCompanies
from northstar.contexts.companies.domain.company import Company
from northstar.contexts.companies.domain.value_objects import CompanyId, CompanySlug
from northstar.shared_kernel import Err, Ok


@dataclass
class FakeCompanyRepository:
    """In-memory stand-in for `CompanyRepository` (application-layer tests
    must not require a live DB — apps/api/CLAUDE.md)."""

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


def test_get_company_returns_ok_when_found():
    company = _company("Acme")
    repo = FakeCompanyRepository(companies=[company])

    result = GetCompany(repository=repo).execute(company.id)

    assert result == Ok(company)


def test_get_company_returns_err_when_missing():
    result = GetCompany(repository=FakeCompanyRepository()).execute(CompanyId.new())

    assert isinstance(result, Err)
    assert result.error.code == "company_not_found"


def test_list_companies_returns_all_within_page():
    companies = [_company("Beta"), _company("Alpha")]
    repo = FakeCompanyRepository(companies=companies)

    result = ListCompanies(repository=repo).execute(limit=10, offset=0)

    assert isinstance(result, Ok)
    assert [c.name for c in result.value] == ["Alpha", "Beta"]


def test_list_companies_rejects_invalid_pagination():
    result = ListCompanies(repository=FakeCompanyRepository()).execute(limit=0)

    assert isinstance(result, Err)
    assert result.error.code == "invalid_pagination"
