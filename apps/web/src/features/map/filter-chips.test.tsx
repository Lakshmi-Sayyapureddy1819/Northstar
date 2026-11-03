import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { FilterChips } from "./filter-chips";
import type { NearbyCompany } from "./use-nearby-companies";

function company(industry: string): NearbyCompany {
  return {
    id: industry,
    slug: industry,
    name: industry,
    industry,
    description: "",
    latitude: 0,
    longitude: 0,
    distanceKm: 0,
  };
}

describe("FilterChips", () => {
  it("derives deduplicated chip labels from real seeded industries", () => {
    render(
      <FilterChips
        companies={[
          company("AI/ML & Data"),
          company("AI/ML & Data"),
          company("Fintech"),
        ]}
        selected={null}
        onSelect={vi.fn()}
      />,
    );
    expect(screen.getAllByRole("button")).toHaveLength(2);
    expect(screen.getByRole("button", { name: "AI/ML" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Fintech" })).toBeInTheDocument();
  });

  it("toggles selection off when the active chip is clicked again", () => {
    const onSelect = vi.fn();
    render(
      <FilterChips
        companies={[company("Fintech")]}
        selected="Fintech"
        onSelect={onSelect}
      />,
    );
    screen.getByRole("button", { name: "Fintech" }).click();
    expect(onSelect).toHaveBeenCalledWith(null);
  });
});
