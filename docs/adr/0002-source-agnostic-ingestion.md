# ADR 0002 — Source-agnostic, pluggable data ingestion

- **Status:** Accepted
- **Date:** 2026-07-12

## Context

A hyperlocal career-navigation platform lives or dies on its data. Depending on
a single source is both a resilience risk and a legal one. Scraping LinkedIn /
Naukri / Indeed carries ToS and legal exposure and is operationally brittle. We
need data acquisition modeled so sources are interchangeable and adding one
never destabilizes the rest of the platform.

## Decision

Model ingestion behind a `JobProvider` port. Each source is an independent
adapter that normalizes into one **canonical Opportunity schema**, with
**provenance** and **dedup** as first-class concerns. Prefer legal, maintainable
sources in this order: (1) official company career pages, (2) public ATS
providers (Greenhouse, Lever, Ashby, Workable, SmartRecruiters), (3) public
structured JobPosting metadata, (4) employer-submitted [future], (5)
user-contributed [future]. **Never** design around scraping LinkedIn, Naukri, or
Indeed. Adding a provider is a new adapter + registry entry — never a core
change.

## Consequences

- Nothing downstream (opportunities, matching, geo) knows or cares where a
  posting came from.
- Legal posture is explicit and per-provider (recorded in the capability
  manifest).
- New providers are additive; the core is untouched (additive-extensibility
  goal).

## As implemented

- `contexts/ingestion/` with a `providers/` extension point and `contract.py`;
  the context is isolated behind its contract (ADR 0001).
- The rule and provider-onboarding procedure are documented in
  `contexts/ingestion/CLAUDE.md`; the `add-provider` skill scaffolds new
  adapters and refuses prohibited sources.
- Canonical schema, provenance, and dedup are the ingestion domain's
  responsibility (implemented incrementally from Phase 1; the boundary and port
  exist in Phase 0).
