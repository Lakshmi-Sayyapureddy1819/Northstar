# NorthStar — Root Context

> _Navigate Your Career. Reach Your North Star._
> AI-powered **Hyperlocal Career Navigation Platform** — "Google Maps for Careers." NOT a job board.

This file holds only the **permanent architectural truths** of NorthStar. It stays concise on purpose — implementation detail lives in local `CLAUDE.md` files and `docs/`. The canonical architecture is **`docs/architecture/blueprint.md` (frozen v1.0)**.

## Non-negotiable rules

1. **Facts First, AI Second.** Deterministic engines produce truth; AI (Polaris) only explains, summarizes, compares, answers, personalizes. AI never computes business facts.
2. **Contract-only imports.** A bounded context may import another context's `contract.py` — never its internals. Enforced by import-linter.
3. **Career Intelligence Engine is the only recommender.** All objective recommendations come from deterministic engines in `contexts/career_intelligence/`.
4. **API contracts are truth.** Backend owns the OpenAPI schema; frontend consumes generated types (`packages/api-contracts`) only.
5. **Cloud-agnostic.** Infra sits behind ports; config from env only; no vendor SDK in domain/application layers.
6. **Anonymous-first.** The Core tier is identity-agnostic; personalization is gated on auth, never a wall in front of value.
7. **Simplicity.** Simplest implementation that delivers the UX; add complexity only when justified by user value.
8. **Living Documentation (DoD).** A feature is complete only with: implementation + passing tests + updated docs + ADRs when architecture changes.
9. **Automation enforces architecture, never replaces architectural thinking.** Any architectural change begins with discussion → documentation → **ADR**, before implementation. Do not introduce new architectural concepts unless an ADR changes the design.

## The nine principles → ADRs

See `docs/architecture/principles.md` (distilled) and `docs/adr/` (0001–0009, immutable). Every feature traces to `docs/product/prd.md`.

## Structure (see blueprint §4)

- `apps/web/` — Next.js (App Router). `apps/api/` — FastAPI modular monolith.
- Tiers: **Core** (identity-agnostic) → **Personalization** (auth-gated) → **Polaris** (AI).
- Backend contexts live in `apps/api/src/northstar/contexts/`; technical foundation in `platform/`.

## Running locally

`docker compose -f infra/compose/docker-compose.yml up` → Postgres+PostGIS+pgvector, Redis. See `docs/engineering/getting-started.md`.

## Working here (use these)

- Scaffold via deterministic Skills: `add-engine`, `add-provider`, `add-context`, `update-adr`, `update-documentation`, `generate-api-contracts`.
- The **architecture-guardian** subagent reviews diffs against the rules above. It reviews, never implements.
