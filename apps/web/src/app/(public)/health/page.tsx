import { Button } from "@northstar/ui";

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
      </dl>

      <div>
        <Button>Design-system button</Button>
      </div>

      <p className="text-xs text-muted-foreground">
        Backend liveness is served by the API at <code>/health</code>. It will be
        consumed here through the generated client (packages/api-contracts) after
        Milestone 6 — the frontend never hand-defines API types.
      </p>
    </main>
  );
}
