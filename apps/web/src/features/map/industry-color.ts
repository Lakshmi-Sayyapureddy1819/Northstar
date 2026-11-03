/**
 * Deterministic industry -> accent color, used to tint career-node markers
 * and filter chips. Derived from `Company.industry` (real Slice-1 data) —
 * not a fabricated taxonomy. One consistent node glyph, color-varied by a
 * real field (Visual Design Direction, slice-3-map-experience.md).
 */
const PALETTE = ["#D9A552", "#4FB6A8", "#8A93A8", "#C77B5A", "#6F9CEB", "#B387C7"];

/** A short, stable hash so the same industry string always maps to the same color. */
function hash(value: string): number {
  let h = 0;
  for (let i = 0; i < value.length; i += 1) {
    h = (h << 5) - h + value.charCodeAt(i);
    h |= 0;
  }
  return Math.abs(h);
}

export function colorForIndustry(industry: string): string {
  return PALETTE[hash(industry) % PALETTE.length];
}

/** A short label set derived from the real seeded industries, for filter chips. */
export function industryChipLabel(industry: string): string {
  // "Software Engineering & AI/ML" -> "Software Engineering"; keep the first
  // clause so chips stay short ("very little text" — Visual Design Direction).
  return industry.split("&")[0]?.trim() ?? industry;
}
