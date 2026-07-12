# NorthStar Architectural Principles

The distilled, always-open list of the nine principles. This is the quick
reference to keep open while coding; the **decisions with full context** live in
`docs/adr/` (0001–0009), and the system design in `docs/architecture/blueprint.md`
(frozen v1.0). If this list and an ADR ever disagree, the ADR wins.

1. **Modular monolith, enforced boundaries** *(ADR 0001)* — one FastAPI
   deployable, partitioned into bounded contexts; cross-context access only via
   `contract.py`; dependencies point inward. Enforced by import-linter.
2. **Source-agnostic ingestion** *(ADR 0002)* — pluggable `JobProvider`
   adapters normalizing into a canonical schema; legal sources first; never
   scrape LinkedIn/Naukri/Indeed.
3. **Cloud-agnostic, local-first** *(ADR 0003)* — infra behind ports, config
   from env only, Docker Compose locally, managed services at deploy; no vendor
   SDK in domain/application.
4. **Anonymous-first** *(ADR 0004)* — identity-agnostic Core shared by all;
   personalization layered on an auth gate, never a wall in front of value.
5. **Facts First, AI Second** *(ADR 0005)* — deterministic engines compute
   truth; AI (Polaris) only explains, summarizes, compares, answers,
   personalizes. AI never computes business facts.
6. **Career Intelligence Engine** *(ADR 0006)* — the only recommender; a
   registry of single-responsibility deterministic engines, each returning the
   uniform `EngineResult` and meeting the Engine Definition of Done.
7. **LLM Port, no agent framework (MVP)** *(ADR 0007)* — thin Claude adapter
   behind an `LLMPort` in `platform/llm/`; no LangGraph/PydanticAI until a real
   requirement outgrows the SDK.
8. **API contracts are truth** *(ADR 0008)* — backend owns the OpenAPI schema;
   frontend consumes generated types only; generated files never hand-edited;
   CI fails on drift.
9. **Automation enforces architecture** *(ADR 0009)* — hooks/Skills/CI/agents
   protect the design; they never make design decisions. Architectural changes
   begin with an ADR, before implementation.

## Cross-cutting standards

- **Simplicity** *(recorded in ADR 0001)* — the simplest implementation that
  delivers the intended UX; add complexity only when justified by user value.
- **Living Documentation (DoD)** — a feature is complete only with
  implementation + passing tests + updated docs + ADRs when architecture changes.
- **Additive Extensibility** — every new provider, engine, context, or platform
  capability is added incrementally, without an architectural rewrite.
