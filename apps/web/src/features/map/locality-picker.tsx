"use client";

import { LOCALITIES } from "./localities";

export interface LocalityPickerProps {
  value: string;
  onChange: (localityName: string) => void;
}

/**
 * A real, labeled, keyboard-operable control over the seven known
 * localities — not a map-only gesture (Accessibility, Search by location —
 * slice-3-map-experience.md).
 */
export function LocalityPicker({ value, onChange }: LocalityPickerProps) {
  return (
    <label className="flex items-center gap-2 text-sm text-ns-mist">
      <span aria-hidden="true">📍</span>
      <span className="sr-only">Search by locality</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="rounded-md border border-border bg-ns-surface px-2 py-1.5 text-foreground focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ns-gold"
      >
        <option value="Hyderabad">Hyderabad</option>
        {LOCALITIES.map((locality) => (
          <option key={locality.name} value={locality.name}>
            {locality.name}
          </option>
        ))}
      </select>
    </label>
  );
}
