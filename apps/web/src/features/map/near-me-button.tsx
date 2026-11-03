"use client";

import { Button } from "@northstar/ui";

import { useGeolocation } from "./use-geolocation";

export interface NearMeButtonProps {
  onLocated: (latitude: number, longitude: number) => void;
}

/**
 * "Near Me" — browser Geolocation, permission-gated, always resolves to a
 * visible state (never a silent failure or blank map). See "Near Me" in
 * slice-3-map-experience.md.
 */
export function NearMeButton({ onLocated }: NearMeButtonProps) {
  const { state, locate } = useGeolocation();

  function handleClick() {
    locate();
  }

  const message =
    state.kind === "denied"
      ? "Location access denied — showing Hyderabad instead."
      : state.kind === "unsupported"
        ? "Location isn't supported in this browser."
        : state.kind === "error"
          ? "Couldn't get your location — showing Hyderabad instead."
          : null;

  // Fire the callback once a position resolves.
  if (state.kind === "granted") {
    onLocated(state.latitude, state.longitude);
  }

  return (
    <div className="flex flex-col gap-1">
      <Button
        type="button"
        variant="outline"
        onClick={handleClick}
        disabled={state.kind === "locating"}
        aria-describedby={message ? "near-me-status" : undefined}
      >
        {state.kind === "locating" ? "Locating…" : "Near Me"}
      </Button>
      {message && (
        <p
          id="near-me-status"
          role="status"
          aria-live="polite"
          className="text-xs text-ns-mist"
        >
          {message}
        </p>
      )}
    </div>
  );
}
