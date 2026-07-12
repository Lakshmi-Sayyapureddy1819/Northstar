# Phase 0 — Foundation (no features)

> Goal (Blueprint §7): `git clone` → `docker compose up` → a running (empty) app
> with every guardrail live. No business features. This document tracks the
> Phase 0 milestones and their status.

**Exit criterion:** a new contributor (or Claude Code) can clone, start
everything, run the full check suite green, and read exactly *why* every
architectural choice exists — before a single feature exists.

## Milestone status

| # | Milestone | Status |
|---|-----------|--------|
| 1 | Repository Foundation — Turborepo + pnpm workspaces, `apps/`·`packages/`·`infra/`·`docs/` | ✅ Complete |
| 2 | Backend Foundation — FastAPI + uv, health endpoint, config, `platform/`, `shared_kernel/`, 11 bounded contexts + `contract.py` | ✅ Complete |
| 3 | Frontend Foundation — Next.js + TS + Tailwind + shadcn/ui, layout, health page, `(public)`/`(app)` route groups | ✅ Complete |
| 4 | Infrastructure — Docker Compose: PostgreSQL + PostGIS + pgvector, Redis; one-command up | ✅ Complete |
| 5 | Quality — Ruff · Black · mypy · ESLint · Prettier · tsc · pytest · Vitest · Playwright · import-linter | ✅ Complete |
| 6 | API Contracts — OpenAPI → generated TypeScript client → `packages/api-contracts` | ✅ Complete |
| 7 | CI — GitHub Actions: lint · typecheck · test · import-linter · contract-drift · build; uv/pnpm/turbo caching; Dependabot | ✅ Complete |
| 8 | Verification — build, compose, CI, contracts, hooks, skills all green | ⬜ Pending |
| 9 | Documentation Finalization — ADRs 0001–0009, blueprint review, getting-started, diagrams, final verification, retrospective, consistency review | ⬜ Pending |

## Milestone 9 — Documentation Finalization (after all implementation milestones)

The last milestone of Phase 0, run only once Milestones 1–8 are complete.
Documentation is written to reflect the architecture **as implemented**, not only
as originally designed.

- **ADRs 0001–0009** — the nine principles, reflecting the as-built system.
- **Engineering Blueprint v1.0 review** — reconcile the frozen blueprint against what was built.
- **Getting Started guide** — proven by a fresh-clone dry run.
- **Architecture diagrams.**
- **Final Phase 0 verification.**
- **Phase 0 retrospective.**
- **Documentation consistency review.**

## Blueprint §7 checklist

**Scaffolding**
- [x] Turborepo + pnpm; `apps/web` (Next.js) + `apps/api` (FastAPI/uv) boot with a health check.
- [x] Docker Compose: Postgres+PostGIS+pgvector, Redis; one-command up. *(extension init hook in place; product seed data deferred — no product data in Phase 0. Verified via `infra/compose/verify.sh`; see `docs/infrastructure/local-infrastructure.md`.)*
- [x] Pydantic Settings (env-only config); documented `.env.example`.

**Guardrails**
- [x] `contexts/` skeleton with empty `contract.py` per context + `shared_kernel/` + `platform/`.
- [x] **import-linter** enforcing contract-only boundaries — 2 contracts (context independence + Clean Architecture layers). *(configured & passing in M5; wired into CI in M7)*
- [x] Ruff + Black + mypy (strict) for Python; ESLint + Prettier + `tsc --noEmit` for TS.
- [x] pytest + a first engine-pattern unit test; Vitest + Playwright scaffold on web.
- [x] OpenAPI → `packages/api-contracts` type generation. *(M6 — one-command `pnpm contracts:generate`; committed artifacts; CI drift validation wired in M7)*
- [x] GitHub Actions: lint · typecheck · test · import-linter · contract-drift · build, with uv/pnpm/turbo caching and Dependabot. *(M7 — see `docs/engineering/continuous-integration.md`; e2e job documented as deferred to Phase 1)*

**Decision record & docs**
- [ ] ADRs **0001–0009** written (the nine principles). *(NOT yet authored — `docs/adr/` is empty. See "Open gap" below.)*
- [x] `docs/architecture/blueprint.md` (frozen v1.0); layered `CLAUDE.md`; `.claude/` scaffold.
- [ ] `docs/engineering/getting-started.md` proven by a fresh-clone dry run. *(M8)*

## Open gap — ADRs 0001–0009 not yet written

Blueprint §7 and §9 require the nine ADRs as a Phase 0 deliverable. They are
referenced throughout the codebase and `CLAUDE.md` files but `docs/adr/` does
not exist yet. This is tracked as an explicit gap to be closed within Phase 0
(via the `update-adr` skill) — it is not covered by any of Milestones 4–8 above
and should be scheduled before Phase 0 is declared complete.

## Cross-cutting standards adopted in Phase 0

- **Accessibility** is an engineering standard from day one (semantic HTML, keyboard, focus, contrast, reduced motion) — see `apps/web/CLAUDE.md`.
- **Theming** structured for light/dark/brand via semantic tokens — see `apps/web/CLAUDE.md` and `apps/web/src/app/globals.css`.
