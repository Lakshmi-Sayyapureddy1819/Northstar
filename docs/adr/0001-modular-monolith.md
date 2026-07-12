# ADR 0001 — Modular monolith with enforced context boundaries

- **Status:** Accepted
- **Date:** 2026-07-12

## Context

NorthStar is a multi-subsystem platform built by a solo developer. Microservices
would impose operational and cognitive overhead unjustified at this stage, but a
conventional monolith tends to rot into a tangle that cannot later be split. We
need the low overhead of one deployable with boundaries strong enough to evolve
into services if scale ever demands it. This also encodes the Simplicity
principle: the simplest structure that supports two years of evolution.

## Decision

Build one FastAPI application partitioned into **bounded contexts** that
communicate only through an explicit public surface — each context's
`contract.py`. A context may import another context's `contract`, never its
internals. Within each context, dependencies point inward (Clean Architecture):
`infrastructure → application → domain`; domain and application never import
infrastructure. The boundary rule is enforced **mechanically** by import-linter,
not by convention.

## Consequences

- Boundaries are draw-once, not retrofitted; a context could later be extracted
  to a service with its contract as the seam.
- A violation fails CI, so the architecture cannot silently erode.
- Slight up-front ceremony (a `contract.py` per context, layered folders) that
  pays back in long-term maintainability.
- Simplicity is a first-class constraint: complexity is added only when a
  concrete need justifies it.

## As implemented

- 11 contexts under `apps/api/src/northstar/contexts/`, each with `contract.py`
  and `domain/`·`application/`·`infrastructure/`.
- Two import-linter contracts in `apps/api/pyproject.toml`: context
  *independence* (cross-context only via `contract`) and *layered* Clean
  Architecture — both enforced in CI (`.github/workflows/ci.yml`, backend job)
  and locally (`scripts/verify-phase0.sh`).
- `platform/` (technical foundation) and a deliberately small `shared_kernel/`
  (domain primitives) are kept distinct.
