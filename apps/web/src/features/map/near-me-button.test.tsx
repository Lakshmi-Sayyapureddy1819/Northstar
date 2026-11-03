import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { NearMeButton } from "./near-me-button";

const originalGeolocation = navigator.geolocation;

afterEach(() => {
  Object.defineProperty(navigator, "geolocation", {
    value: originalGeolocation,
    configurable: true,
  });
  vi.restoreAllMocks();
});

function mockGeolocation(
  impl: (success: PositionCallback, error?: PositionErrorCallback) => void,
) {
  Object.defineProperty(navigator, "geolocation", {
    value: { getCurrentPosition: vi.fn(impl) },
    configurable: true,
  });
}

describe("NearMeButton", () => {
  it("calls onLocated when permission is granted", async () => {
    mockGeolocation((success) => {
      success({
        coords: { latitude: 17.44, longitude: 78.35 } as GeolocationCoordinates,
      } as GeolocationPosition);
    });
    const onLocated = vi.fn();
    render(<NearMeButton onLocated={onLocated} />);

    screen.getByRole("button", { name: /near me/i }).click();

    await waitFor(() => expect(onLocated).toHaveBeenCalledWith(17.44, 78.35));
  });

  it("shows a visible message when permission is denied — never a blank state", async () => {
    mockGeolocation((_success, error) => {
      error?.({ code: 1, PERMISSION_DENIED: 1 } as GeolocationPositionError);
    });
    render(<NearMeButton onLocated={vi.fn()} />);

    screen.getByRole("button", { name: /near me/i }).click();

    expect(await screen.findByRole("status")).toHaveTextContent(/denied/i);
  });

  it("shows a visible message when geolocation is unsupported", async () => {
    Object.defineProperty(navigator, "geolocation", {
      value: undefined,
      configurable: true,
    });
    render(<NearMeButton onLocated={vi.fn()} />);

    screen.getByRole("button", { name: /near me/i }).click();

    expect(await screen.findByRole("status")).toHaveTextContent(/isn't supported/i);
  });
});
