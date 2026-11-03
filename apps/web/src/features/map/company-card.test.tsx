import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { CompanyCard } from "./company-card";
import type { NearbyCompany } from "./use-nearby-companies";

const company: NearbyCompany = {
  id: "1",
  slug: "darwinbox",
  name: "Darwinbox",
  industry: "HR Tech & AI/ML",
  description: "HR tech startup.",
  latitude: 17.43,
  longitude: 78.37,
  distanceKm: 2.1,
};

describe("CompanyCard", () => {
  it("renders name, locality, industry, and distance", () => {
    render(
      <CompanyCard
        company={company}
        locality="Raidurg"
        selected={false}
        onSelect={vi.fn()}
      />,
    );
    expect(screen.getByRole("heading", { name: "Darwinbox" })).toBeInTheDocument();
    expect(screen.getByText(/raidurg/i)).toBeInTheDocument();
    expect(screen.getByText(/hr tech/i)).toBeInTheDocument();
    expect(screen.getByText("2.1 km")).toBeInTheDocument();
  });

  it("never renders a fabricated star rating — only the honest reserved slot", () => {
    render(
      <CompanyCard
        company={company}
        locality="Raidurg"
        selected={false}
        onSelect={vi.fn()}
      />,
    );
    expect(screen.queryByText(/★/)).not.toBeInTheDocument();
    expect(screen.getByText(/career score — coming soon/i)).toBeInTheDocument();
  });

  it("calls onSelect with the company id when clicked", () => {
    const onSelect = vi.fn();
    render(
      <CompanyCard
        company={company}
        locality="Raidurg"
        selected={false}
        onSelect={onSelect}
      />,
    );
    screen.getByRole("button").click();
    expect(onSelect).toHaveBeenCalledWith("1");
  });
});
