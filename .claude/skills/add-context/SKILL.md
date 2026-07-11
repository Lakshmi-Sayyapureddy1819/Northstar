---
name: add-context
description: Scaffold a new bounded context in the API with Clean Architecture layers and a contract.py public surface. Use when introducing a new domain area. Deterministic scaffolding only.
---

# add-context

Scaffolds a new bounded context so it conforms to the modular-monolith boundary rules from birth.

## Inputs

- `<name>` — snake_case context name.
- Tier — Core (identity-agnostic) | Personalization (auth-gated) | (Polaris is fixed).

## Preconditions

- A new context is an architectural decision. Confirm an ADR exists or is being written (`update-adr`). If not, STOP — architecture changes begin with an ADR.

## Steps

1. Create `apps/api/src/northstar/contexts/<name>/`:
   - `domain/` — entities, value objects, pure logic.
   - `application/` — use cases orchestrating domain + ports.
   - `infrastructure/` — repositories, adapters (implement ports; may use `platform/`).
   - `contract.py` — the ONLY public surface. Export just what other contexts may consume.
   - `tests/`
2. Add the context to the import-linter configuration so cross-context access is restricted to `contract.py`.
3. If it exposes HTTP, add a thin router under `apps/api/src/northstar/api/routers/<name>.py` and regenerate contracts (`generate-api-contracts`).
4. Create/refresh `docs/architecture/bounded-contexts.md` entry and a local `CLAUDE.md` if the context has special rules.

## Rules

- Dependencies point inward; domain/application never import infrastructure.
- Core-tier contexts must remain identity-agnostic.
- No cross-context import except via `contract.py`.
