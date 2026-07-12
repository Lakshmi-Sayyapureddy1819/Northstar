# NorthStar Engineering Blueprint

**Version:** 1.0 (Frozen)
**Date:** 2026-07-11
**Status:** Canonical. Proceed exactly per this blueprint. No new architectural concept is introduced unless a new ADR formally changes the design.

> _Navigate Your Career. Reach Your North Star._

---

## 0. How to read this document

This is the frozen architectural record for NorthStar v1.0. It is the parent of every downstream artifact:

- The **eight principles** (§2) become ADRs `0001`–`0008`, plus a ninth for the automation principle.
- The **structure** (§4) becomes the actual repository.
- The **roadmap** (§6) becomes the phase plan; Phase 0 (§7) is next.
- Any change to what's written here requires **discussion → documentation → ADR**, before implementation.

---

## 1. Product Vision (canonical summary)

NorthStar is an **AI-powered Hyperlocal Career Navigation Platform** — "Google Maps for Careers." It is explicitly **not** a job board. It answers *navigation* and *decision* questions: What is my best next move? Which nearby companies fit me? What should I learn next? What salary should I expect? Where is the highest long-term growth?

- **Positioning:** Navigation over search; decision intelligence over filtering; AI guidance over keyword matching. Not competing with LinkedIn / Naukri / Indeed.
- **MVP scope:** Hyderabad · Software Engineering · AI/ML roles. Everything else is explicitly deferred.
- **Builder context:** solo developer with occasional Claude Code assistance. Production-grade but operationally lightweight.
- **Design language:** subtle navigation/universe metaphor (North Star = dream career, Earth = current position, planets = opportunities, stars = skills, rocket = journey, Polaris = AI assistant). Enterprise-quality and elegant — never game-like.

The canonical business specification lives in `docs/product/prd.md`; every feature traces back to it.

---

## 2. Architectural Principles

These nine principles are the permanent truths of NorthStar. Each is backed by an immutable ADR.

| # | Principle | ADR | One-line rule |
|---|-----------|-----|---------------|
| 1 | **Source-Agnostic Ingestion** | 0002 | Pluggable `JobProvider` adapters; legal sources first; never scrape LinkedIn/Naukri/Indeed. |
| 2 | **Cloud-Agnostic Infrastructure** | 0003 | Local-first Docker Compose; managed services at deploy; infra behind ports; replaceable without code change. |
| 3 | **Anonymous-First Experience** | 0004 | Identity-agnostic core shared by all; personalization layered on top of an auth gate. |
| 4 | **Facts First, AI Second** | 0005 | Deterministic engines produce truth; AI communicates, personalizes, assists — never computes business facts. |
| 5 | **Career Intelligence Engine** | 0006 | The only layer that makes objective recommendations; a registry of single-responsibility deterministic engines. |
| 6 | **Simplicity** | (in 0001) | Simplest implementation that delivers the intended UX; complexity only when justified by user value, not aesthetics. |
| 7 | **API Contracts Are Truth** | 0008 | Backend owns the OpenAPI contract; frontend consumes generated types only. |
| 8 | **LLM Port, No Agent Framework (MVP)** | 0007 | Thin Claude adapter behind an `LLMPort`; no PydanticAI/LangGraph until a real requirement outgrows the SDK. |
| 9 | **Automation Enforces Architecture** | 0009 | Hooks/Skills/agents protect the architecture; they never make design decisions. Changes start with an ADR. |

Two cross-cutting standards derived from these:

- **Living Documentation (DoD):** a feature is complete only when implementation + tests + documentation + (when needed) ADRs are all done. Docs evolve with the code.
- **Additive Extensibility (goal):** every new provider, engine, bounded context, or platform capability can be added incrementally without an architectural rewrite.

The distilled, always-open version of this list lives in `docs/architecture/principles.md`.

---

## 3. System Architecture

### 3.1 Shape: modular monolith with enforced boundaries

One FastAPI application, one deployable, internally partitioned into **bounded contexts** that communicate only through explicit `contract.py` interfaces — never by reaching into each other's internals. This is a modular monolith engineered to evolve into microservices: the seams are drawn now, not retrofitted later. The boundary rule is enforced mechanically by **import-linter** in CI.

### 3.2 The three tiers

```
CORE (identity-agnostic, cacheable, anonymous-accessible)
  Ingestion → Opportunities → Companies → Geo
                     ↘        ↙
              Career Intelligence Engine  (deterministic engines = truth)
        │
        ▼ consumes core facts
PERSONALIZATION (auth-gated)
  Identity/Auth · Profile · Resume Intelligence · Career GPS · Engagement
        │
        ▼ consumes core + personalization
POLARIS (AI assistant)
  Explains · summarizes · compares · answers · personalizes.  Owns no facts.
```

- **Core** knows nothing about users → fast, cacheable, SEO-friendly anonymous experience.
- **Career Intelligence Engine (CIE)** is a distinct deterministic tier — the structural heart of Facts-First.
- **Polaris** only reads downward; it is architecturally incapable of computing facts.

### 3.3 Clean Architecture within every context

```
API/Router → Application (use cases) → Domain (entities, logic)
                    ↓                        ↑
               Ports (interfaces) ← Infrastructure (adapters: DB, Redis, Mapbox, Claude, providers)
```

Dependencies point inward. Domain/Application never import infrastructure. This is what makes Postgres/Redis/Claude/Mapbox swappable and business logic unit-testable without a database.

### 3.4 The Career Intelligence Engine

The CIE is the only layer that makes objective recommendations. It is a **registry of single-responsibility deterministic engines**.

**MVP engines:** Matching · Ranking · Salary Intelligence · Skill Gap · Career Path · Commute · Company Scoring.
**Future engines** (must add without touching existing ones): Offer Comparison · Resume Scoring · Market Trend · Hiring Trend · Learning Recommendation.

**Standard `EngineResult`** every engine returns — uniform for explainability and future analytics:

```
Input (typed) → {
  Output      (typed),
  Confidence  (score),
  Explanation (human-readable),
  Trace       (provenance back to structured data),
  Metadata
}
```

**Engine Definition of Done** (all required before an engine is complete):
Deterministic · Independently testable · Explainable · Confidence score · Trace/Provenance · Documented (`docs/engines/<name>.md`) · Benchmarked.

Adding an engine = new module under `career_intelligence/engines/<name>/` implementing the contract + one `registry.py` entry + a spec. Zero changes to existing engines.

### 3.5 AI as a platform capability

The AI layer is **infrastructure, not business logic**. `platform/llm/` owns the `LLMPort`, the Claude adapter, prompt infrastructure, structured-output handling, and AI observability. **Polaris** (a context) consumes that platform capability plus engine contracts; it holds conversation and orchestration only. Business decisions always live in deterministic engines.

MVP AI stack: `LLMPort` → `ClaudeAdapter` (thin wrapper over the `anthropic` SDK using `messages.parse` + Pydantic models for validated structured output; default model `claude-opus-4-8`). No PydanticAI, no LangGraph — the SDK already provides typed validated outputs, and the port already provides provider-agnosticism.

### 3.6 Ingestion

Ingestion is isolated behind a `JobProvider` port. Each source is an independent adapter normalizing into one **canonical Opportunity schema** with **provenance + dedup** as first-class concerns. Preferred source order: (1) official career pages, (2) public ATS providers (Greenhouse, Lever, Ashby, Workable, SmartRecruiters), (3) public structured JobPosting metadata, (4) employer-submitted [future], (5) user-contributed [future]. Adding a provider = new adapter + config, never a core change.

---

## 4. Repository Structure

Turborepo monorepo (pnpm workspaces; Python API managed with `uv`, orchestrated by Turbo as an opaque target).

```
northstar/
├── apps/
│   ├── web/                    # Next.js (App Router) — sole frontend deployable
│   └── api/                    # FastAPI — the modular monolith
├── packages/
│   ├── ui/                     # shadcn/ui + design system
│   ├── api-contracts/          # TS types generated from the API OpenAPI schema
│   ├── config-eslint/ · config-typescript/
├── infra/{docker,compose}/     # Dockerfiles; docker-compose (Postgres+PostGIS+pgvector, Redis)
├── docs/                       # §5
├── .claude/                    # §8
├── .github/workflows/          # lint · typecheck · test · import-linter · contract-drift · build
├── turbo.json · package.json · CLAUDE.md
```

### 4.1 API (bounded contexts)

```
apps/api/src/northstar/
├── main.py                     # app assembly, router registration, DI wiring
├── shared_kernel/              # domain primitives shared across contexts (small by design)
├── platform/                   # technical foundation, not business logic
│   ├── db/ · cache/ · geo/ · config/ · observability/
│   └── llm/                    # LLMPort + ClaudeAdapter + prompt infra + AI observability
├── contexts/
│   ├── ingestion/              # domain · application · providers/ · infrastructure · contract.py
│   ├── opportunities/ · companies/ · geo/
│   ├── career_intelligence/    # THE ENGINE TIER
│   │   ├── domain/             # engine contract, EngineResult, trace types
│   │   ├── engines/{matching,ranking,salary,skill_gap,career_path,commute,company_scoring}/
│   │   ├── registry.py
│   │   └── contract.py
│   ├── identity/ · profile/ · resume/ · career_gps/ · engagement/
│   └── polaris/                # consumes contracts + platform/llm; owns no facts
└── api/                        # thin HTTP layer: routers/ · dependencies.py · schemas
```

**Mandatory rules:**
- `contract.py` is a context's only public surface. Cross-context imports may reference *only* the contract. Enforced by import-linter.
- `platform/` = technical; `shared_kernel/` = domain primitives. Keep distinct.

### 4.2 Web

```
apps/web/src/
├── app/(public)/               # anonymous: explore, company, career-universe
├── app/(app)/                  # auth-gated: dashboard, gps, resume, tracking
├── features/{career-universe,map,company-intelligence,career-gps,polaris}/
├── components/ (from packages/ui) · lib/api (generated typed client) · styles/
```

`(public)`/`(app)` route groups express the anonymous-first boundary; the same core navigation components render in both, personalization layered via props/context. Frontend consumes only generated API types (`packages/api-contracts`) — drift from the backend contract becomes a type error.

---

## 5. Documentation Structure

```
docs/
├── product/    prd.md · user-flows.md · vision.md · mvp-scope.md · personas.md · design-language.md
├── architecture/  overview.md · principles.md · bounded-contexts.md · career-intelligence-engine.md
│                  · ingestion.md · ai-and-polaris.md · data-model.md · blueprint.md (this file)
├── adr/        0001–0009 (immutable) + README index
├── api/        philosophy · versioning · authentication · error-model · pagination · filtering · rate-limiting
├── database/   schema-overview · entity-relationships · migration-strategy · postgis · pgvector
├── ai/         polaris-architecture · llm-port · prompt-strategy · structured-outputs
│               · context-management · guardrails · evaluation-strategy
├── engineering/ getting-started · local-development · coding-standards · testing-strategy
│               · module-boundaries · conventions
├── engines/    _template.md (Input/Output/Confidence/Explanation/Trace/Metadata) + one spec per engine
├── runbooks/   deployment · ingestion-provider-onboarding
└── roadmap/    roadmap.md · phase-0.md
```

- **ADRs are immutable & numbered.** A changed decision is a *new* ADR superseding the old one.
- `docs/engines/` mirrors the engine registry; the spec `_template.md` sections *are* the `EngineResult` fields. Writing the spec is step one of adding an engine.
- `docs/architecture/` = cross-cutting decisions; `docs/{api,database,ai}/` = conventions within one concern.
- Plain Markdown in-repo (no docs-site framework yet). A PR that changes a contract changes its doc in the same commit.

---

## 6. Development Roadmap

Sequencing: **least-dependencies-first** and **anonymous-value-first**. Each post-foundation phase is a thin vertical slice (DB → engine/context → API → web) ending demoable and independently deployable.

```
Foundation → Data → Visualization → Career Intelligence → Identity
   → Resume Intelligence → Career GPS → Polaris
```

| Phase | Slice | Delivers |
|-------|-------|----------|
| **0** | Foundation | Skeleton, guardrails, ADRs, green CI. No features. (§7) |
| **1** | Data (product identity) | Mapbox + nearby companies + company cards + search by role + search by location + company details. Reads as "career navigation," not "job board." |
| **2** | Visualization | Lightweight Career Universe over the **same canonical data** as the map (React components + Framer Motion). Map = "Where are opportunities?"; Universe = "How do opportunities relate to me?" |
| **3** | Career Intelligence | First engines (Commute, Company Scoring, Ranking) end-to-end; results carry `EngineResult`. |
| **4** | Identity | Anonymous→authenticated upgrade (searches saved on login); auth boundary live without disturbing the core. |
| **5** | Resume Intelligence | Resume upload → structured profile (LLM parsing) → Matching + Skill Gap engines. |
| **6** | Career GPS | Salary Intelligence + Career Path engines; React Flow roadmap arrives. |
| **7** | Polaris | AI assistant, last — narrates what the engines already computed; guardrails + eval harness. |

**Polaris is last on purpose:** it can only be trustworthy once engines exist to feed it facts. Phases are additive — none rewrites a previous one.

**Phase Completion DoD:** working software · passing tests · updated docs · updated ADRs (when required) · demo-ready · independently deployable.

**Explicitly deferred:** other cities, non-SWE verticals, employer/user ingestion, D3 visualizations, LangGraph/PydanticAI, mobile, real-time features. Each returns only when a phase's user value justifies it — via an ADR.

---

## 7. Phase 0 — Foundation (no features)

Goal: `git clone` → `docker compose up` → a running (empty) app with every guardrail live. Full checklist in `docs/roadmap/phase-0.md`.

**Scaffolding**
- Turborepo + pnpm; `apps/web` (Next.js) + `apps/api` (FastAPI/uv) boot with a health check.
- Docker Compose: Postgres+PostGIS+pgvector, Redis; one-command up + seed hooks.
- Pydantic Settings (env-only config); documented `.env.example`.

**Guardrails**
- `contexts/` skeleton with empty `contract.py` per context + `shared_kernel/` + `platform/`.
- **import-linter** in CI enforcing contract-only boundaries.
- Ruff + Black + mypy (strict) for Python; ESLint + Prettier + `tsc --noEmit` for TS.
- pytest + a first engine unit test as the pattern; Vitest + Playwright scaffold on web.
- OpenAPI → `packages/api-contracts` type generation in CI.
- GitHub Actions: lint · typecheck · test · import-linter · contract-drift · build — green on an empty repo. (A DB migration check is added when the first Alembic migration lands; there are no DB models in Phase 0.)

**Decision record & docs**
- ADRs **0001–0009** written (the nine principles).
- `docs/architecture/principles.md`, initial `docs/product/prd.md`, `docs/product/mvp-scope.md`, this blueprint.
- Layered `CLAUDE.md` (root + per-context stubs) and `.claude/` scaffold (§8).
- `docs/engineering/getting-started.md` proven by a fresh-clone dry run.

**Exit criterion:** a new contributor (or Claude Code) can clone, start everything, run the full check suite green, and read exactly *why* every architectural choice exists — before a single feature exists.

---

## 8. Claude Code Integration

Adopted gradually: a small, high-leverage foundation in Phase 0; advanced capabilities only when a real need appears. Claude Code is an **executor of the architecture**, never a freewheeling generator.

### 8.1 Layered `CLAUDE.md`

- **Root `CLAUDE.md`** — concise; **permanent architectural truths only** (the nine principles, hard rules, how to run). Implementation detail lives in local files/docs so the root stays stable as the project grows.
- **`apps/api/CLAUDE.md`** — Clean Architecture layering, Result/error types, context anatomy.
- **`contexts/career_intelligence/CLAUDE.md`** — how to add an engine: `EngineResult`, the Engine DoD, registry step, spec template.
- **`contexts/ingestion/CLAUDE.md`** — how to add a provider: `JobProvider` port, canonical schema, dedup/provenance.
- **`contexts/polaris/CLAUDE.md`** — the Facts-First boundary in bold: Polaris explains, never computes.
- **`apps/web/CLAUDE.md`** — feature-first, generated API types only, `(public)/(app)` split, Framer Motion sparingly.

### 8.2 Phase-0 `.claude/` assets

```
.claude/
├── skills/          add-engine · add-provider · add-context · update-adr
│                    · update-documentation · generate-api-contracts
├── agents/          architecture-guardian.md
└── settings.json    permissions + hook wiring
```

**Skills are deterministic** — they scaffold or validate architectural patterns; they never make product decisions. `add-engine` gives every engine the `EngineResult` shape, a test, a benchmark stub, a registry entry, and a spec from birth (Engine DoD as a template).

**Architecture Guardian** is the repository's **technical reviewer**: it reviews changes and **never implements features or modifies business logic**. It verifies module boundaries · contract-only imports · architectural principles · Engine DoD · Phase DoD · Living Documentation · ADR requirements · PRD traceability.

### 8.3 Hooks (Phase 0)

- **Quality gate** (pre-commit / PreToolUse): Ruff + mypy + ESLint + `tsc` + **import-linter** on changed files — the contract-boundary rule becomes mechanically unbreakable.
- **Doc-drift check** (post-edit): a new engine/context without its matching `docs/engines/*.md` or `contract.py` is flagged — Living-Documentation DoD, automated.

### 8.4 Deferred (introduce only when complexity justifies)

- **MCP servers** — when an external system merits a first-class tool surface.
- **Additional reviewers** — Security · Performance · Accessibility · Data Quality · AI Evaluation.
- **Workflow orchestration** — only if multi-agent parallelism pays for itself here.

---

## 9. ADR Index (to be authored in Phase 0)

| ADR | Title |
|-----|-------|
| 0001 | Modular monolith with enforced context boundaries (incl. Simplicity principle) |
| 0002 | Source-agnostic ingestion |
| 0003 | Cloud-agnostic infrastructure |
| 0004 | Anonymous-first experience |
| 0005 | Facts First, AI Second |
| 0006 | Career Intelligence Engine |
| 0007 | LLM Port; no agent framework for MVP |
| 0008 | API contracts as single source of truth |
| 0009 | Automation enforces architecture |

ADRs are immutable. Every significant architectural decision is captured **before** implementation.

---

## 10. Change Control

This blueprint is **frozen at v1.0**. Phase 0 and all subsequent work proceed exactly per this document. No new architectural concept is introduced unless a new ADR formally supersedes part of this design — and every architectural change begins with **discussion → documentation → ADR**, before implementation.

### Change log

- **2026-07-12 — Milestone 9 blueprint review (no architectural change).** Reconciled blueprint text with the as-built system after the compliance audit (`docs/architecture/compliance-audit.md`): the CI pipeline references were corrected from "migration check" to "contract-drift · build" (§4, §7) — there are no DB models/migrations in Phase 0, and contract-drift is the more valuable gate; a DB migration check is added when the first Alembic migration lands. All nine principles were ratified as immutable ADRs 0001–0009 (`docs/adr/`), and the previously-referenced `docs/architecture/principles.md`, `docs/product/{prd,mvp-scope}.md`, and `docs/engines/_template.md` were authored. No production code changed; no principle changed.

_Automation should enforce architecture, not replace architectural thinking._
