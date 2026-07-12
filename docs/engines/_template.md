# Engine Spec — `<engine_name>`

> Template for every Career Intelligence Engine (ADR 0006). Copy to
> `docs/engines/<engine_name>.md` and fill in. **Writing this spec is step one of
> adding an engine** (before code) — the `add-engine` skill and the doc-drift
> hook both expect a spec per engine. Sections mirror the `EngineResult`
> envelope.

## Purpose

One or two sentences: what objective question this engine answers. Deterministic
only — no LLM calls, no randomness, no external opinion sources.

## Input

The typed input model. Fields, types, units, and where each comes from
(structured data / other contexts' contracts).

## Output

The typed output model — the computed recommendation/values. Types and meaning.

## Confidence

How the `confidence` score (0..1) is derived and what it means for this engine
(e.g. data completeness, match strength). When it is low, and why.

## Explanation

What the human-readable `explanation` contains and how it is constructed from the
inputs — enough for a user (or Polaris) to understand *why* this result.

## Trace / Provenance

Exactly which structured data and computation steps produced the output, so any
number traces back to its source.

## Metadata

Non-authoritative extras recorded for analytics (timings, versions, input
digest, feature flags).

## Determinism & tests

State the determinism guarantee (same input → same output) and list the unit
tests that prove it, plus the benchmark (accuracy/latency against a fixture set).

## Definition of Done

- [ ] Deterministic
- [ ] Independently testable
- [ ] Explainable
- [ ] Confidence score
- [ ] Trace / Provenance
- [ ] Documented (this file)
- [ ] Benchmarked
- [ ] Registered in `contexts/career_intelligence/registry.py`
