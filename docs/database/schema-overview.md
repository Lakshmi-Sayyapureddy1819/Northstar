# Database Schema — Overview & Migration Strategy

> First populated in Phase 1, Slice 1 (Company Foundation) — the repository's
> first real tables and first Alembic migration. Phase 0 shipped Postgres +
> PostGIS + pgvector running (ADR 0003) but with zero application schema.

## Migration tool: Alembic

- Config: `apps/api/alembic.ini` + `apps/api/alembic/env.py`.
- `env.py` reads the DB URL from `Settings.database_url` (env-only, ADR 0003)
  — never a hardcoded value in `alembic.ini`.
- `target_metadata = Base.metadata` (`platform/db/session.py`); every
  context's SQLAlchemy models are imported explicitly in `env.py` so
  `--autogenerate` can see them. One import line per context as its
  infrastructure models land — `env.py` is the one place allowed to know all
  contexts' models exist (everywhere else, contexts stay independent).
- Commands (from `apps/api/`): `uv run alembic revision --autogenerate -m "..."`,
  `uv run alembic upgrade head`, `uv run alembic check` (fails if models drifted
  from the latest migration — the DB analogue of the API contract-drift check).

### PostGIS/pgvector system tables are excluded from autogenerate

PostGIS installs `spatial_ref_sys` (and pgvector installs its own extension
objects) directly into the database, outside SQLAlchemy's metadata. Without
a filter, `--autogenerate` proposes dropping them on every revision. `env.py`
defines `include_object()` to exclude known extension-owned tables
(`_POSTGIS_SYSTEM_TABLES`) from comparison — extend that set if a future
extension adds more system tables.

## CI gate (blueprint §7 footnote)

The blueprint's Phase-0 footnote noted: *"a DB migration check is added when
the first Alembic migration lands."* This is that migration, so
`.github/workflows/ci.yml` gained a `database` job:

1. Spins up a `postgis/postgis:16-3.4` service container (matches Postgres 16
   + PostGIS from `infra/compose/`; pgvector isn't in this image — add it back
   to the CI service only once a migration actually needs a vector column).
2. `uv run alembic upgrade head` against a clean database — proves migrations
   apply from empty, not just incrementally on a dev DB that's drifted.
3. `uv run alembic check` — fails the build if a model change wasn't captured
   in a migration, mirroring the API contract-drift job (ADR 0008) for the
   database.

## Tables

### `companies` (Slice 1 — Company Foundation)

Backs the `Company` aggregate root (`contexts/companies/domain/company.py`).
See `contexts/companies/CLAUDE.md` for why `id` and `slug` are separate
columns rather than one.

| Column | Type | Notes |
|---|---|---|
| `id` | `uuid` (PK) | Stable identity (`CompanyId`). Never reused, never derived from mutable data. |
| `slug` | `varchar(255)`, unique, indexed | SEO-friendly, mutable. Not identity. |
| `name` | `varchar(255)` | |
| `description` | `text` | |
| `industry` | `varchar(255)` | |
| `website` | `varchar(512)` | |
| `careers_page_url` | `varchar(512)`, nullable | |
| `founded_year` | `integer`, nullable | Validated in the domain to `[1800, 2100]`. |
| `created_at` / `updated_at` | `timestamptz` | Server-side defaults (`now()` / `now()` on update). |

No foreign keys reference `companies.id` yet. Slice 2 (`opportunities`) will
add a DB-level FK to `companies.id` — acceptable since both tables live in one
physical database (ADR 0001's contract-only rule is an **application-code**
boundary; it doesn't forbid a DB-level FK within one deployable). Application
code still never joins across contexts directly — it goes through
`companies.contract`.

## What's deliberately not here yet

- **Geo/PostGIS columns** — deferred to Slice 4 (`geo` context); no
  `geography(Point, 4326)` column exists yet.
- **pgvector columns** — deferred to whichever phase first needs embeddings
  (Resume Intelligence or Polaris); the CI `database` job's Postgres image
  will need to switch to one bundling pgvector at that point.
- **Company Intelligence fields** (team size bucket, funding stage, tech
  stack, growth signal) — Slice 5; added as new nullable columns, additive to
  this table, not a redesign.

## Slice Boundary Review (pre-merge)

An `architecture-guardian` review before merging Slice 1 confirmed: the
`companies` table holds only Slice-1 factual fields (no geo/opportunity/
intelligence columns leaked in); the migration touches nothing outside
`companies`; and `alembic check` + `lint-imports` both stayed green after the
review's one required change (see `contexts/companies/CLAUDE.md` and the
feature spec's "Slice Boundary Review" note) — the unused
`SqlAlchemyCompanyReader` adapter was removed from
`companies/infrastructure/` since it had no caller this slice. No schema
change resulted from the review; it was a code-level, not table-level, fix.
