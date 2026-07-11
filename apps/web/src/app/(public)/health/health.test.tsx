import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import HealthPage from "./page";

describe("HealthPage", () => {
  it("renders the web status heading", () => {
    render(<HealthPage />);
    expect(screen.getByRole("heading", { name: /web status/i })).toBeInTheDocument();
  });

  it("renders the design-system button", () => {
    render(<HealthPage />);
    expect(
      screen.getByRole("button", { name: /design-system button/i }),
    ).toBeInTheDocument();
  });
});
