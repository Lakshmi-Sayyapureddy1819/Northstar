# lib/api — generated API client

This directory holds the typed API client the frontend uses to talk to the
backend. It is **generated** from the backend OpenAPI schema (see
`packages/api-contracts`) in **Milestone 6** — do not hand-write API types here.

Per ADR 0008 (API Contracts Are Truth): the backend owns the contract; the
frontend consumes generated types only. Drift becomes a compile error.
