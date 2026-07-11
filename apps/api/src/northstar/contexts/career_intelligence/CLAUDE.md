# contexts/career_intelligence — The Career Intelligence Engine (CIE)

The **only** layer that makes objective recommendations. A registry of single-responsibility **deterministic** engines. This is the structural heart of "Facts First, AI Second."

## Every engine returns a standard `EngineResult`

```
Input (typed) → EngineResult {
    output:      <typed>       # the recommendation / computed values
    confidence:  float         # 0..1
    explanation: str           # human-readable, why this result
    trace:       Trace         # provenance back to the structured data used
    metadata:    dict          # timing, versions, inputs digest (for analytics)
}
```

## Engine Definition of Done (ALL required)

- [ ] **Deterministic** — same input → same output; no randomness, no LLM calls.
- [ ] **Independently testable** — unit-tested in isolation, no cross-engine dependency.
- [ ] **Explainable** — populates `explanation`.
- [ ] **Confidence score** — populates `confidence`.
- [ ] **Trace / Provenance** — populates `trace`; every number traces to structured data.
- [ ] **Documented** — `docs/engines/<name>.md` from `docs/engines/_template.md`.
- [ ] **Benchmarked** — a benchmark exists and is recorded.

## Adding an engine (use the `add-engine` Skill)

1. `engines/<name>/` with `domain/`, the engine implementing the common `Engine` contract, and tests.
2. Register in `registry.py` — the single wiring point.
3. Write the spec `docs/engines/<name>.md`.
4. **Do not modify existing engines.** Additive only.

## MVP engines

matching · ranking · salary · skill_gap · career_path · commute · company_scoring

## Future engines (additive, no rewrites)

Offer Comparison · Resume Scoring · Market Trend · Hiring Trend · Learning Recommendation

## Forbidden here

- No LLM calls. No non-determinism. No I/O to external opinion sources. Engines compute from structured data only.
