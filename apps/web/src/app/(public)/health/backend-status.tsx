"use client";

import { useEffect, useState } from "react";

import { api } from "@/lib/api/client";

/**
 * Live backend liveness, fetched through the generated, typed client.
 *
 * The response shape is inferred from `@northstar/api-contracts` (generated from
 * the backend OpenAPI schema) — there is no hand-written interface for it here.
 * Fetch is client-side with a graceful fallback so a production build never
 * depends on a running API.
 */
export function BackendStatus() {
  const [state, setState] = useState<
    | { kind: "loading" }
    | { kind: "unavailable" }
    | { kind: "ok"; status: string; environment: string; version: string }
  >({ kind: "loading" });

  useEffect(() => {
    let cancelled = false;
    api
      .GET("/health")
      .then(({ data }) => {
        if (cancelled) return;
        // `data` is typed as HealthResponse from the generated contract.
        setState(
          data
            ? {
                kind: "ok",
                status: data.status,
                environment: data.environment,
                version: data.version,
              }
            : { kind: "unavailable" },
        );
      })
      .catch(() => {
        if (!cancelled) setState({ kind: "unavailable" });
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (state.kind === "loading") {
    return (
      <dd aria-live="polite" className="text-muted-foreground">
        checking…
      </dd>
    );
  }
  if (state.kind === "unavailable") {
    return (
      <dd aria-live="polite" className="text-muted-foreground">
        unavailable
      </dd>
    );
  }
  return (
    <dd aria-live="polite">
      {state.status} · {state.environment} · v{state.version}
    </dd>
  );
}
