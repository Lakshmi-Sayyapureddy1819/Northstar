import type { ReactNode } from "react";

/**
 * App (auth-gated) tier — ADR 0004.
 * Personalization layered on top of the anonymous core (dashboard, GPS,
 * resume, tracking). The auth gate itself arrives with the Identity phase.
 */
export default function AppLayout({ children }: { children: ReactNode }) {
  return <div data-tier="app">{children}</div>;
}
