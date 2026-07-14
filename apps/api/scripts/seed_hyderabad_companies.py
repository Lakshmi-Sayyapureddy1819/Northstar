"""Seed real Hyderabad SWE/AI-ML companies with locations (Phase 1, Slice 2).

Loads a static JSON file (`scripts/data/hyderabad_companies.json`) and
persists through the existing `companies`/`geo` application-layer building
blocks — the same call path a future automated data source would use if the
static list were ever replaced (see
`docs/features/phase1/slice-2-seed-hyderabad-dataset.md`, "Seed pipeline
design"). Idempotent: a company already present by slug is not recreated;
its location is upserted either way.

Run via: `uv run python scripts/seed_hyderabad_companies.py`
"""

from __future__ import annotations

import json
from pathlib import Path

from northstar.contexts.companies.domain.company import Company
from northstar.contexts.companies.domain.value_objects import CompanySlug
from northstar.contexts.companies.infrastructure.repository import (
    SqlAlchemyCompanyRepository,
)
from northstar.contexts.geo.domain.value_objects import Location
from northstar.contexts.geo.infrastructure.repository import (
    SqlAlchemyCompanyLocationRepository,
)
from northstar.platform.db import session_scope

DATA_FILE = Path(__file__).resolve().parent / "data" / "hyderabad_companies.json"


def main() -> None:
    records = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    created = 0
    skipped = 0

    with session_scope() as session:
        companies_repo = SqlAlchemyCompanyRepository(session)
        locations_repo = SqlAlchemyCompanyLocationRepository(session)

        for record in records:
            slug = CompanySlug.from_name(record["name"])
            existing = companies_repo.get_by_slug(slug)
            if existing is not None:
                company = existing
                skipped += 1
            else:
                company = Company.create(
                    name=record["name"],
                    description=record["description"],
                    industry=record["industry"],
                    website=record["website"],
                    careers_page_url=record.get("careers_page_url"),
                    founded_year=record.get("founded_year"),
                    slug=slug,
                )
                companies_repo.add(company)
                session.flush()  # ensure the FK target exists before the location row
                created += 1

            locations_repo.set_for_company(
                company.id,
                Location(latitude=record["latitude"], longitude=record["longitude"]),
            )

    print(
        f"Seed complete: {created} created, {skipped} already present "
        f"(of {len(records)} total)."
    )


if __name__ == "__main__":
    main()
