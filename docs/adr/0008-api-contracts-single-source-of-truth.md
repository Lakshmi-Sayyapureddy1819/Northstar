# ADR 0008 — API contracts as the single source of truth

- **Status:** Accepted
- **Date:** 2026-07-12

## Context

Frontend and backend drift is a classic source of runtime bugs. Hand-written API
types on the frontend inevitably diverge from the backend. With strong typing as
a project standard, that drift should be impossible rather than merely
discouraged.

## Decision

The **backend owns the contract**. The FastAPI app is the source of truth; it
emits the OpenAPI schema, from which the frontend's TypeScript types are
**generated** into `packages/api-contracts`. The frontend consumes only those
generated types and **never hand-writes API interfaces**. Generated artifacts
(`openapi.json`, `schema.ts`) are committed and never hand-edited. CI regenerates
and fails on drift. Change the contract by changing the backend, then regenerate.

## Consequences

- Backend↔frontend drift becomes a compile error, caught before merge.
- A fresh clone type-checks and builds without first running the backend.
- The `openapi.json` diff is the human-readable record of every contract change.

## As implemented

- `apps/api/scripts/export_openapi.py` serializes `app.openapi()` (sorted keys)
  → `packages/api-contracts/openapi.json`; `openapi-typescript` generates
  `src/schema.ts`; `src/index.ts` re-exports the types.
- One command: `pnpm contracts:generate` (root `package.json`).
- `apps/web/src/lib/api/client.ts` is an `openapi-fetch` client typed with the
  generated `paths`; the health page consumes the typed `/health` with no local
  interface.
- CI `contracts` job regenerates and runs `git diff --exit-code`; verified
  end-to-end in Milestone 6 (a backend field change flowed through to the
  generated types) and re-checked by `scripts/verify-phase0.sh`.
- Documented in `docs/api/{contract-generation,versioning,evolution}.md` and
  `packages/api-contracts/README.md`.
