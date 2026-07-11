# Local Infrastructure Architecture

> Local-first data services for NorthStar development. Backed by
> **ADR 0003 (Cloud-Agnostic Infrastructure)**: everything here is local-first,
> sits behind ports, and is replaceable by a managed equivalent at deploy time
> via configuration — never a code change.

Defined in `infra/compose/docker-compose.yml`; images in `infra/docker/`.
Start with one command:

```bash
docker compose -f infra/compose/docker-compose.yml up -d
```

## Services — what, why, and which layer consumes them

| Service | Version | Why it exists | Consuming architectural layer |
|---------|---------|---------------|-------------------------------|
| **PostgreSQL** | 16 | The system of record — relational store for all structured facts (companies, opportunities, profiles, …). Facts-First means truth lives in structured data, and this is where it lives. | `platform/db` (connection/session + persistence port) → each context's `infrastructure/` repositories. Domain/application never touch it directly. |
| **PostGIS** | 3.4 | Geospatial types and queries — distances, "nearby companies", commute geometry. The literal engine behind "hyperlocal" and "Google Maps for Careers". | `platform/geo` (geo port) and the `geo` context; the Commute engine (CIE) reads structured geo facts. |
| **pgvector** | 0.8 | Vector storage + similarity search for embeddings. Reserved for semantic/AI-adjacent retrieval (e.g. grounding Polaris in structured data). Present from Phase 0 so the schema seam exists early; unused until the AI phases. | `platform/llm` / AI-adjacent retrieval. Never a source of business facts (ADR 0005) — it retrieves, engines decide. |
| **Redis** | 7 | Cache and queue substrate. Enables the fast, cacheable, anonymous-accessible Core tier and background work. | `platform/cache` (cache port). Underpins the anonymous-first experience (ADR 0004). |

Extensions (`postgis`, `vector`) are enabled automatically on first
initialization by `infra/docker/postgres/init/01-extensions.sql`.

## Why a custom Postgres image

No single official image bundles **both** PostGIS and pgvector. We therefore
extend `postgis/postgis:16-3.4` and install `postgresql-16-pgvector` from the
PGDG apt repository (`infra/docker/postgres/Dockerfile`), producing
`northstar/postgres:16-postgis-pgvector`. Both extensions, one image, one
`CREATE EXTENSION` init step.

## Platform note — amd64 emulation on Apple Silicon

**Observation:** on Apple Silicon (arm64) hosts, the Postgres container reports:

> _The requested image's platform (linux/amd64) does not match the detected host
> platform (linux/arm64/v8)._

**Why it happens.** The `postgis/postgis:16-3.4` tag we build from resolves to a
`linux/amd64` image. Docker Desktop runs it under emulation (Rosetta 2 / QEMU)
rather than natively.

**Performance implications.** Emulation adds CPU overhead for compute-heavy
operations (large PostGIS geometry math, bulk index builds, heavy queries).
For Phase 0 and typical local development the impact is negligible — the
service is fully correct and responsive. It matters only under heavy local load.

**Should a native arm64 image be considered?** Not required for correctness, and
not worth doing in Phase 0. Revisit **only if** local performance becomes
painful, by either:
- pinning an arm64-capable PostGIS base (some PostGIS tags publish arm64), or
- building a multi-arch image (`docker buildx --platform linux/amd64,linux/arm64`).

This is a local-development ergonomics choice, not an architectural one, and
production runs a managed Postgres regardless (ADR 0003).

## Verification (repeatable — for new contributors)

With the stack up, run the bundled checker:

```bash
infra/compose/verify.sh
```

It validates all four requirements and exits non-zero on any failure:

1. **PostgreSQL connectivity** — `pg_isready` + a live `SELECT`.
2. **PostGIS extension available** — present in `pg_extension` and `postgis_version()` responds.
3. **pgvector extension available** — present in `pg_extension` and the `<=>` distance operator works.
4. **Redis connectivity** — `redis-cli ping` → `PONG`.

Manual equivalents (if you prefer):

```bash
DC="docker compose -f infra/compose/docker-compose.yml"
$DC exec -T postgres pg_isready -U northstar -d northstar
$DC exec -T postgres psql -U northstar -d northstar -c "SELECT postgis_version();"
$DC exec -T postgres psql -U northstar -d northstar -c "SELECT '[1,0]'::vector <=> '[0,1]'::vector;"
$DC exec -T redis redis-cli ping
```

## Start / stop

See `infra/compose/README.md`. Volumes `northstar_pgdata` / `northstar_redisdata`
persist data across restarts; `down -v` wipes them.
