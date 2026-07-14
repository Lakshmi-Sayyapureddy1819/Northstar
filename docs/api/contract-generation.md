# API Contract Generation

> **Principle (ADR 0008):** the backend owns the API contract; the frontend
> consumes generated types only. No hand-written API interfaces exist in the web
> app. Drift between backend and frontend becomes a **compile error**, not a
> runtime surprise.

This is the Milestone 6 mechanism that makes that principle real.

## The pipeline

```
FastAPI app (source of truth)
   │  app.openapi()                     apps/api/scripts/export_openapi.py
   ▼
packages/api-contracts/openapi.json     (committed artifact — reviewable diffs)
   │  openapi-typescript                pnpm --filter @northstar/api-contracts generate
   ▼
packages/api-contracts/src/schema.ts    (generated types: paths, components, operations)
   │  export type { paths, … }          packages/api-contracts/src/index.ts
   ▼
apps/web/src/lib/api/client.ts          createClient<paths>()  (openapi-fetch)
   │
   ▼
feature code                            api.GET("/health") → response typed from the contract
```

## One command

```bash
pnpm contracts:generate     # from the repo root
```

This runs, in order:

1. `pnpm openapi:export` → `(cd apps/api && uv run python scripts/export_openapi.py)` — serializes `app.openapi()` (sorted keys) to `packages/api-contracts/openapi.json`.
2. `pnpm --filter @northstar/api-contracts run generate` → `openapi-typescript ./openapi.json --output ./src/schema.ts`.

`apps/api` is a Python project (not a pnpm workspace), so the export step is a subshell rather than a `--filter` target.

## Rules

- **Never hand-edit** `packages/api-contracts/src/schema.ts` or `openapi.json` — they are generated. Both are `.prettierignore`d for the same reason.
- **Never hand-write API request/response interfaces** in the web app. Import types from `@northstar/api-contracts` (via the `openapi-fetch` client), which infers them from `paths`.
- To change the contract: change the **backend** (Pydantic models / routes), then run `pnpm contracts:generate` and commit the regenerated `openapi.json` + `schema.ts` alongside the backend change.
- CI regenerates and fails if the committed artifacts are stale (wired in Milestone 7).

## How the "drift = compile error" guarantee works

`apps/web/src/lib/api/client.ts` types the client with the generated `paths`:

```ts
import type { paths } from "@northstar/api-contracts";
import createClient from "openapi-fetch";
export const api = createClient<paths>({ baseUrl });
```

Every call site (`api.GET("/health")`, …) is typed from that. If the backend
removes a field, changes a type, or renames a route, regenerating updates
`schema.ts`, and `tsc --noEmit` on the web app fails anywhere the old shape was
assumed — surfacing the break at build time.

## Verified (Milestone 6)

- OpenAPI export from FastAPI succeeds (`openapi: 3.1.0`, `/health`, `HealthResponse`).
- Type generation succeeds (`paths`, `components`, `operations`).
- The web app builds against the generated types (`next build` green; `/health` consumes the typed client).
- A backend contract change flows through: adding a field to `HealthResponse` regenerated `schema.ts` with the new field; reverting removed it.

## Verified (Phase 1, Slice 1 — first real endpoints)

- `GET /companies` and `GET /companies/{company_id}` regenerated the contract
  cleanly (`paths: /companies, /companies/{company_id}, /health`); `tsc --noEmit`
  on `apps/web` stayed green against the new `schema.ts` with no manual changes.
- This is the first time the pipeline carried a real pagination envelope and a
  path parameter (`company_id`) — see `docs/api/pagination.md` for the
  convention it established.
- Slice Boundary Review (pre-merge): confirmed both endpoints are thin HTTP
  wrappers over `companies` application use cases only — no reach into any
  other context, no business logic in the router. Nothing about the exposed
  surface (`CompanySummaryResponse`/`CompanyDetailResponse`) changed as a
  result of the review; the one fix it produced (removing the unused
  `SqlAlchemyCompanyReader` adapter) was internal to `companies` and does not
  touch the API contract.
