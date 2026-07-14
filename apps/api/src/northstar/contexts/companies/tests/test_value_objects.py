"""CompanyId / CompanySlug — identity is stable, slug is mutable and derived."""

import uuid

import pytest

from northstar.contexts.companies.domain.value_objects import CompanyId, CompanySlug


def test_company_id_round_trips_through_str():
    company_id = CompanyId.new()
    assert CompanyId.from_str(str(company_id)) == company_id


def test_company_id_equality_is_value_based():
    raw = uuid.uuid4()
    assert CompanyId(raw) == CompanyId(raw)


def test_slug_derived_from_name_is_lowercase_hyphenated():
    assert str(CompanySlug.from_name("Acme  Robotics & Co.")) == "acme-robotics-co"


def test_slug_rejects_invalid_format():
    with pytest.raises(ValueError):
        CompanySlug("Not A Slug!")


def test_slug_cannot_be_derived_from_blank_name():
    with pytest.raises(ValueError):
        CompanySlug.from_name("   ")
