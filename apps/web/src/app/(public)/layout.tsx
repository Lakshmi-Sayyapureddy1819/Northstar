import type { ReactNode } from "react";

/**
 * Public (anonymous-first) tier — ADR 0004.
 * No auth dependency; server-rendered and cacheable. The same core navigation
 * components render here and in the (app) tier; personalization is layered on top.
 */
export default function PublicLayout({ children }: { children: ReactNode }) {
  return <div data-tier="public">{children}</div>;
}
