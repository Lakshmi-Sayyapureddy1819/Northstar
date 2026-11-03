# Phase 1 — Hyperlocal Career Navigation (Data / product identity)

> Spec: `docs/features/phase1/hyperlocal-career-navigation.md`. Goal
> (blueprint §6): Mapbox + nearby companies + company cards + search by role
> + search by location + company details — reads as career navigation, not a
> job board. Delivered as five sequential slices; never more than one in
> flight at a time.

## Execution order (revised after Slice 1)

Reordered on 2026-07-14, after Slice 1 shipped, to get a visible product
moment on screen as early as possible — same architecture, same five slices,
no new contexts, no ADR change. Rationale and content re-scoping recorded in
`docs/features/phase1/hyperlocal-career-navigation.md`'s "Execution Order"
note and in `docs/features/phase1/slice-2-seed-hyderabad-dataset.md`.

| Order | Slice | Status |
|---|-------|--------|
| 1 | Company Foundation | ✅ Complete |
| 2 | Seed Hyderabad Dataset | ✅ Complete |
| 3 | Map Experience | ✅ Complete |
| 4 | Opportunity Foundation | ⬜ Not started |
| 5 | Company Intelligence | ⬜ Not started |

Original order (superseded, kept for history): Company Foundation →
Opportunity Foundation → Seed Hyderabad Dataset → Map Experience → Company
Intelligence.

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

## Slice 2 — Seed Hyderabad Dataset

Spec: `docs/features/phase1/slice-2-seed-hyderabad-dataset.md`.

- `geo` context filled in for the first time: domain (`domain/value_objects.py`
  — `Location`, validated lat/lng), application (`application/{ports,use_cases}.py`
  — `SetCompanyLocation`/`GetCompanyLocation`), infrastructure
  (`infrastructure/{models,repository}.py` — PostGIS-backed `company_locations`
  table, `geography(Point,4326)` + GIST index, PK = `company_id`), `contract.py`
  (exposes `Location` only — no read port yet, deferred to Slice 3). See
  `contexts/geo/CLAUDE.md`.
- `Company` (Slice 1) is completely unchanged — this slice only adds rows via
  the existing repository, confirming the aggregate's additive-extensibility
  design actually holds under a second slice.
- Second Alembic migration (`company_locations`). New dependencies:
  `geoalchemy2`, `shapely`. One real bug caught during migration: geoalchemy2's
  `Geography(spatial_index=True)` auto-creates its GIST index via a
  CREATE-TABLE event listener — the initial autogenerated migration also
  explicitly called `op.create_index(...)`, causing a duplicate-index error on
  first apply. Fixed by removing the explicit index calls and letting
  geoalchemy2 own index creation/drop; `alembic check` confirmed the model
  metadata still matches reality afterward.
- Seed script (`apps/api/scripts/seed_hyderabad_companies.py`) + data
  (`apps/api/scripts/data/hyderabad_companies.json`): 30 real Hyderabad
  SWE/AI-ML companies (target was 25–50), evenly spread across all seven
  requested localities (Gachibowli 5, Raidurg 5, Madhapur 4, Hitech City 4,
  Financial District 4, Kondapur 4, Nanakramguda 4). Load/persist separated
  so a future real data source only replaces the load step (see the spec's
  "Seed pipeline design"). One real data bug caught live: State Street
  Corporation's `founded_year: 1792` violated `Company`'s own `[1800, 2100]`
  validation (a legitimate Slice 1 invariant, not a bug in it) — fixed by
  nulling the field for that one ambiguous record rather than widening the
  domain's validation range.
- No API changes — zero OpenAPI contract drift, confirmed by regenerating and
  diffing.

**Verification:** `ruff` / `black --check` / `mypy --strict` / `lint-imports`
/ `pytest` all green (39/39 tests: 28 from Slice 1 + 11 new `geo` tests).
`alembic upgrade head` + `alembic check` green against a fresh database. Seed
run live against real Postgres+PostGIS twice: first run → 30 created, 0
skipped; second run → 0 created, 30 skipped (idempotency proven, not just
claimed). All 30 seeded coordinates verified inside a Hyderabad bounding box
(17.2–17.6°N, 78.2–78.6°E) via a live SQL check; a sample `ST_DWithin` query
around Gachibowli's center correctly returned 21 companies within 3km,
proving the PostGIS geography column is genuinely queryable ahead of Slice 3
building the real nearby-query use case on top of it.

**Slice Boundary Review (pre-merge, `architecture-guardian`):** PASS on all 7
checks — file placement, no speculative abstractions (`geo.contract` exposes
`Location` only, no premature read port), no future-phase functionality
(`Opportunity`/Mapbox/`JobProvider`/Company Intelligence all absent),
`Company` aggregate byte-for-byte unchanged, `geo` depends only on the opaque
`CompanyId` from `companies.contract`, seed data distribution/quality
verified, import-linter 2/2 kept. One documentation gap the review caught —
this section was missing before the review ran — closed by this update. One
non-blocking note for the record: the seed script imports `companies`
internals directly (`Company`, `CompanySlug`, `SqlAlchemyCompanyRepository`)
rather than going through `companies.contract`, because Slice 1 shipped no
write use case (only `GetCompany`/`ListCompanies`) — pre-authorized by this
slice's approved spec, same category as `scripts/export_openapi.py`, but
worth watching: if Slice 4's opportunity seed repeats this pattern, consider
whether `companies` needs a real `CreateCompany` application use case instead
of every future seed reaching around the contract.

## Acceptance criteria checklist (Slice 2 — Seed Hyderabad Dataset)

| # | Acceptance criterion | Status |
|---|---|---|
| 1 | `geo.contract` exposes a validated `Location` value object | ✅ Complete |
| 2 | `company_locations` table with PostGIS geography column + GIST index; no columns added to `companies` | ✅ Complete |
| 3 | Seed produces ≥15 (target 25–50) real Hyderabad companies with resolvable coordinates | ✅ Complete — 30 companies, 0 out-of-bounds |
| 4 | Every seed record traceable to a real, resolvable source (company website) | ✅ Complete |
| 5 | Re-running the seed is idempotent | ✅ Complete — proven live (30 created → 0 created/30 skipped) |
| 6 | Cross-slice: ruff/black/mypy --strict/lint-imports/pytest all pass | ✅ Complete |
| 7 | Cross-slice: `alembic upgrade head` + `alembic check` green for the new migration | ✅ Complete |
| 8 | Slice Boundary Review passes before merge | ✅ Complete — 7/7 passed, 1 doc gap closed, 1 note recorded |

## Slice 3 — Map Experience

Spec: `docs/features/phase1/slice-3-map-experience.md`.

- `geo` gained the read port Slices 1/2 deliberately deferred:
  `FindNearbyCompanies` (`application/use_cases.py`), `NearbyQuery`/
  `NearbyResult` in `contract.py` (defined directly in the contract, mirroring
  `companies.contract`'s pattern — not imported from application), and
  `SqlAlchemyCompanyLocationRepository.find_nearby` using `ST_DWithin` +
  `ST_Distance` against Slice 2's `company_locations`. **No new migration** —
  proof that table was already the right shape.
- New endpoints: `GET /companies/nearby` (composes `geo`'s nearby query with
  `companies`' `GetCompany` to hydrate `CompanySummary` + `distance_km` +
  `latitude`/`longitude` per result) and `GET /companies/by-slug/{slug}`
  (the deep-link route's lookup, backed by Slice 1's existing
  `CompanyRepository.get_by_slug`). Both registered ahead of
  `/{company_id}` in the router to avoid UUID-parsing shadowing.
- Frontend: first real feature module, `apps/web/src/features/map/` —
  Mapbox GL (client-only dynamic import, `ssr:false`), custom "career node"
  markers (industry-tinted glow circles, not default pins — native
  clustering via `react-map-gl`'s declarative `Source`/`Layer`), a locality
  picker + "Near Me" + client-side industry filter chips (derived from the
  real seeded `industry` field, no schema change), a company detail panel
  (drawer) plus the deep-linkable `/companies/[slug]` route, and a NorthStar
  brand token system (`globals.css` `.theme-brand`) with three deliberately
  chosen typefaces (Fraunces/Manrope/IBM Plex Mono) replacing the Phase 0
  placeholder home page entirely.
- Four real bugs caught only by running the full stack: missing CORS
  middleware (fixed with a `GET`-only `CORSMiddleware`), a missing
  `latitude`/`longitude` on the nearby response (the map can't place a
  marker from distance alone), `prefers-reduced-motion` not actually
  reaching Framer Motion's JS-driven animations (fixed with
  `useReducedMotion()` at three call sites), and a missing `<main>` landmark.
  See the feature spec's "As implemented" section for full detail.

**Verification:** backend — `ruff`/`black --check`/`mypy --strict`/
`lint-imports`/`pytest` all green (48/48 tests); `alembic check` clean (no
schema change). Frontend — `tsc --noEmit`/`eslint`/Prettier all clean; 12/12
Vitest unit tests; 7/7 Playwright e2e tests against the real backend and
real seeded data (full anonymous journey, "Near Me" denied → graceful
fallback, full keyboard-only reachability into the detail dialog); full
`turbo run lint typecheck test build` pipeline green (4/4 tasks); production
build confirms Mapbox GL is code-split off the main bundle (162kB total
first-load JS — far too small to include Mapbox GL, which alone is
200KB+). Performance: Lighthouse via chrome-devtools MCP wasn't reachable in
this environment; a Playwright-measured first-contentful-paint (~100ms)
served as an honest proxy, not a substitute for the real audit — flagged
explicitly as a gap to close when browser tooling is available. OpenAPI
regenerated with exactly the two new paths, zero unexpected drift.

**Slice Boundary Review (pre-merge, `architecture-guardian`):** CLEAN —
every check passed (module boundaries, contract-only imports, Facts-First,
cloud-agnostic, API-contracts-as-truth, anonymous-first, Living
Documentation, ADR requirements, PRD traceability), independently
re-verified rather than taken on faith: the reviewer re-ran `lint-imports`
(2/2 kept), `pytest` (green), and `tsc --noEmit` (clean) itself. One
non-blocking style note: `api/routers/companies.py` imported `Location`
from `geo.domain.value_objects` instead of the now-available
`geo.contract` — fixed (one-line import change), re-verified green after
the fix.

## Acceptance criteria checklist (Slice 3 — Map Experience)

| # | Acceptance criterion | Status |
|---|---|---|
| 1 | Mapbox integration: client-only, code-split, token via env | ✅ Complete |
| 2 | Public home page replaces Phase 0 placeholder, map-dominant layout | ✅ Complete |
| 3 | Career nodes (custom markers) — no default Mapbox pins | ✅ Complete |
| 4 | Marker clustering (native, no extra library) | ✅ Complete |
| 5 | Map-load animation, `prefers-reduced-motion` respected | ✅ Complete (fixed a real gap — see above) |
| 6 | Company cards: locality, industry, distance, honest reserved score slot (no fabricated rating) | ✅ Complete |
| 7 | Filter chips (industry, client-side, companies only) | ✅ Complete |
| 8 | Company detail panel + deep-linkable `/companies/[slug]` | ✅ Complete |
| 9 | Search by location (locality picker, curated, not a geocoder) | ✅ Complete |
| 10 | "Near Me" with graceful fallback (denied/unsupported/error) | ✅ Complete — verified live in Playwright |
| 11 | Responsive layout | ✅ Complete |
| 12 | Accessibility: full keyboard/screen-reader path independent of the map, `<main>` landmark | ✅ Complete — verified live in Playwright |
| 13 | Performance: LCP target, code-split bundle | ⚠️ Partially verified — bundle size confirmed; full Lighthouse LCP audit not run (browser tooling unavailable), FCP proxy measured instead |
| 14 | Career Universe CTA present, disabled, zero Phase 2 logic | ✅ Complete |
| 15 | Cross-slice: all quality gates + tests pass | ✅ Complete |
