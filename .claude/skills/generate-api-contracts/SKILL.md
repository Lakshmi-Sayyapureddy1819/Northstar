---
name: generate-api-contracts
description: Regenerate the frontend TypeScript API types from the backend OpenAPI schema. Use after any change to API endpoints or schemas. Enforces "API contracts are the single source of truth."
---

# generate-api-contracts

Regenerates `packages/api-contracts` from the FastAPI OpenAPI schema. Backend owns the contract; the frontend consumes generated types only. This Skill is deterministic — it transforms the schema, it makes no decisions.

## Steps

1. Ensure the API is exportable: obtain the current OpenAPI schema (export from the FastAPI app, e.g. a `just openapi` / `uv run` task that dumps `openapi.json`).
2. Generate TypeScript types into `packages/api-contracts/` from that schema.
3. Ensure `apps/web/lib/api/` consumes the generated types — never hand-written interfaces for API objects.
4. Run `tsc --noEmit` on `apps/web`; a drift between backend and frontend now surfaces as a type error.
5. Commit the regenerated types alongside the backend change (same change set).

## Rules

- **Backend is the source of truth.** If the frontend needs a new field, add it to the backend schema and regenerate — never patch the generated file.
- Do not hand-edit anything under `packages/api-contracts/`.
- Endpoints are documented by the OpenAPI schema itself; API *conventions* live in `docs/api/`.
