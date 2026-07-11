---
name: add-engine
description: Scaffold a new deterministic engine in the Career Intelligence Engine (CIE). Use when adding a Matching/Salary/SkillGap/etc. engine or any future deterministic engine. Deterministic scaffolding only — makes no product decisions.
---

# add-engine

Scaffolds a new CIE engine so it is born satisfying the Engine Definition of Done. This Skill is **deterministic**: it creates structure and stubs from a fixed template; it does not decide business logic or product behavior.

## Inputs

- `<name>` — snake_case engine name (e.g. `offer_comparison`).

## Steps (perform in order)

1. **Confirm it belongs in the CIE.** The engine must be deterministic and compute business facts. If it involves LLM calls or non-determinism, stop — it does not belong here.
2. Create `apps/api/src/northstar/contexts/career_intelligence/engines/<name>/`:
   - `__init__.py`
   - `domain.py` — typed `Input` and `Output` models.
   - `engine.py` — class implementing the common `Engine` contract; returns `EngineResult{output, confidence, explanation, trace, metadata}`.
   - `tests/test_<name>.py` — independent unit tests (no cross-engine deps, no DB where avoidable).
   - `benchmark.py` — a benchmark stub recording accuracy/latency against a fixture set.
3. Register the engine in `contexts/career_intelligence/registry.py`. This is the ONLY wiring point — do not import the engine elsewhere.
4. Create the spec `docs/engines/<name>.md` from `docs/engines/_template.md` (sections: Input / Output / Confidence / Explanation / Trace / Metadata).
5. **Do not modify existing engines.** Additive only.

## Definition of Done (verify before finishing)

Deterministic · Independently testable · Explainable · Confidence score · Trace/Provenance · Documented · Benchmarked.

## Do NOT

- Add LLM calls, randomness, or external opinion sources.
- Touch other engines or contexts.
- Decide product rules that aren't already specified — if the scoring logic is undefined, stop and ask; scaffold only.
