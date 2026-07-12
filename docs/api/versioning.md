# API Contract Versioning

> **Principle (ADR 0008):** the backend owns the API contract; the frontend
> consumes generated types only. This document defines how that contract is
> versioned, when it must be regenerated, what gets committed, and how CI
> guards against drift. See `contract-generation.md` for the mechanism and
> `evolution.md` for the additive-first change strategy.

## What "the contract" is

The contract is the backend's OpenAPI document (`packages/api-contracts/openapi.json`)
and the TypeScript types generated from it (`packages/api-contracts/src/schema.ts`).
The FastAPI application is the source of truth; both files are **generated
artifacts**.

## Generated code policy (absolute)

**Generated files must never be edited by hand.** This applies to:

- `packages/api-contracts/openapi.json`
- `packages/api-contracts/src/schema.ts`

To change either, change the **backend** (Pydantic models / routers) and
regenerate with `pnpm contracts:generate`. A manual edit will be silently
overwritten on the next regeneration and will fail CI drift validation. The
same rule holds for any future generated client. The generated header in
`schema.ts` ("Do not make direct changes to the file") is authoritative.

## Are generated contracts committed? — Yes, always

Both `openapi.json` and `schema.ts` are **committed** (they are not gitignored).
Reasons:

- The diff on `openapi.json` is the human-readable record of every contract
  change — it makes breaking changes visible in review.
- Committed types mean a fresh clone type-checks and builds without first
  running the backend to regenerate.
- CI can compare freshly-generated artifacts against the committed ones to
  detect drift (below).

Commit the regenerated artifacts **in the same commit** as the backend change
that caused them. Never commit a backend contract change without its
regenerated artifacts.

## When regeneration is required

Run `pnpm contracts:generate` (and commit the result) whenever any of these
change on the backend:

- A route is added, removed, or its path/method changes.
- A request or response Pydantic model changes (field added/removed/renamed, a
  type or nullability change, enum values, defaults that affect `required`).
- Status codes, response models, or `response_model` annotations change.
- Shared schemas referenced by endpoints change.

Regeneration is **not** required for changes that don't affect the OpenAPI
surface (internal refactors, docstrings that aren't surfaced, business logic
that doesn't alter the schema). When in doubt, run it — a no-op run produces no
diff (output is deterministic, sorted keys).

## Contract change classification

| Class | Examples | Version impact |
|---|---|---|
| **Additive (backward-compatible)** | New optional field; new endpoint; new enum value a client may ignore | Preferred. No consumer break. Regenerate + commit. |
| **Breaking** | Removing/renaming a field or route; narrowing a type; making an optional field required; changing status codes | Requires the migration process in `evolution.md`. Regenerate + commit; the frontend will fail to compile at every affected call site until updated (that compile failure is the guardrail working). |

## How CI validates contract drift (Milestone 7)

CI runs the generation pipeline and fails if the committed artifacts are stale:

1. `pnpm contracts:generate` (export OpenAPI from FastAPI → regenerate types).
2. `git diff --exit-code packages/api-contracts/openapi.json packages/api-contracts/src/schema.ts`.
3. A non-empty diff fails the build with a message to run `pnpm contracts:generate` and commit the result.

This guarantees the committed contract always matches the backend, and that no
one hand-edited a generated file. It complements import-linter (module
boundaries) as a mechanical architectural guardrail.
