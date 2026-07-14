# Phase 1 — Hyperlocal Career Navigation (Data / product identity)

> Spec: `docs/features/phase1/hyperlocal-career-navigation.md`. Goal
> (blueprint §6): Mapbox + nearby companies + company cards + search by role
> + search by location + company details — reads as career navigation, not a
> job board. Delivered as five sequential slices; never more than one in
> flight at a time.

## Slice status

| # | Slice | Status |
|---|-------|--------|
| 1 | Company Foundation | ✅ Complete |
| 2 | Opportunity Foundation | ⬜ Not started |
| 3 | Seed Hyderabad Dataset | ⬜ Not started |
| 4 | Map Experience | ⬜ Not started |
| 5 | Company Intelligence | ⬜ Not started |

## Slice 1 — Company Foundation

- `Company` aggregate root: domain (`domain/company.py`, `domain/value_objects.py`),
  application (`application/{ports,use_cases}.py`), infrastructure
  (`infrastructure/{models,repository}.py`), `contract.py`
  (`CompanyId`, `CompanySummary`, `CompanyDetail`, `CompanyReader` — the
  concrete adapter is deferred to Slice 2, see Slice Boundary Review below).
- Identity/slug split: `CompanyId` (stable) vs. `CompanySlug` (mutable, SEO).
  See `contexts/companies/CLAUDE.md`.
- First real DB dependency added (`sqlalchemy`, `alembic`, `psycopg`); first
  Alembic migration (`companies` table); `platform/db/` filled in
  (engine/session, declarative `Base`).
- `GET /companies` (paginated list) and `GET /companies/{company_id}` (detail)
  — thin router, `apps/api/CLAUDE.md`-style `Result`-based use cases
  underneath.
- CI gained a `database` job (blueprint §7 footnote: the first migration
  triggers the migration-check gate) — `alembic upgrade head` against a clean
  Postgres+PostGIS service, then `alembic check`.
- Tests: domain (value objects + aggregate validation), application (use
  cases against an in-memory fake repository — no DB required), API
  (`TestClient` with the repository dependency overridden). Verified live
  against a real Postgres row end-to-end (insert → API → JSON) during review.
- Docs: `contexts/companies/CLAUDE.md` (new), `docs/database/schema-overview.md`
  (new), `docs/api/pagination.md` (new), `docs/api/contract-generation.md`
  (verification note appended), this file, `docs/project-history.md`,
  `docs/features/phase1/hyperlocal-career-navigation.md` (Slice 1 acceptance
  criteria reconciled with as-built).

**Verification:** `ruff` / `black --check` / `mypy --strict` / `lint-imports`
/ `pytest` all green; `alembic upgrade head` + `alembic check` green against a
fresh database; OpenAPI regenerated with zero drift; frontend `tsc --noEmit`
green against the new contract; full `scripts/verify-phase0.sh` gauntlet
re-run green end-to-end with Slice 1 in place.

**Slice Boundary Review (pre-merge, `architecture-guardian`):** independently
verified — every new file belongs to `companies` or infrastructure/platform;
no future-phase functionality (geo, opportunities, seed data, map UI, Company
Intelligence fields) present; `Company` holds only plain factual fields; zero
coupling to `career_intelligence`/`resume`/`polaris`/`identity`/`profile`/
`engagement`/`career_gps` (mechanically confirmed, import-linter 2/2 kept).
One finding: `SqlAlchemyCompanyReader` (infrastructure) had zero callers this
slice — removed as a speculative abstraction; the `CompanyReader` contract
type stays since Slice 1's acceptance criteria required the read-model shapes
to exist independent of a consumer. Full re-verification after the fix: all
gates still green (28/28 tests).

## Acceptance criteria checklist (Slice 1 — Company Foundation)

| # | Acceptance criterion | Status |
|---|---|---|
| 1 | `companies.contract` exposes typed `CompanyId`, `CompanySummary`, `CompanyDetail` — no other context/API layer reaches `companies` internals directly | ✅ Complete |
| 2 | Company domain entity and value objects unit-tested without a live DB | ✅ Complete — `contexts/companies/tests/{test_company.py,test_value_objects.py}` |
| 3 | import-linter's two contracts still pass with `companies` now non-empty | ✅ Complete — 2 kept, 0 broken (102 files, 44 deps) |
| 4 | Cross-slice: ruff/black/mypy --strict/lint-imports/pytest all pass | ✅ Complete |
| 5 | Cross-slice: `scripts/verify-phase0.sh`-equivalent gauntlet stays green, extended with the first Alembic migration check | ✅ Complete — `database` CI job added; full gauntlet re-run green |
| 6 | Cross-slice: docs/ADR land in the same commit as the change (Living Documentation) | ✅ Complete — see doc list above |
| 7 | (Added during review) Slice Boundary Review passes all 5 checks before merge | ✅ Complete — 4/5 passed outright, 1 finding resolved (see above) |
