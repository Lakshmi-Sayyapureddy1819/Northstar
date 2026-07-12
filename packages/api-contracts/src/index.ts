/**
 * Public entrypoint for the generated API contracts.
 *
 * Backend owns the contract (ADR 0008). `schema.ts` is generated from
 * `openapi.json` by `pnpm --filter @northstar/api-contracts generate` — never
 * hand-edit it. Consumers import these types (and nothing hand-written) to talk
 * to the API in a type-safe way.
 */
export type { components, operations, paths } from "./schema";
