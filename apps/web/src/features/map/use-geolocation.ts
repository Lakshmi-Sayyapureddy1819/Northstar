"use client";

import { useCallback, useState } from "react";

export type GeolocationState =
  | { kind: "idle" }
  | { kind: "locating" }
  | { kind: "granted"; latitude: number; longitude: number }
  | { kind: "denied" }
  | { kind: "unsupported" }
  | { kind: "error"; message: string };

/**
 * Wraps the browser Geolocation API for the "Near Me" control. Gated on the
 * browser's own permission prompt — no account, no login (ADR 0004). Every
 * failure path (denied, unsupported, error) resolves to a distinct state so
 * the UI never shows a blank/broken map — see slice-3-map-experience.md's
 * "Near Me" acceptance criteria.
 */
export function useGeolocation() {
  const [state, setState] = useState<GeolocationState>({ kind: "idle" });

  const locate = useCallback(() => {
    if (typeof navigator === "undefined" || !navigator.geolocation) {
      setState({ kind: "unsupported" });
      return;
    }
    setState({ kind: "locating" });
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setState({
          kind: "granted",
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        });
      },
      (error) => {
        if (error.code === error.PERMISSION_DENIED) {
          setState({ kind: "denied" });
        } else {
          setState({ kind: "error", message: error.message });
        }
      },
      { timeout: 8000 },
    );
  }, []);

  return { state, locate };
}
