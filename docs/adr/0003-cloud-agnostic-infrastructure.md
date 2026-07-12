# ADR 0003 — Cloud-agnostic, local-first infrastructure

- **Status:** Accepted
- **Date:** 2026-07-12

## Context

NorthStar is developed by a solo developer and must be production-ready but
operationally lightweight. Committing the codebase to a specific cloud early
creates lock-in and complicates local development. We want to develop locally,
deploy to managed services when ready, and keep infrastructure replaceable
without touching application code.

## Decision

- **Local-first** development via Docker Compose that mirrors production
  topology.
- **Infrastructure behind ports**: DB, cache, geo, blob, queue, and LLM
  providers are accessed through interfaces in `platform/`; domain and
  application layers never import a vendor SDK.
- **Config from environment only** (Pydantic Settings; `NORTHSTAR_`-prefixed).
- Prefer **managed services** at deploy time. Preferred first bindings
  (Vercel / Railway-or-Render / Neon / Upstash) are choices, not assumptions
  baked into code. No Kubernetes / Terraform at this stage.

## Consequences

- A managed service can be swapped by changing an adapter + env, not app code.
- Local dev needs only Docker; a fresh clone reaches a running stack with one
  command.
- Deployment target stays an open, reversible decision.

## As implemented

- `infra/compose/docker-compose.yml` brings up PostgreSQL 16 + PostGIS +
  pgvector and Redis 7 with healthchecks; `infra/compose/verify.sh` proves all
  four. Application containers are intentionally not defined in Phase 0.
- `platform/{db,cache,geo,llm,config,observability}/` hold the technical
  foundation; `platform/config/settings.py` reads env only; `.env.example`
  documents keys.
- `scripts/verify-phase0.sh` starts the stack with `--wait` and verifies it as
  part of the fresh-clone gauntlet.
