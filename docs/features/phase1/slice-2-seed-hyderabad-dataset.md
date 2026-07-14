# Phase 1, Slice 2 — Seed Hyderabad Dataset (Feature Specification)

> **Status:** Approved and complete. Implemented, verified live against
> Postgres+PostGIS, Slice-Boundary-reviewed (7/7 checks passed) — see
> `docs/roadmap/phase-1.md`'s Slice 2 section for full results. Seed target
> was refined from ≥15 to ~25–50 companies before implementation; shipped
> with 30, distributed across all seven requested localities (Madhapur,
> Hitech City, Gachibowli, Financial District, Kondapur, Raidurg,
> Nanakramguda). Parent spec: `docs/features/phase1/hyperlocal-career-navigation.md`.
> Traces to `docs/product/prd.md` and `docs/product/mvp-scope.md`. Builds
> inside ADRs 0001–0009 — introduced no new context, no new import-linter
> contract, no ADR change.

## Vision

Slice 1 gave the platform a real `Company` aggregate with nowhere to point
on a map. This slice gives every seeded company a real place in Hyderabad —
so Slice 3 (Map Experience) has real, geolocated data to plot on day one
instead of a placeholder. This is the slice that makes the eventual map
*true*, not just present.

## Problem Statement

`companies` (Slice 1) can persist a company's identity and facts, but has no
concept of *where* a company is. There is no `geo` capability yet — Phase 0
shipped PostGIS running, but no schema, no `Location` value object, and no
real data. Without this slice, Map Experience (Slice 3) would have nothing
real to query or display. This slice must: (1) introduce `Location` as a
first-class value object (refinement carried over from the Slice 1 review),
(2) give the `geo` context its first real schema and persistence, and (3)
seed ~25–50 well-distributed real Hyderabad SWE/AI-ML companies (refined from
an initial ≥15 target before implementation), each with a resolvable
coordinate — with **no** `Opportunity` modeling yet, since Opportunity
Foundation now runs *after* Map Experience in the revised order.

## Goals

1. Introduce `Location` (a `GeoPoint`-style value object: latitude,
   longitude, both validated to plausible ranges) as a first-class concept in
   the `geo` context — never raw floats passed around ad hoc.
2. Give `geo` its first real persistence: a table associating a `CompanyId`
   with a `Location`, using PostGIS's `geography(Point, 4326)` type and a
   GIST index (schema-ready for Slice 3's nearby query, even though the
   query itself isn't built yet).
3. Seed ~25–50 real Hyderabad companies, well-distributed across Madhapur,
   Hitech City, Gachibowli, Financial District, Kondapur, Raidurg, and
   Nanakramguda (reusing Slice 1's `Company` aggregate and repository
   unchanged), each with enough metadata for a future Company Card (name,
   description, industry, website — all Slice-1 fields, no schema change
   needed) and a real, resolvable Hyderabad coordinate. Quality over
   quantity: prefer fewer, well-curated real companies over padding the count.
4. Keep the seed's data-loading step decoupled from its persistence step, so
   swapping the static seed list for a real data source later (a company
   directory API, a CSV import, anything) never requires touching
   `companies`/`geo` application or infrastructure code — only the loader.
5. Make the seed idempotent — re-running it must not duplicate companies or
   locations.

## Non-goals (explicitly out of scope for this slice)

- **`Opportunity` modeling or seeding** — no roles, no postings, no
  `JobProvider` port work. That's Slice 4 (Opportunity Foundation) in the
  revised order. This slice seeds companies and locations only.
- **The nearby-company query, Mapbox, or any UI** — that's Slice 3 (Map
  Experience). This slice only makes the *data* real; nothing renders yet.
- **Multiple offices per company** — one `Location` per company (treated as
  its primary/HQ location) for MVP simplicity. Multi-office modeling is a
  future additive extension, not blocked by anything built here.
- **A generalized ingestion-provider abstraction** — see "Seed pipeline
  design" below for why this slice deliberately does *not* introduce a new
  port/protocol.
- **Company Intelligence fields** — team size, funding stage, tech stack,
  growth signal remain Slice 5.

## Personas

Unchanged from the parent spec (Anonymous Active Explorer, Final-Year
Student, Relocating Professional) — this slice has no user-facing surface,
but it's the data those personas will see rendered in Slice 3.

## User Stories

- As the platform, I want every company to have a real, resolvable Hyderabad
  coordinate, so Slice 3's map has real data to plot rather than a
  placeholder.
- As a future maintainer, I want the seed's data source cleanly separated
  from how it's persisted, so swapping a static list for a real data feed
  later doesn't touch `companies` or `geo` application/infrastructure code.
- As the platform, I want re-running the seed to be a no-op on already-seeded
  data, so it's safe to run repeatedly in local dev without manual cleanup.

## Acceptance Criteria

- `geo.contract` exposes a `Location` (or `GeoPoint`) value object — latitude
  `[-90, 90]`, longitude `[-180, 180]`, validated at construction.
- A new table (owned by `geo`'s infrastructure) stores `company_id` (FK to
  `companies.id`) + a PostGIS `geography(Point, 4326)` column + a GIST index.
  No column is added to the `companies` table itself — location stays out of
  the `Company` aggregate, per `contexts/companies/CLAUDE.md`.
- Running the seed produces ~25–50 real Hyderabad companies (SWE/AI/ML),
  well-distributed across all seven named localities, each with a location
  row resolving to real Hyderabad coordinates (validated by a sanity
  bounding-box check around Hyderabad, not just "some lat/lng"). Each company
  also carries the Slice-1 fields (name, description, industry, website,
  careers page, founded year where known) — sufficient metadata for a future
  Company Card without a schema change — but this is not "seed
  opportunities," so no roles are attached.
  **As implemented:** 30 companies shipped (Gachibowli 5, Raidurg 5, Madhapur
  4, Hitech City 4, Financial District 4, Kondapur 4, Nanakramguda 4).
- Every seed record's source is a real, resolvable reference (e.g. the
  company's own website/public profile) — not fabricated data — consistent
  with the spirit of ADR 0002 (legal, traceable sourcing) even though no
  `JobProvider` exists yet.
- Re-running the seed script twice produces the same row counts both times
  (idempotent — upsert or skip-if-exists by slug, not insert-always).
- `lint-imports` stays green: the seed script may import `companies` and
  `geo` internals directly (it's not a bounded context, it's a script in
  `apps/api/scripts/` or similar — same category as
  `scripts/export_openapi.py`), but `companies` and `geo` still only reach
  each other, if at all, via contract.
- Cross-slice: `ruff` / `black --check` / `mypy --strict` / `lint-imports` /
  `pytest` all pass; `alembic upgrade head` + `alembic check` green for the
  new migration; full verification gauntlet stays green.

**As implemented / verified live (not just claimed):** ran the seed against
real Postgres+PostGIS twice — first run: 30 created, 0 skipped; second run: 0
created, 30 skipped, proving idempotency rather than asserting it. All 30
coordinates verified inside a Hyderabad bounding box via a live SQL check; a
sample `ST_DWithin` query around Gachibowli returned 21 companies within
3km, proving the geography column is genuinely queryable. Two real bugs
surfaced only by running things: (1) geoalchemy2's `Geography(spatial_index=True)`
auto-creates its GIST index via a table-creation event, which collided with
Alembic's own autogenerated explicit `create_index` call — fixed by removing
the duplicate (see `docs/database/schema-overview.md`); (2) one seed record's
`founded_year` (1792) violated `Company`'s own domain validation
(`[1800, 2100]`) — fixed by nulling that field rather than loosening the
Slice 1 rule. Slice Boundary Review (`architecture-guardian`): 7/7 checks
passed; see `docs/roadmap/phase-1.md` for full detail, including one
non-blocking note about the seed script bypassing `companies.contract` for
writes (pre-authorized by this spec; worth revisiting if Slice 4 repeats it).

## Domain Model

### `geo` (Core tier) — first real content this slice

- **Domain:** `Location` value object — `latitude: float`, `longitude:
  float`, validated ranges in `__post_init__` (mirrors the pattern already
  used for `CompanyId`/`CompanySlug` in `companies/domain/value_objects.py`).
- **Application:** `SetCompanyLocation` (persist a `Location` for a
  `CompanyId`), `GetCompanyLocation` (read it back) — deliberately minimal;
  the nearby-query use case (`find_nearby`) is Slice 3's job, not this
  slice's.
- **Infrastructure:** SQLAlchemy model + repository for the new
  `company_locations` table (PostGIS geography column). This is the context's
  first infrastructure code — same pattern as `companies`' Slice 1 buildout.
- **Contract surface:** `Location` (or `GeoPoint`), and a narrow
  `CompanyLocationReader`-style read accessor if Slice 3 needs one — kept as
  small as Slice 1's `CompanyReader` was, and only built if there's an actual
  caller (learned from the Slice 1 Boundary Review: no unused adapters).

### `companies` — unchanged

No changes to `Company`, `CompanyId`, `CompanySlug`, or `companies.contract`.
This slice only *adds rows* via the existing repository — it doesn't touch
the aggregate's shape. Confirms the extensibility design from Slice 1 (new
capability arrives without redesigning `Company`).

## Database Changes

Second Alembic migration in the repository:

- `company_locations` table: `company_id` (FK → `companies.id`), `location`
  (`geography(Point, 4326)`), `created_at`/`updated_at`. GIST index on
  `location` (schema-ready for Slice 3's `ST_DWithin` query; the query itself
  isn't written this slice).
- No changes to the `companies` table.
- `alembic check` must stay green (mirrors Slice 1's CI gate).

## API Changes

**None.** This slice has no new endpoint — it's a data-only slice (seed
script + underlying persistence). `GET /companies`/`GET /companies/{id}`
responses are unchanged; no contract regeneration is expected unless a
decision is made to surface location on `CompanyDetail` early (not planned —
that's naturally Slice 3's job, once there's a query to serve it).

## UI Flow

**None.** No page, no component. First UI arrives in Slice 3.

## Seed pipeline design (refinement: evolvable into provider-based ingestion)

The seed is a script (e.g. `apps/api/scripts/seed_hyderabad_companies.py`)
with two cleanly separated steps:

1. **Load** — read a static, structured list of Hyderabad companies (name,
   description, industry, website, careers page, founded year, lat/lng) from
   a local data file (e.g. `apps/api/scripts/data/hyderabad_companies.json`).
2. **Persist** — for each record, call `companies`' existing application
   layer (`Company.create(...)` + repository) and `geo`'s new
   `SetCompanyLocation` use case. No new port/protocol is introduced for
   this.

This deliberately does **not** introduce a `JobProvider`-style abstraction
now: ADR 0002's `JobProvider` port is specifically for ingesting
*Opportunities* (job postings), and there are no opportunities yet in this
slice — inventing a parallel "company source" port before there's a second
real source to justify it would violate Simplicity. The evolution path the
review asked for is satisfied structurally: the **Load** step is the only
part that would change if a real data source replaced the static list (a
company-directory API, a CSV import) — **Persist** already goes through the
same `companies`/`geo` application-layer calls a future automated source
would use. When Slice 4 (Opportunity Foundation) introduces real
`JobProvider` adapters for actual job postings, this same separation
(load raw records → persist via existing application use cases) is the
pattern to repeat, not a new one to invent.

## Testing Strategy

- **Unit:** `Location` value-object validation (rejects out-of-range
  lat/lng); `SetCompanyLocation`/`GetCompanyLocation` use cases against an
  in-memory fake repository — no DB required, matching Slice 1's pattern.
- **Integration:** the new migration applies cleanly to a real
  Postgres+PostGIS instance (`alembic upgrade head`); a real row round-trips
  through the PostGIS geography column correctly (insert a known
  lat/lng, read it back, confirm it matches).
- **Seed idempotency:** running the seed script twice against a real
  database produces identical row counts both times — an explicit test, not
  just a manual check (mirrors the acceptance criterion).
- **Boundary:** `lint-imports` after the change — `geo` remains independent
  of every context except via contract, matching Slice 1.

## Risks

| Risk | Mitigation |
|---|---|
| Real coordinates for 15+ companies must actually be correct (wrong coordinates would make Slice 3's map look broken or dishonest). | Sanity-check each seeded coordinate falls within a Hyderabad bounding box as part of the seed script itself, not just eyeballed. |
| Temptation to also seed placeholder opportunities "since we're here" — reintroducing Slice 4 scope early. | Explicit non-goal above; Slice Boundary Review (same as Slice 1) checks for this before merge. |
| PostGIS geography column correctness untested until Slice 3 actually queries it. | Integration test round-trips a known coordinate through the column now, rather than waiting until Slice 3 to discover a storage bug. |
| Static seed data going stale (companies close, career pages change) is a real but low-urgency risk for a one-time MVP seed. | Not mitigated in this slice — acceptable for now; revisit if/when re-seeding cadence becomes a real product need. |

## Rollout Plan

Single slice, single migration, single commit — same discipline as Slice 1:
spec (this document) → approval → implementation → verification → docs →
Slice Boundary Review → commit → tag `phase1-slice2`.

## Future Extensions

- **Slice 3 (Map Experience)** builds `find_nearby` on top of the
  `company_locations` table this slice creates, plus the Mapbox UI.
- **Slice 4 (Opportunity Foundation)** will seed real Hyderabad job postings
  for these same companies, using the same load/persist separation pattern
  established here, likely via a real `JobProvider` adapter at that point.
- **Multiple offices per company** — if a company's Hyderabad presence
  turns out to need more than one point (e.g. multiple campuses), that's an
  additive change to `geo` (more rows per `CompanyId`), not a redesign.
