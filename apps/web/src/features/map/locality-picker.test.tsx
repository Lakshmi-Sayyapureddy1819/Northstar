import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { LocalityPicker } from "./locality-picker";

describe("LocalityPicker", () => {
  it("lists Hyderabad plus all seven seeded localities", () => {
    render(<LocalityPicker value="Hyderabad" onChange={vi.fn()} />);
    const select = screen.getByRole("combobox", { name: /search by locality/i });
    const options = Array.from(select.querySelectorAll("option")).map(
      (o) => o.textContent,
    );
    expect(options).toEqual([
      "Hyderabad",
      "Madhapur",
      "Hitech City",
      "Gachibowli",
      "Financial District",
      "Kondapur",
      "Raidurg",
      "Nanakramguda",
    ]);
  });

  it("calls onChange with the selected locality", () => {
    const onChange = vi.fn();
    render(<LocalityPicker value="Hyderabad" onChange={onChange} />);
    fireEvent.change(screen.getByRole("combobox", { name: /search by locality/i }), {
      target: { value: "Gachibowli" },
    });
    expect(onChange).toHaveBeenCalledWith("Gachibowli");
  });
});
