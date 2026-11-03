# Phase 1 — Hyperlocal Career Navigation (Feature Specification)

> **Status:** Approved. Slice 1 (Company Foundation) implemented, verified,
> Slice-Boundary-reviewed, complete, and tagged `phase1-slice1`. **Execution
> order revised 2026-07-14** (see Rollout Plan) — Seed Hyderabad Dataset now
> runs second and Map Experience third, ahead of Opportunity Foundation, so a
> visible map experience lands as early as possible. Architecture, contexts,
> and ADRs are unchanged; only the build sequence and each slice's content
> boundary shifted accordingly. Traces to `docs/product/prd.md` and
> `docs/product/mvp-scope.md`; implements blueprint §6 Phase 1 ("Data /
> product identity"). Does not modify the frozen
> `docs/architecture/blueprint.md` or any ADR — it builds inside the
> boundaries ADRs 0001–0009 already fixed.

## Vision

A first-time, anonymous visitor opens NorthStar and — within one screen —
understands: *this is a map of my career, not a list of job postings.* They
see real companies near a real location in Hyderabad, can search by role or
place, and can open a company to see a structured, factual profile. No login,
no application funnel, no keyword-search box pretending to be a job board.

This slice is the product's **identity moment**: the one screen every
downstream phase (Career Universe, Career Intelligence, Resume Intelligence,
Career GPS, Polaris) will build on top of. Get the data model and the map
experience right here, and every later phase reuses it rather than
re-deriving it — this is also the acid test for **Additive Extensibility**.

## Problem Statement

Today the repository has skeleton contexts (`companies`, `opportunities`,
`geo` — empty `contract.py`, empty layer folders) and no data. There is no
way for a user to see anything, and no canonical company/opportunity/location
data for any later phase (Career Universe, engines, Resume Intelligence) to
consume. Phase 1 must produce the **first real, factual, geolocated dataset**
of Hyderabad SWE/AI-ML companies and roles, exposed through a map-first UI —
without introducing AI, auth, or recommendation logic, all of which are
explicitly out of scope until later phases.

## Goals

1. Stand up real domain models and contracts for `companies`, `opportunities`,
   and `geo` (currently empty skeletons from Phase 0).
2. Ingest a real, legally-sourced dataset of Hyderabad SWE/AI-ML companies and
   open roles via the `JobProvider` port (ADR 0002).
3. Persist companies, opportunities, and geolocation in Postgres/PostGIS
   (first real schema + first Alembic migrations in the repo).
4. Ship an anonymous, map-first web experience: nearby companies, search by
   role and by location, company cards, and a company detail page.
5. Give each company a structured, factual **Company Intelligence** profile
   (size, funding stage, tech stack, founding year, growth signal) —
   descriptive facts only, not a score or a recommendation.
6. Keep the OpenAPI contract (ADR 0008) and import-linter boundaries (ADR
   0001) green throughout — this is the first phase where `contract.py` files
   stop being empty, so it's the first real test of those guardrails under
   load.

## Non-goals (explicitly out of scope for Phase 1)

Per `docs/product/mvp-scope.md` and the blueprint roadmap (§6), the following
are **not** part of this slice, regardless of how tempting they are to bolt
on while touching adjacent code:

- **Career Universe** (Phase 2) — no alternate visualization; Phase 1 ships
  the map only. The data model is designed so Phase 2 can reuse it unchanged.
- **Career Intelligence Engine** (Phase 3) — no matching, ranking, scoring,
  salary, skill-gap, or commute engines. "Company Intelligence" here means a
  static factual profile, never a computed score or recommendation.
- **Identity/Auth** (Phase 4) — everything in this spec is Core-tier,
  anonymous, and unauthenticated (ADR 0004). No accounts, no saved searches.
- **Resume Intelligence** (Phase 5), **Career GPS** (Phase 6), **Polaris**
  (Phase 7) — no resume upload, no salary/career-path engines, no AI
  assistant or LLM calls anywhere in this slice.
- **Multiple cities or verticals** — Hyderabad + SWE/AI-ML only.
- **Employer- or user-submitted listings** — ingestion sources 4–5 (ADR 0002)
  stay deferred; only official career pages / public ATS providers this
  phase.
- **D3 or physics-based visualization** — Mapbox + standard React only.

## Personas

Drawn from the PRD's MVP-narrowed audience (Hyderabad, SWE/AI-ML):

1. **Anonymous Active Explorer** — a software engineer or AI/ML practitioner
   in Hyderabad casually browsing what's nearby before deciding whether to
   make a move. Wants a fast, honest picture of the local market — not another
   portal to register on.
2. **Final-Year Student** — a CS/AI student surveying the Hyderabad tech
   landscape ahead of placements. Wants to understand *which companies exist
   near college/home* and *what they're like*, not just a list of postings.
3. **Relocating Professional** — an engineer considering a move to Hyderabad
   from elsewhere. Wants a geographic, honest sense of where the opportunity
   density actually is before committing to a city.

All three are anonymous by definition in this phase — there is no
authenticated persona yet (Phase 4).

## User Stories

Organized by the five delivery slices; each is independently demoable per the
Development Strategy (spec → review → implementation → verification → docs →
commit, one slice at a time).

### Slice 1 — Company Foundation
- As an anonymous visitor, I want companies to have a real, structured
  identity (name, industry, description, website, careers page) so that a
  company card or detail page has something real to show.
- As a future phase (Career Universe, CIE), I want `companies.contract` to
  expose stable, typed read models so I can build on it without touching
  `companies` internals.

### Slice 2 — Opportunity Foundation
- As an anonymous visitor, I want to see open roles tied to a real company,
  with role title, seniority, employment type, and a link to apply, so
  browsing a company feels concrete rather than abstract.
- As the platform, I want every opportunity to carry provenance (which
  provider, which source URL, when fetched) so legal/source traceability
  (ADR 0002) holds from day one.
- As the platform, I want two postings for the same role from two sources to
  collapse into one canonical opportunity (dedup), so the dataset doesn't
  double-count.

### Slice 3 — Seed Hyderabad Dataset
- As an anonymous visitor, I want the map and search to show *real* Hyderabad
  companies and roles (not placeholders), so the product feels credible on
  first use.
- As the platform, I want the seed dataset sourced only from official career
  pages / public ATS providers (ADR 0002), so there is no legal exposure and
  no dependency on scraping prohibited sites.

### Slice 4 — Map Experience
- As an anonymous visitor, I want to see nearby companies plotted on a real
  map centered on a location I choose, so I immediately grasp "where are the
  opportunities near me."
- As an anonymous visitor, I want to search by role (e.g. "backend engineer")
  and by location (e.g. a neighborhood or landmark) and see the map/list
  update, so I can narrow down without a job-board-style keyword box.
- As an anonymous visitor, I want a company card (from the map or a list) to
  open a full company detail page, so I can go from "where" to "what."

### Slice 5 — Company Intelligence
- As an anonymous visitor, I want a company's detail page to show factual
  signals (team size bucket, funding stage, founding year, tech stack, growth
  signal) so I can judge fit for myself, without the platform telling me what
  to think.
- As the platform, I want these fields to be explicitly factual/static data
  (not a computed score), so Facts-First (ADR 0005) isn't quietly violated by
  a "Company Intelligence" feature that sounds like it belongs to the CIE
  (which doesn't exist until Phase 3).

## Acceptance Criteria

**Slice 1 — Company Foundation** ✅ Complete — see `docs/roadmap/phase-1.md`.
- `companies.contract` exposes typed `CompanyId`, `CompanySummary`,
  `CompanyDetail` (or equivalent) — no other context or the API layer reaches
  into `companies.domain`/`application`/`infrastructure` directly.
- Company domain entity and value objects are unit-tested without a live DB.
- import-linter's two contracts still pass with `companies` now non-empty.

**As implemented:** `CompanyId` (stable UUID identity) and `CompanySlug`
(mutable, SEO-friendly) are separate value objects from the start — refined
per review before Slice 1 began (see `contexts/companies/CLAUDE.md`). The API
layer talks to the application layer's `Result`-based use cases directly
(`GET /companies`, `GET /companies/{company_id}`), per the blueprint's
Router → Application → Domain diagram. `contract.py` exposes the `CompanyId`/
`CompanySummary`/`CompanyDetail` read models and a `CompanyReader` Protocol as
required by this slice's acceptance criteria — but per the Slice Boundary
Review before merge, the **concrete** `SqlAlchemyCompanyReader` adapter was
removed: it had zero callers this slice (no cross-context consumer exists
until Slice 2's `opportunities`), so shipping it now would have been a
speculative abstraction. It will be (re)implemented in
`companies/infrastructure/` in Slice 2, when there's a real caller to prove
it against. This slice also stood up the first real DB dependency
(SQLAlchemy/Alembic/psycopg), the first migration, and the new CI `database`
job — see `docs/database/schema-overview.md`.

**Slice Boundary Review (pre-merge, via `architecture-guardian`):** all new
files confirmed to belong to either `companies` or infrastructure/platform;
no future-phase functionality (geo, opportunities, seed/ingestion, map UI,
Company Intelligence fields) leaked into this slice; `Company` holds only
plain factual identity fields; zero imports from `career_intelligence`,
`resume`, `polaris`, `identity`, `profile`, `engagement`, or `career_gps`
anywhere in the diff, mechanically confirmed by `lint-imports` (2 contracts
kept, 0 broken). One CONCERN raised (the unused `SqlAlchemyCompanyReader`)
was resolved by removing it, as above.

**Slice 2 — Opportunity Foundation**
- `opportunities.contract` exposes typed `OpportunityId`, `OpportunitySummary`
  read models referencing `CompanyId` (from `companies.contract`) — never a
  raw foreign key crossing the contract boundary.
- A `JobProvider` implementation exists in `contexts/ingestion/providers/`
  producing the canonical Opportunity schema; provenance (source, source URL,
  fetched_at) is present on every record.
- A dedup rule collapses same-role/same-company postings from two sources
  into one canonical opportunity; covered by a unit test with two synthetic
  sources.

**Slice 3 — Seed Hyderabad Dataset**
- Running the seed produces ≥ 15 real Hyderabad companies (SWE/AI/ML) and
  their currently-open roles, each traceable to an official source URL.
- Every seeded company has a resolvable geolocation (lat/lng in Hyderabad).
- Re-running the seed is idempotent (no duplicate rows on re-run).

**Slice 4 — Map Experience**
- `GET /companies/nearby?lat=&lng=&radius_km=` returns companies within
  radius, ordered by distance, backed by a PostGIS `ST_DWithin`/GIST-indexed
  query.
- `GET /companies/search?role=&location=` returns companies/opportunities
  matching a free-text role and a location term.
- `apps/web` `(public)` route renders the map (Mapbox), plots real
  results, and supports the two search paths above with no auth required.
- Company card → company detail page navigation works with no console errors
  and passes the existing accessibility bar (`apps/web/CLAUDE.md`: semantic
  HTML, keyboard-complete, labeled controls, AA contrast).
- OpenAPI regenerates with zero drift (`pnpm contracts:generate` +
  `git diff --exit-code`).

**Slice 5 — Company Intelligence**
- Company detail page renders team-size bucket, funding stage, founding year,
  tech stack, and a growth signal, sourced from stored, factual fields — no
  field is LLM-generated or engine-computed in this phase.
- `docs/product/mvp-scope.md`-style language check: no UI copy implies a
  recommendation, ranking, or match score (that's Phase 3's CIE).

**Cross-slice (every slice)**
- `ruff`, `black --check`, `mypy --strict`, `lint-imports`, `pytest` (backend)
  and `prettier`, `tsc --noEmit`, `eslint`, `vitest` (frontend) all pass.
- `scripts/verify-phase0.sh`-equivalent full gauntlet stays green (extended
  with the first Alembic migration check per the blueprint §7 footnote — see
  Risks).
- Each slice's own docs/ADR (if architecture actually changes) land in the
  same commit — Living Documentation DoD.

## Domain Model

All three contexts already exist as Phase 0 skeletons
(`apps/api/src/northstar/contexts/{companies,opportunities,geo}/`, each with
empty `contract.py` + empty `domain/`·`application/`·`infrastructure/`). This
phase fills them in — no new contexts, no new import-linter contracts.

### `companies` (Core tier)
- **Domain:** `Company` entity — `id: CompanyId`, `name`, `description`,
  `industry`, `website`, `careers_page_url`, `founded_year`,
  `team_size_bucket` (enum: e.g. `1-10`/`11-50`/`51-200`/`201-500`/`500+`),
  `funding_stage` (enum: `bootstrapped`/`seed`/`series_a`.../`public`),
  `tech_stack: list[str]`, `growth_signal` (enum: `hiring`/`stable`/`unknown`
  — a static, human-curated tag, not a computed score).
- **Value objects:** `CompanyId` (typed identifier, not a raw int/UUID leaking
  across the contract).
- **Application:** use cases — `get_company(id)`, `list_companies(filter)`,
  `search_companies(role, location)`.
- **Infrastructure:** SQLAlchemy repository over the `companies` table.
- **Contract surface:** `CompanyId`, `CompanySummary` (card-sized read model),
  `CompanyDetail` (full profile, including the Slice-5 intelligence fields).

### `opportunities` (Core tier)
- **Domain:** `Opportunity` entity — `id: OpportunityId`, `company_id:
  CompanyId` (imported via `companies.contract`, never a bare foreign key),
  `title`, `seniority` (enum), `employment_type` (enum: `full_time`/
  `internship`/…), `skills: list[str]`, `apply_url`, `posted_at`, `status`
  (`open`/`closed`), and a `Provenance` value object (`source_provider`,
  `source_url`, `fetched_at`).
- **Application:** `list_opportunities_for_company(company_id)`,
  `search_opportunities(role, location)`, and the **dedup** use case that
  collapses provider duplicates into one canonical record.
- **Infrastructure:** SQLAlchemy repository; adapters for the `JobProvider`
  port implementations live in `contexts/ingestion/providers/`, not here —
  `opportunities` only knows the canonical schema, never a provider's shape
  (ADR 0002).
- **Contract surface:** `OpportunityId`, `OpportunitySummary`.

### `geo` (Core tier, platform-adjacent)
- **Domain:** `GeoPoint` value object (lat/lng), `NearbyQuery` (origin +
  radius), `NearbyResult`.
- **Application:** `find_nearby(origin, radius_km, candidate_ids)` — takes
  candidate `CompanyId`s (from `companies`) and returns them ordered by
  distance; `geo` does not know what a "company" is, only points and
  distances, keeping the independence contract clean.
- **Infrastructure:** PostGIS-backed repository (`ST_DWithin`, GIST index);
  this is the first context to actually use `platform/geo/` (currently an
  empty Phase-0 placeholder) for shared geometry helpers if any are needed
  across contexts.
- **Contract surface:** `GeoPoint`, `NearbyQuery`, `NearbyResult`.

### `ingestion` (existing extension point, ADR 0002)
- New provider under `providers/` (name TBD at implementation time, e.g.
  `providers/hyderabad_seed/` or a named ATS provider if one is used) —
  implements `JobProvider`, maps raw source data to the canonical Opportunity
  shape consumed by `opportunities`. No change to `opportunities`' internals
  is needed to add this provider (additive extensibility, ADR 0002).

No cross-context edge in this phase needs anything beyond what's already
modeled: `opportunities` → `companies.contract` (for `CompanyId`/summary
lookups when composing a response), API routers → all three contracts. Every
edge is contract-only, per ADR 0001.

## Database Changes

This is the **first Alembic migration** in the repository — Phase 0 had no DB
models. Concretely:

- `companies` table — matches the `Company` domain fields above; `id` as
  primary key (`CompanyId`-backed UUID or surrogate int, decided at
  implementation).
- `company_locations` table (or a `geography(Point, 4326)` column directly on
  `companies`, decided at implementation) — PostGIS geography point + a GIST
  index, used by `geo`'s nearby query.
- `opportunities` table — matches the `Opportunity` domain fields; foreign
  key to `companies.id` at the **database** level is acceptable (it's one
  physical DB), but application code still only ever reaches `companies` via
  its contract, never by joining across contexts in code.
- `opportunity_provenance` (either a table or JSON column on `opportunities`)
  — `source_provider`, `source_url`, `fetched_at`, used for the dedup rule and
  ADR 0002's provenance requirement.

**CI implication:** per the blueprint §7 footnote ("a DB migration check is
added when the first Alembic migration lands"), this phase must also add that
migration-check step to `.github/workflows/ci.yml` — flagged explicitly in
Risks below so it isn't missed.

## API Changes

New routers under `apps/api/src/northstar/api/routers/` (thin HTTP layer per
blueprint §4.1 — no business logic in the router itself):

- `companies.py` — `GET /companies`, `GET /companies/{id}`,
  `GET /companies/nearby`, `GET /companies/search`.
- `opportunities.py` — `GET /opportunities`, `GET /companies/{id}/opportunities`.

All request/response schemas are Pydantic models in `api/schemas/` (or
inline, per existing convention), which FastAPI turns into the OpenAPI
document. Per ADR 0008: after any endpoint change, run
`pnpm contracts:generate`; the regenerated `packages/api-contracts/{openapi.json,
schema.ts}` are committed in the same PR, and CI's contract-drift check
(`git diff --exit-code`) is the enforcement, not a manual promise.

## UI Flow

`apps/web/src/app/(public)/` (anonymous, per ADR 0004 — no auth anywhere in
this phase):

1. **Explore** (`/explore` or similar) — Mapbox map centered on Hyderabad,
   plots nearby companies from `GET /companies/nearby`; a search bar with two
   inputs (role, location) driving `GET /companies/search`; results update
   both the map and an adjacent list of **company cards**.
2. **Company card** (`features/company-intelligence/` presentational
   component) — logo/name, industry, one-line description, distance from
   search origin; click-through to detail.
3. **Company detail** (`/companies/[id]`) — full profile: description,
   website/careers links, open opportunities (from
   `GET /companies/{id}/opportunities`), and the Slice-5 Company Intelligence
   block (team size, funding stage, founded year, tech stack, growth signal).

Per `apps/web/CLAUDE.md`: business-specific UI lives in `features/{map,
company-intelligence}/`, not in `packages/ui`; only generated API types from
`packages/api-contracts` are consumed; Framer Motion used sparingly (e.g. map
marker hover, not spectacle); accessibility (keyboard-complete map controls,
labeled search inputs, AA contrast) is a Definition-of-Done item, not a
follow-up.

## Testing Strategy

- **Unit (backend, pytest):** `Company`, `Opportunity`, `GeoPoint`/`NearbyQuery`
  domain logic and application use cases tested against in-memory
  repositories/ports — no live DB required, per `apps/api/CLAUDE.md`. Dedup
  logic gets a dedicated test with two synthetic provider records.
- **Integration (backend, pytest + Docker Compose):** the PostGIS nearby-query
  path (`ST_DWithin` + GIST index) tested against a real Postgres+PostGIS
  instance — this is the one place a real DB is necessary, since geometry
  correctness can't be faithfully faked in-memory.
- **Contract (ADR 0008):** `pnpm contracts:generate` + `git diff --exit-code`
  on every API-shape change; existing CI job, no new tooling needed.
- **Boundary (ADR 0001):** `lint-imports` run after every slice — this is the
  first phase where the two contracts have real content to check, not empty
  skeletons; a failure here would be the first genuine post-Phase-0 signal
  that the guardrail matters in practice.
- **Frontend (Vitest):** company card, search inputs, and map-wrapper
  components unit-tested in isolation.
- **E2E (Playwright):** anonymous flow — load `/explore`, search by role,
  search by location, click a company card, land on detail page — with zero
  auth in the flow, proving ADR 0004 holds for the very first real feature.
- **Seed idempotency:** a test/script assertion that re-running the Slice-3
  seed does not duplicate companies or opportunities.

## Risks

| Risk | Mitigation |
|---|---|
| First Alembic migration also means the first new CI gate (migration check) — easy to forget per the blueprint §7 footnote. | Call it out explicitly as a Slice-1/2 deliverable, not an afterthought; add to `.github/workflows/ci.yml` in the same PR as the first migration. |
| "Company Intelligence" naming invites scope creep toward AI-generated insight or a computed score, which would quietly violate Facts-First (ADR 0005) before the CIE (Phase 3) exists. | Explicitly scope Slice 5 to static, human-curated/sourced fields only; acceptance criteria include a copy check for recommendation-sounding language; `architecture-guardian` review before merge. |
| Legal/source risk in the seed dataset if provenance is sloppy. | Every seeded opportunity must carry a resolvable `source_url` from an official career page or public ATS; enforced by the ingestion provider's schema, not a manual promise (ADR 0002). |
| PostGIS nearby-query performance/correctness is new territory (Phase 0 only verified PostGIS *exists*, never a real geometry query). | Integration test against real Postgres+PostGIS (see Testing Strategy); GIST index from the first migration, not retrofitted. |
| Cross-context coupling creep — e.g. `opportunities` reaching into `companies.domain` for convenience instead of `companies.contract`. | import-linter now has real content to check for the first time since Phase 0; treat any red run here as a stop-the-line signal, not a lint nuisance. |
| Mapbox usage/cost and API-key handling. | Token from env only (`NORTHSTAR_`-prefixed, per ADR 0003); Mapbox is a frontend UI dependency, not a backend vendor SDK — doesn't touch domain/application layers. |
| Five-slice scope is large for "never implement multiple slices simultaneously." | Strict sequential execution per slice, each with its own spec-review-implement-verify-doc-commit cycle; this document covers the whole phase's shape, but implementation proceeds one slice at a time. |

## Rollout Plan

> **Execution order revised after Slice 1 (2026-07-14).** Same five slices,
> same architecture, no new contexts, no ADR change — only the sequence
> changed, to put a visible "Google Maps for Careers" product moment on
> screen as early as possible rather than last. New order:
>
> 1. Company Foundation ✅ complete
> 2. Seed Hyderabad Dataset
> 3. Map Experience
> 4. Opportunity Foundation
> 5. Company Intelligence
>
> **Consequence of reordering (content, not architecture, shifts):**
> Opportunity now lands *after* Map Experience instead of before it, so:
> - **Seed Hyderabad Dataset (now Slice 2)** seeds only `companies` +
>   geolocation for each — no opportunities/roles yet, since `opportunities`
>   doesn't exist until Slice 4. This also means Location (refinement #3 from
>   Slice 1 review) is introduced here rather than in Map Experience — Slice
>   2 is where geolocation data first enters the system, Slice 3 is where
>   it's queried and displayed. See the dedicated
>   `docs/features/phase1/slice-2-seed-hyderabad-dataset.md` spec.
> - **Map Experience (now Slice 3)** ships nearby-company map + company cards
>   + company detail page, and search **by location only** — search **by
>   role** is dropped from this slice's scope (there's no `Opportunity` to
>   search yet) and returns once Slice 4 lands.
> - **Opportunity Foundation (now Slice 4)** absorbs seeding real Hyderabad
>   job postings for the already-seeded companies (previously bundled into
>   the old Slice 3), since there's no other slice left to do it in.
> - **Company Intelligence (Slice 5)** is unaffected — still last, still
>   additive to `CompanyDetail`.

Sequential, one slice at a time, each independently demoable, spec'd and
approved before implementation, and committed separately (per the
Development Strategy in the kickoff brief):

1. **Slice 1 — Company Foundation** ✅ complete: domain + contract +
   persistence + `GET /companies`/`GET /companies/{id}`. No UI yet beyond a
   raw JSON/Swagger check.
2. **Slice 2 — Seed Hyderabad Dataset** ✅ complete: `Location` value object,
   `geo`'s first persistence, idempotent seed of 30 real Hyderabad companies
   (well-distributed across all seven named localities) with resolvable
   coordinates. Spec: `docs/features/phase1/slice-2-seed-hyderabad-dataset.md`.
3. **Slice 3 — Map Experience** ✅ complete: the product's identity moment —
   anonymous map + nearby-company query + custom career-node markers +
   company cards + detail page/deep-link + search by location, all backed by
   real seeded data. Spec: `docs/features/phase1/slice-3-map-experience.md`.
4. **Slice 4 — Opportunity Foundation:** domain + contract + dedup +
   `JobProvider` port + a real seed of Hyderabad job postings for the
   existing companies; search by role becomes possible from here.
5. **Slice 5 — Company Intelligence:** enriches the Slice-1 `Company` model
   and the Slice-3 detail page with factual profile fields.

Each slice ends with: passing tests, zero contract drift, `lint-imports`
green, updated docs (this spec's relevant section reconciled with
as-implemented reality, mirroring how the blueprint's own change log works),
and a commit — mirroring the Phase 0 milestone discipline
(`docs/project-history.md`). No feature flags are needed: everything here is
Core-tier and anonymous, so there's no auth-gate to stage behind.

## Future Extensions

Explicitly deferred, to return only via a new ADR when user value justifies
it (per `docs/product/mvp-scope.md`'s deferral policy):

- **Career Universe (Phase 2)** reuses the exact `companies`/`opportunities`/
  `geo` canonical data this phase produces — no new data pipeline, a second
  presentation layer only.
- **Career Intelligence Engine (Phase 3)** — Commute, Company Scoring, and
  Ranking engines will consume `companies.contract`/`geo.contract` read
  models as their inputs; this phase's `CompanyDetail`/`NearbyResult` shapes
  are designed to be engine-input-friendly without modification.
- **Additional ingestion providers** (Greenhouse, Lever, Ashby, Workable,
  SmartRecruiters) — additive, per ADR 0002; the Slice-2 `JobProvider` port
  is built to accept them without touching `opportunities` internals.
- **Other cities/verticals** — same domain model, different seed data and a
  new ADR when justified.
- **Employer-/user-submitted listings** — ingestion sources 4–5, deferred
  until legal/product justification exists.
