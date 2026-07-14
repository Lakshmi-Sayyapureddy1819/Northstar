"""`Company` aggregate — validation and identity/slug derivation."""

import pytest

from northstar.contexts.companies.domain.company import Company
from northstar.contexts.companies.domain.value_objects import CompanySlug


def _base_kwargs() -> dict[str, str]:
    return {
        "name": "Acme Robotics",
        "description": "Builds autonomous warehouse robots.",
        "industry": "Robotics",
        "website": "https://acme.example",
    }


def test_create_derives_id_and_slug():
    company = Company.create(**_base_kwargs())
    assert str(company.slug) == "acme-robotics"
    assert company.id is not None


def test_create_accepts_explicit_slug():
    company = Company.create(**_base_kwargs(), slug=CompanySlug("acme-robotics-inc"))
    assert str(company.slug) == "acme-robotics-inc"


@pytest.mark.parametrize("field", ["name", "industry", "website"])
def test_rejects_blank_required_fields(field: str):
    kwargs = _base_kwargs()
    kwargs[field] = "   "
    with pytest.raises(ValueError):
        Company.create(**kwargs)


@pytest.mark.parametrize("year", [1799, 2101])
def test_rejects_implausible_founded_year(year: int):
    with pytest.raises(ValueError):
        Company.create(**_base_kwargs(), founded_year=year)


def test_accepts_plausible_founded_year():
    company = Company.create(**_base_kwargs(), founded_year=2015)
    assert company.founded_year == 2015


def test_founded_year_is_optional():
    company = Company.create(**_base_kwargs())
    assert company.founded_year is None
