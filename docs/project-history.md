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

**Execution order revised after Slice 1 (2026-07-14).** The original slice
sequence (Company Foundation → Opportunity Foundation → Seed Hyderabad
Dataset → Map Experience → Company Intelligence) put the first visible,
demoable product experience fourth — three slices of pure backend work
before anything appears in a browser. Reordered to: Company Foundation →
Seed Hyderabad Dataset → Map Experience → Opportunity Foundation → Company
Intelligence, so the map — the actual "Google Maps for Careers" moment —
lands as slice 3 instead of slice 4. No architecture changed: same five
slices, same contexts, no new import-linter contracts, no ADR superseded.
The reorder does shift what each slice's content boundary covers — most
notably, Location/geo work moves earlier (into the Seed slice, since seeded
companies need real coordinates) and Opportunity's real-postings seed moves
later (since Slice 2 no longer seeds opportunities, there's no context to
hold them in until Slice 4). See `docs/roadmap/phase-1.md` and the feature
spec's Rollout Plan for the reconciled detail.

**Slice 2 — Seed Hyderabad Dataset (complete).** `geo` got its first real
content — `Location` (validated lat/lng) as a first-class value object, and
`company_locations` (PostGIS `geography(Point,4326)` + GIST index, one row
per company, keyed by the opaque `CompanyId`). `Company` itself was not
touched — this slice only adds rows, the first real proof that Slice 1's
extensibility design holds under a second slice. The seed script (30 real
Hyderabad SWE/AI-ML companies across all seven requested localities) is
deliberately structured as load → persist, so a future real data source only
ever replaces the load step. Two real bugs were caught by actually running
things rather than trusting the code read right: a geoalchemy2 migration
gotcha (its `Geography(spatial_index=True)` auto-creates a GIST index via an
event listener, which collided with Alembic's own autogenerated
`create_index` call — fixed by removing the duplicate), and one seed record
(State Street Corporation, `founded_year: 1792`) that violated `Company`'s
own `[1800, 2100]` validation — fixed by correcting the data, not loosening
the domain rule. The Slice Boundary Review passed all 7 checks and flagged
one thing worth tracking going forward, not fixing now: the seed script
writes to `companies` by importing its domain/infrastructure directly rather
than through `companies.contract`, because Slice 1 never shipped a write use
case (only reads). Pre-authorized by the approved spec for this slice; if
Slice 4's opportunity seed repeats the same shortcut, that's the signal
`companies` actually needs a `CreateCompany` application use case.

**Slice 3 — Map Experience (complete).** The product's identity moment:
the first thing a visitor to `localhost:3100` sees is now a real, live map
of Hyderabad companies, not a Phase 0 placeholder. `geo` gained the read
port the Slice 1/2 reviews deliberately deferred (`FindNearbyCompanies`,
`ST_DWithin`/`ST_Distance` against Slice 2's `company_locations` — no new
migration needed, proof that table was already the right shape). The
frontend got its first real feature module (`features/map/`): Mapbox GL
(client-only, code-split off the critical path), custom "career node"
markers (industry-tinted glow, not default pins — the visual seed of Phase
2's "nodes become planets"), native clustering, a locality picker + "Near
Me" + client-side industry filter chips, a company detail panel, and a
deep-linkable `/companies/[slug]` route.

Four real bugs surfaced only by actually running the full stack, not by
reading the code: (1) **no CORS middleware existed anywhere in the
backend** — every browser-side fetch from the frontend's origin would have
been silently blocked; invisible to `curl`, which doesn't enforce CORS —
fixed with a `GET`-only `CORSMiddleware`; (2) the nearby-query response
needed `latitude`/`longitude` added mid-slice — a distance alone can't place
a map marker, a gap the original spec didn't anticipate; (3)
`prefers-reduced-motion` looked handled (a global CSS rule already existed)
but that rule only catches native CSS animations — it does nothing for
Framer Motion's JS-driven animations, which needed `useReducedMotion()`
wired in explicitly at three call sites; (4) the page wasn't wrapped in a
`<main>` landmark, a direct, explicit requirement of `apps/web/CLAUDE.md`'s
accessibility standard. All four were caught and fixed before the Slice
Boundary Review, not after.

Verified live: 7 Playwright e2e tests against the real backend and real
seeded data (the full anonymous journey, "Near Me" denied → graceful
fallback, full keyboard-only reachability into the detail dialog), 12 Vitest
unit tests, and the full `turbo run lint typecheck test build` pipeline
green. One verification gap acknowledged rather than papered over: browser
tooling (Lighthouse via chrome-devtools MCP) wasn't reachable in this
environment, so the full Lighthouse LCP audit specified in the spec's
Testing Strategy couldn't run — a Playwright-measured first-contentful-paint
(~100ms) stood in as an honest proxy, not a substitute claim.
