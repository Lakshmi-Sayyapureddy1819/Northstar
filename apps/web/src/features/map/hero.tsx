"use client";

import { FilterChips } from "./filter-chips";
import { LocalityPicker } from "./locality-picker";
import { NearMeButton } from "./near-me-button";
import { SearchInput } from "./search-input";
import type { NearbyCompany } from "./use-nearby-companies";

export interface HeroProps {
  searchValue: string;
  onSearchChange: (value: string) => void;
  localityValue: string;
  onLocalityChange: (name: string) => void;
  onNearMe: (latitude: number, longitude: number) => void;
  companies: NearbyCompany[];
  selectedIndustry: string | null;
  onSelectIndustry: (industry: string | null) => void;
}

/**
 * The first five seconds (Vision, slice-3-map-experience.md): wordmark,
 * display headline, and every control needed before the map even loads —
 * compact, not pushing the map below the fold on desktop.
 */
export function Hero({
  searchValue,
  onSearchChange,
  localityValue,
  onLocalityChange,
  onNearMe,
  companies,
  selectedIndustry,
  onSelectIndustry,
}: HeroProps) {
  return (
    <header className="mx-auto flex max-w-5xl flex-col gap-4 px-6 pb-6 pt-10">
      <p className="font-ui text-sm font-semibold tracking-wide text-ns-gold">
        NorthStar
      </p>
      <div>
        <h1 className="font-display text-3xl font-medium tracking-tight text-foreground sm:text-4xl">
          Your career has a location.
        </h1>
        <p className="mt-2 text-base text-ns-mist">
          Discover opportunities around you.
        </p>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <SearchInput value={searchValue} onChange={onSearchChange} />
        <LocalityPicker value={localityValue} onChange={onLocalityChange} />
        <NearMeButton onLocated={onNearMe} />
      </div>

      <FilterChips
        companies={companies}
        selected={selectedIndustry}
        onSelect={onSelectIndustry}
      />
    </header>
  );
}
