import { Button } from "@northstar/ui";

import { BackendStatus } from "./backend-status";

export default function HealthPage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col justify-center gap-6 px-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Web Status</h1>
        <p className="mt-2 text-muted-foreground">The NorthStar web app is running.</p>
      </div>

      <dl className="grid grid-cols-2 gap-2 text-sm">
        <dt className="text-muted-foreground">Frontend</dt>
        <dd>ok</dd>
        <dt className="text-muted-foreground">Design system</dt>
        <dd>@northstar/ui linked</dd>
        <dt className="text-muted-foreground">Backend</dt>
        <BackendStatus />
      </dl>

      <div>
        <Button>Design-system button</Button>
      </div>

      <p className="text-xs text-muted-foreground">
        Backend liveness at <code>/health</code> is consumed through the typed client in{" "}
        <code>lib/api</code>, whose types are generated from the backend OpenAPI schema
        (<code>packages/api-contracts</code>). The frontend never hand-defines API types
        (ADR 0008).
      </p>
    </main>
  );
}
