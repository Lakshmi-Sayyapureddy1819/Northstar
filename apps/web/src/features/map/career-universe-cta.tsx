/**
 * Visibly present but disabled — zero Phase 2 logic, no route, no
 * component behind it. A static, honest signal of what's next
 * (slice-3-map-experience.md, "Future hook").
 */
export function CareerUniverseCta() {
  return (
    <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-10">
      <span
        aria-disabled="true"
        title="Coming soon"
        className="inline-flex cursor-not-allowed items-center gap-2 font-display text-lg text-ns-mist"
      >
        Explore Career Universe →
        <span className="rounded-full border border-border px-2 py-0.5 font-ui text-xs uppercase tracking-wide text-ns-mist">
          Coming Soon
        </span>
      </span>
    </div>
  );
}
