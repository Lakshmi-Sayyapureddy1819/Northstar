"use client";

export interface SearchInputProps {
  value: string;
  onChange: (value: string) => void;
}

/**
 * Client-side name filter over the already-fetched nearby result set (≤50
 * companies, existing pagination convention) — not a new backend search
 * endpoint. Search by role/full-text is out of scope until Opportunity
 * exists (Slice 4).
 */
export function SearchInput({ value, onChange }: SearchInputProps) {
  return (
    <div className="flex-1">
      <label htmlFor="company-search" className="sr-only">
        Search companies
      </label>
      <input
        id="company-search"
        type="search"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Search companies…"
        className="w-full rounded-md border border-border bg-ns-surface px-3 py-2 text-sm text-foreground placeholder:text-ns-mist focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ns-gold"
      />
    </div>
  );
}
