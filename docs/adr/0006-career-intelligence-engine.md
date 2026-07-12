# ADR 0006 — Career Intelligence Engine (deterministic engine tier)

- **Status:** Accepted
- **Date:** 2026-07-12

## Context

"Facts First" (ADR 0005) requires a home for objective recommendations that is
distinct from both the data contexts and the AI layer. It must let many
single-responsibility engines coexist, each independently testable, and let new
engines be added without disturbing existing ones (additive extensibility).

## Decision

Formalize the recommendation layer as the **Career Intelligence Engine (CIE)** —
a registry of deterministic engines and the *only* layer that makes objective
recommendations. Every engine returns a standard `EngineResult`: typed **input →
{ output, confidence, explanation, trace/provenance, metadata }**, giving uniform
explainability and a future analytics substrate. Each engine satisfies an
**Engine Definition of Done**: deterministic · independently testable ·
explainable · confidence score · trace/provenance · documented · benchmarked.
Adding an engine is a new module + one registry entry + a spec — no change to
existing engines.

MVP engines: matching, ranking, salary, skill_gap, career_path, commute,
company_scoring. Future (additive): offer comparison, resume scoring, market
trend, hiring trend, learning recommendation.

## Consequences

- Recommendations are uniform, explainable, and analyzable.
- Engines are isolated and independently testable; the tier grows additively.
- The `EngineResult` envelope is a stable contract the AI layer can rely on.

## As implemented

- `contexts/career_intelligence/` with `engines/`, `registry.py`, and the
  `Engine` protocol + `EngineResult` in `domain/` (see `domain/engine.py`,
  `domain/engine_result.py`, `contract.py`). `EngineResult.confidence` is
  bounded 0..1 (validated; tested in `tests/test_engine_result.py`).
- The DoD and the "no LLM / no non-determinism" rule are documented in
  `career_intelligence/CLAUDE.md`; the `add-engine` skill scaffolds engines to
  satisfy the DoD from birth.
- Phase 0 ships the tier's contract and an example-engine test pattern; concrete
  engines arrive in the Career Intelligence phase.
