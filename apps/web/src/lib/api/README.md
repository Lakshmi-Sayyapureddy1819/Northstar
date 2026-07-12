# lib/api — typed API client

`client.ts` exports `api`, an [`openapi-fetch`](https://openapi-ts.dev/openapi-fetch/)
client typed with the `paths` from `@northstar/api-contracts`. Those types are
**generated** from the backend OpenAPI schema — do not hand-write API request or
response interfaces anywhere in the web app.

Per ADR 0008 (API Contracts Are Truth): the backend owns the contract; the
frontend consumes generated types only. If the backend changes a contract,
regenerate (`pnpm contracts:generate` at the repo root) and any drift surfaces
as a TypeScript compile error.

Usage:

```ts
import { api } from "@/lib/api/client";

const { data, error } = await api.GET("/health");
// `data` is typed as the backend's HealthResponse — no local interface.
```
