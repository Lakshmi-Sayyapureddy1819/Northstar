---
name: update-documentation
description: Update NorthStar documentation to match a code change, enforcing the Living Documentation Definition of Done. Use as part of completing any feature or change.
---

# update-documentation

Keeps documentation in lockstep with code (Living Documentation). A feature is not complete until docs are updated.

## Where each kind of change is documented

| Change | Doc home |
|--------|----------|
| Business/feature spec | `docs/product/prd.md`, `docs/product/user-flows.md` |
| New/changed engine | `docs/engines/<name>.md` (from `_template.md`) |
| New/changed context or boundary | `docs/architecture/bounded-contexts.md` |
| API convention (versioning, auth, errors, pagination, filtering, rate limits) | `docs/api/` |
| Persistence (schema, ERD, migrations, PostGIS, pgvector) | `docs/database/` |
| AI (Polaris, LLM Port, prompts, guardrails, eval) | `docs/ai/` |
| Endpoints themselves | the OpenAPI schema (source of truth) — regenerate contracts |
| Architectural decision | a new ADR (`update-adr`) |

## Steps

1. Identify which doc homes the change touches (table above).
2. Update them in the **same change** as the code.
3. If an architectural decision changed, ensure a new ADR exists (`update-adr`) — docs alone are not enough for architecture changes.
4. Verify features still trace to `docs/product/prd.md`.

## Definition of Done reminder

Implementation + passing tests + updated docs + ADRs (when architecture changes). All four, or the feature is not done.
