"use client";

import { useEffect, useState } from "react";

import { api } from "@/lib/api/client";

export interface NearbyCompany {
  id: string;
  slug: string;
  name: string;
  industry: string;
  description: string;
  latitude: number;
  longitude: number;
  distanceKm: number;
}

export type NearbyCompaniesState =
  | { kind: "loading" }
  | { kind: "error" }
  | { kind: "ready"; companies: NearbyCompany[] };

/**
 * Fetches `GET /companies/nearby` through the generated, typed client
 * (ADR 0008) — no hand-written response interface. Re-fetches whenever the
 * origin/radius changes (locality picked, "Near Me" resolved).
 */
export function useNearbyCompanies(
  latitude: number,
  longitude: number,
  radiusKm: number,
): NearbyCompaniesState {
  const [state, setState] = useState<NearbyCompaniesState>({ kind: "loading" });

  useEffect(() => {
    let cancelled = false;
    setState({ kind: "loading" });
    api
      .GET("/companies/nearby", {
        params: { query: { lat: latitude, lng: longitude, radius_km: radiusKm } },
      })
      .then(({ data }) => {
        if (cancelled) return;
        if (!data) {
          setState({ kind: "error" });
          return;
        }
        setState({
          kind: "ready",
          companies: data.items.map((item) => ({
            id: item.id,
            slug: item.slug,
            name: item.name,
            industry: item.industry,
            description: item.description,
            latitude: item.latitude,
            longitude: item.longitude,
            distanceKm: item.distance_km,
          })),
        });
      })
      .catch(() => {
        if (!cancelled) setState({ kind: "error" });
      });
    return () => {
      cancelled = true;
    };
  }, [latitude, longitude, radiusKm]);

  return state;
}
