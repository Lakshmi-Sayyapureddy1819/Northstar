# @northstar/api-contracts

TypeScript types generated from the backend OpenAPI schema. **Backend owns the
contract (ADR 0008); the frontend consumes these types only.**

## ⚠️ Generated code — never edit by hand

These files are generated. Do **not** edit them manually:

- `openapi.json` — exported from the FastAPI app (`app.openapi()`).
- `src/schema.ts` — generated from `openapi.json` by `openapi-typescript`.

A manual edit is overwritten on the next regeneration and fails CI drift
validation. `src/index.ts` (the hand-written public re-export of the generated
types) is the only file here you may edit.

## Regenerate

From the repo root, after any backend contract change:

```bash
pnpm contracts:generate
```

This exports the OpenAPI schema from FastAPI, regenerates `src/schema.ts`, and
you commit both artifacts alongside the backend change.

## Consuming these types

Import from the package entrypoint; never hand-write API interfaces:

```ts
import type { paths } from "@northstar/api-contracts";
```

The web app wires these into an `openapi-fetch` client — see
`apps/web/src/lib/api/client.ts`.

## See also

- `docs/api/contract-generation.md` — the full pipeline.
- `docs/api/versioning.md` — versioning, generated-code policy, CI drift.
- `docs/api/evolution.md` — additive-first evolution and breaking-change migration.
