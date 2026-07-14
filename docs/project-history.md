# NorthStar — Project History

A narrative record of how NorthStar came to be and how its architecture was
decided, for contributors who need the *why* behind the code. For the
authoritative current design see `docs/architecture/blueprint.md`; for individual
decisions see `docs/adr/`.

## Why NorthStar exists

Job seekers are served by search engines — portals that match keywords and
return listings. What people actually need when steering a career is
*navigation*: where am I, what's nearby, what's my best next move, what will it
pay, what should I learn. NorthStar exists to answer those questions. The
guiding metaphor is **"Google Maps for Careers"**: navigation over search,
decision intelligence over filtering, AI guidance over keyword matching.

## The original vision

An AI-powered **Hyperlocal Career Navigation Platform** — tagline *"Navigate Your
Career. Reach Your North Star."* A universe/navigation design language (North
Star = dream career, Earth = current position, planets = opportunities, stars =
skills, Polaris = the AI assistant), kept enterprise-clean and elegant rather
than game-like. Long-term it spans many professions and opportunity types; the
**MVP is deliberately narrow**: Hyderabad · Software Engineering · AI/ML roles.

## Major architectural decisions

Nine foundational decisions were made before implementation and are recorded as
immutable ADRs (`docs/adr/`):

1. **Modular monolith** with mechanically-enforced context boundaries (0001).
2. **Source-agnostic ingestion** — pluggable providers, legal sources first, no
   scraping (0002).
3. **Cloud-agnostic, local-first infrastructure** behind ports (0003).
4. **Anonymous-first experience** with personalization layered on an auth gate
   (0004).
5. **Facts First, AI Second** — deterministic engines compute truth; AI only
   communicates (0005).
6. **Career Intelligence Engine** — the deterministic engine tier with a uniform
   `EngineResult` and per-engine Definition of Done (0006).
7. **LLM Port, no agent framework** for the MVP — thin Claude adapter; no
   LangGraph/PydanticAI (0007).
8. **API contracts as the single source of truth** — backend-owned, generated
   frontend types (0008).
9. **Automation enforces architecture** — guardrails are mechanical; changes
   begin with an ADR (0009).

Two cross-cutting standards emerged alongside them: **Living Documentation**
(a feature isn't done without updated docs + ADRs) and **Additive Extensibility**
(providers, engines, contexts, and platform capabilities are added without
rewrites).

## Phase 0 milestones (Foundation — no features)

| # | Milestone | Outcome |
|---|-----------|---------|
| 1 | Repository Foundation | Turborepo + pnpm workspaces; `apps`·`packages`·`infra`·`docs`. |
| 2 | Backend Foundation | FastAPI + uv; 11 bounded contexts + `contract.py`; `platform/`, `shared_kernel/`; health endpoint. |
| 3 | Frontend Foundation | Next.js + TS + Tailwind + shadcn/ui; `(public)`/`(app)` route groups. |
| 4 | Infrastructure | Docker Compose: PostgreSQL + PostGIS + pgvector, Redis; one-command up. |
| 5 | Quality | Ruff · Black · mypy(strict) · pytest · import-linter (2 contracts); ESLint · Prettier · tsc · Vitest · Playwright scaffold. |
| 6 | API Contracts | OpenAPI export → generated TS types → typed `openapi-fetch` client; drift-checked (ADR 0008 executable). |
| 7 | CI/CD | GitHub Actions (3 parallel jobs), uv/pnpm/turbo caching, Dependabot; every guardrail fails the build. |
| 8 | Verification | `scripts/verify-phase0.sh` — fresh-clone gauntlet, executed green end-to-end. |
| 9 | Documentation Finalization | Compliance audit, ADRs 0001–0009, blueprint reconciliation, this history. |

## Significant implementation decisions

- **import-linter with two contracts** (context independence + Clean-Architecture
  layering) turns ADR 0001 from prose into a build gate.
- **`openapi-typescript` + `openapi-fetch`** (types + tiny typed client) chosen
  over a heavier generated SDK, per Simplicity — proven by a backend field change
  flowing through to regenerated types.
- **Generated artifacts are committed and never hand-edited**; CI fails on drift.
- **AI as a platform capability** (`platform/llm/`), not a business context, so
  business logic can never live in the AI layer.
- **Claude Code as an executor of the architecture**: deterministic Skills, one
  review-only `architecture-guardian` agent, and hooks — introduced minimally in
  Phase 0 and grown only as needed.
- **Career Universe** kept lightweight (React + Framer Motion over the same
  canonical data as the map), with D3 deferred until a visualization genuinely
  needs it.

## Future roadmap (post–Phase 0)

Thin vertical slices, anonymous-value-first, each demoable and independently
deployable:

`Data → Visualization → Career Intelligence → Identity → Resume Intelligence →
Career GPS → Polaris.`

- **Phase 1 (Data / product identity):** Mapbox + nearby companies + company
  cards + search by role/location + company details — reads as career navigation,
  not a job board.
- **Phase 2 (Visualization):** the lightweight Career Universe.
- **Phase 3 (Career Intelligence):** first deterministic engines end-to-end.
- **Phase 4 (Identity):** anonymous→authenticated upgrade.
- **Phase 5 (Resume Intelligence):** resume → structured profile → matching +
  skill gap.
- **Phase 6 (Career GPS):** salary + career-path engines; React Flow roadmap.
- **Phase 7 (Polaris):** the AI assistant, last — narrating what the engines
  already computed.

Deferred until justified by user value (each via a new ADR): other cities and
verticals, employer/user-contributed ingestion, D3 visualizations,
LangGraph/PydanticAI, mobile, real-time features.

## Phase 1 — in progress

Spec: `docs/features/phase1/hyperlocal-career-navigation.md`. Status:
`docs/roadmap/phase-1.md`. Delivered as five sequential slices (Company
Foundation → Opportunity Foundation → Seed Hyderabad Dataset → Map Experience
→ Company Intelligence), one at a time, each spec'd, implemented, verified,
documented, and committed before the next begins.

**Slice 1 — Company Foundation (complete).** `Company` established as the
platform's aggregate root, designed for additive extensibility: later slices
(offices/geo, Company Intelligence, and beyond — reviews, benefits, ESG,
hiring velocity, campus hiring, internship/articleship programs, Career
Universe, Polaris) attach new optional fields or related value objects
without ever renaming or restructuring what Slice 1 shipped. Identity is
split deliberately: `CompanyId` (stable, UUID) is the only thing referenced
across the `contract.py` boundary or by a future `Opportunity`; `CompanySlug`
is separate and mutable, for URLs only. This slice also introduced the
repository's first real database dependency (SQLAlchemy + Alembic + psycopg)
and its first migration, which per the blueprint's own §7 footnote triggered
adding a DB migration-check job to CI alongside the existing API
contract-drift check.

Before merge, a Slice Boundary Review (via the `architecture-guardian`
agent) checked the slice against five criteria: every new file belongs to
`companies` or infrastructure/platform; no speculative abstractions; no
future-phase functionality (geo, opportunities, seed data, map UI, Company
Intelligence fields) leaked in; `Company` holds only plain factual fields; and
zero coupling to `career_intelligence`/`resume`/`polaris`/`identity`/
`profile`/`engagement`/`career_gps`, mechanically confirmed via
`lint-imports`. Four of five checks passed outright; the fifth flagged a
genuine finding — `SqlAlchemyCompanyReader`, a concrete adapter with zero
callers this slice — which was removed rather than kept "for later." The
`CompanyReader` contract type stays (Slice 1's own acceptance criteria
required the read-model shapes to exist); only the unimplemented, unused
adapter was cut. This is the pattern going forward: each slice gets an
independent boundary review before merge, not just self-verification.
