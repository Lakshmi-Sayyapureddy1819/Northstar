# ADR 0005 — Facts First, AI Second

- **Status:** Accepted
- **Date:** 2026-07-12

## Context

NorthStar makes high-stakes claims — best next move, expected salary, skill gaps.
If an LLM computes these, they are unverifiable and prone to hallucination, which
is unacceptable for decisions people build careers on. We need recommendations
that are explainable, traceable, and defensible when challenged.

## Decision

**Deterministic engines produce truth; AI produces understanding.** Business
facts (matches, salary, skill gaps, commute, rankings, scores) are computed only
by deterministic domain engines with structured, explainable, traceable output.
The AI assistant (Polaris) consumes those structured outputs to explain,
summarize, compare, answer follow-ups, and personalize communication — it never
performs business calculations and cannot invent facts. This principle governs
every current and future AI feature.

## Consequences

- Every recommendation is traceable to structured data and defensible.
- The failure mode "the LLM made up a number" is structurally prevented, not
  merely discouraged.
- AI value (natural-language understanding) is retained without ceding
  correctness to it.

## As implemented

- The engine tier (`contexts/career_intelligence/`, ADR 0006) is the only
  recommender; Polaris (`contexts/polaris/`) may import other contexts' contracts
  (already-computed results) but has no path to compute facts.
- The boundary is stated emphatically in `contexts/polaris/CLAUDE.md` (Polaris
  explains, never computes) and `career_intelligence/CLAUDE.md` (no LLM calls,
  no non-determinism in engines).
- The `architecture-guardian` agent explicitly checks for business calculations
  outside the engine tier.
