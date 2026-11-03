"use client";

import { CompanyCard } from "./company-card";
import { LOCALITIES } from "./localities";
import type { NearbyCompany } from "./use-nearby-companies";

export interface NearbyListProps {
  companies: NearbyCompany[];
  selectedCompanyId: string | null;
  onSelect: (companyId: string) => void;
}

/** Approximate nearest known locality label for a card — display only. */
function nearestLocalityName(lat: number, lng: number): string | null {
  let closest: { name: string; distSq: number } | null = null;
  for (const locality of LOCALITIES) {
    const distSq = (locality.latitude - lat) ** 2 + (locality.longitude - lng) ** 2;
    if (!closest || distSq < closest.distSq) closest = { name: locality.name, distSq };
  }
  return closest?.name ?? null;
}

/**
 * The fully keyboard/screen-reader-complete path to every company —
 * independent of the map (Accessibility, slice-3-map-experience.md). This
 * list must never be gated behind the map widget.
 */
export function NearbyList({
  companies,
  selectedCompanyId,
  onSelect,
}: NearbyListProps) {
  if (companies.length === 0) {
    return (
      <p className="px-1 py-6 text-sm text-ns-mist">
        No companies found in this area. Try a different locality or a wider radius.
      </p>
    );
  }

  return (
    <ul aria-label="Nearby companies" className="flex flex-col gap-2">
      {companies.map((company) => (
        <li key={company.id}>
          <CompanyCard
            company={company}
            locality={nearestLocalityName(company.latitude, company.longitude)}
            selected={company.id === selectedCompanyId}
            onSelect={onSelect}
          />
        </li>
      ))}
    </ul>
  );
}
