/**
 * Typed API client — the ONLY way the web app talks to the backend.
 *
 * Types come from `@northstar/api-contracts`, generated from the backend's
 * OpenAPI schema (ADR 0008: backend owns the contract). We never hand-write API
 * request/response interfaces here — `openapi-fetch` derives request shapes,
 * params, and response types from the generated `paths`.
 */
import type { paths } from "@northstar/api-contracts";
import createClient from "openapi-fetch";

const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export const api = createClient<paths>({ baseUrl });
