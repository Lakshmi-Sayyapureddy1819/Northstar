---
name: add-provider
description: Scaffold a new ingestion JobProvider adapter (Greenhouse, Lever, career page, etc.). Use when adding a data source. Deterministic scaffolding only; enforces the legal-source and canonical-schema rules.
---

# add-provider

Scaffolds a new `JobProvider` adapter behind the ingestion port. Deterministic scaffolding — no product decisions.

## Inputs

- `<provider>` — snake_case provider name (e.g. `greenhouse`, `career_page`).

## Preconditions (STOP if violated)

- The source must be legal + maintainable. **Never** scaffold a scraper for LinkedIn, Naukri, or Indeed.
- Preferred order: official career pages → public ATS (Greenhouse/Lever/Ashby/Workable/SmartRecruiters) → public structured JobPosting metadata.

## Steps

1. Create `apps/api/src/northstar/contexts/ingestion/providers/<provider>/`:
   - `adapter.py` — implements the `JobProvider` port; maps raw source data → the **canonical Opportunity schema**.
   - `mapping.py` — the field mapping, kept isolated.
   - `tests/test_<provider>.py` — fixture-driven; assert canonical output shape, provenance, and dedup keys.
2. Register in `contexts/ingestion/providers/registry.py` with the capability manifest: rate limits, freshness, **legal basis**, dedup keys.
3. Ensure **provenance** (source lineage retained) and **dedup** (collapses duplicates to one canonical opportunity) are populated.
4. Add onboarding steps to `docs/runbooks/ingestion-provider-onboarding.md`.
5. **Do not modify core or other providers.** Additive only.

## Do NOT

- Reach into `opportunities`, `companies`, or `geo` internals — normalize into the canonical schema and stop.
- Scrape prohibited sources.
