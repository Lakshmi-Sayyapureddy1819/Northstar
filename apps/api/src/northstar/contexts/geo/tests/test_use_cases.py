"""SetCompanyLocation / GetCompanyLocation against an in-memory fake — no DB."""

from dataclasses import dataclass, field

from northstar.contexts.companies.contract import CompanyId
from northstar.contexts.geo.application.use_cases import (
    GetCompanyLocation,
    SetCompanyLocation,
)
from northstar.contexts.geo.domain.value_objects import Location
from northstar.shared_kernel import Err, Ok


@dataclass
class FakeCompanyLocationRepository:
    """In-memory stand-in for `CompanyLocationRepository`."""

    locations: dict[CompanyId, Location] = field(default_factory=dict)

    def get_by_company_id(self, company_id: CompanyId) -> Location | None:
        return self.locations.get(company_id)

    def set_for_company(self, company_id: CompanyId, location: Location) -> None:
        self.locations[company_id] = location


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
