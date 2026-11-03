"use client";

import { colorForIndustry } from "./industry-color";
import type { NearbyCompany } from "./use-nearby-companies";

export interface CompanyCardProps {
  company: NearbyCompany;
  locality: string | null;
  selected: boolean;
  onSelect: (companyId: string) => void;
}

/**
 * Premium card treatment (Visual Design Direction,
 * slice-3-map-experience.md): name, locality, industry, distance, and a
 * reserved-but-honest "Career Score" slot. No fabricated star rating —
 * there is no real score yet (Slice 5 / Phase 3 CIE), so inventing one here
 * would quietly break Facts-First (ADR 0005) two slices early.
 */
export function CompanyCard({
  company,
  locality,
  selected,
  onSelect,
}: CompanyCardProps) {
  return (
    <button
      type="button"
      onClick={() => onSelect(company.id)}
      aria-pressed={selected}
      className={`w-full rounded-lg border border-border bg-ns-surface px-4 py-3 text-left transition-colors hover:border-ns-gold/60 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ns-gold ${
        selected ? "border-ns-gold" : ""
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <span
              aria-hidden="true"
              className="inline-block h-2.5 w-2.5 rounded-full"
              style={{ backgroundColor: colorForIndustry(company.industry) }}
            />
            <h3 className="font-display text-base font-medium text-foreground">
              {company.name}
            </h3>
          </div>
          {locality && (
            <p className="mt-1 text-sm text-ns-mist">
              <span aria-hidden="true">📍 </span>
              {locality}
            </p>
          )}
          <p className="mt-1 text-sm text-ns-mist">{company.industry}</p>
        </div>
        <span className="whitespace-nowrap font-mono text-xs text-ns-mist">
          {company.distanceKm.toFixed(1)} km
        </span>
      </div>

      {/* Reserved for Slice 5's real Career Score — never a fabricated rating. */}
      <p className="mt-2 font-mono text-xs text-ns-mist/70">
        Career Score — coming soon
      </p>

      <span className="mt-2 inline-block text-sm font-medium text-ns-gold">
        View Company →
      </span>
    </button>
  );
}
