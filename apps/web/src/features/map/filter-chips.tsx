"use client";

import { industryChipLabel } from "./industry-color";
import type { NearbyCompany } from "./use-nearby-companies";

export interface FilterChipsProps {
  companies: NearbyCompany[];
  selected: string | null;
  onSelect: (industry: string | null) => void;
}

/**
 * Client-side industry filter — derived from the real, already-seeded
 * `Company.industry` field (no new backend field, no schema change). These
 * filter companies, not opportunities: there is still no `Opportunity` in
 * this slice (slice-3-map-experience.md, "Filter chips").
 */
export function FilterChips({ companies, selected, onSelect }: FilterChipsProps) {
  const labels = Array.from(
    new Set(companies.map((c) => industryChipLabel(c.industry))),
  ).sort();

  if (labels.length === 0) return null;

  return (
    <div
      role="group"
      aria-label="Filter companies by industry"
      className="flex flex-wrap gap-2"
    >
      {labels.map((label) => {
        const isActive = selected === label;
        return (
          <button
            key={label}
            type="button"
            aria-pressed={isActive}
            onClick={() => onSelect(isActive ? null : label)}
            className={`rounded-full border px-3 py-1 text-xs transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ns-gold ${
              isActive
                ? "border-ns-gold bg-ns-gold/10 text-ns-gold"
                : "border-border text-ns-mist hover:border-ns-gold/50"
            }`}
          >
            {label}
          </button>
        );
      })}
    </div>
  );
}
