"use client";

import "mapbox-gl/dist/mapbox-gl.css";

import { useReducedMotion } from "framer-motion";
import { useCallback, useEffect, useMemo, useRef } from "react";
import Map, {
  type MapRef,
  Layer,
  type LayerProps,
  type MapMouseEvent,
  Source,
} from "react-map-gl/mapbox";

import { colorForIndustry } from "./industry-color";
import { HYDERABAD_CENTER } from "./localities";
import type { NearbyCompany } from "./use-nearby-companies";

const MAPBOX_TOKEN = process.env.NEXT_PUBLIC_MAPBOX_TOKEN ?? "";

export interface MapViewProps {
  companies: NearbyCompany[];
  center: { latitude: number; longitude: number };
  selectedCompanyId: string | null;
  onSelectCompany: (companyId: string) => void;
}

// Career nodes, not default Mapbox pins: a soft glow (halo) circle beneath a
// solid core circle, tinted per-industry — Visual Design Direction,
// slice-3-map-experience.md.
const glowLayer: LayerProps = {
  id: "career-node-glow",
  type: "circle",
  filter: ["!", ["has", "point_count"]],
  paint: {
    "circle-radius": 16,
    "circle-color": ["get", "color"],
    "circle-opacity": 0.25,
    "circle-opacity-transition": { duration: 600 },
  },
};

const coreLayer: LayerProps = {
  id: "career-node-core",
  type: "circle",
  filter: ["!", ["has", "point_count"]],
  paint: {
    "circle-radius": ["case", ["boolean", ["feature-state", "selected"], false], 8, 6],
    "circle-color": ["get", "color"],
    "circle-stroke-width": 1.5,
    "circle-stroke-color": "#0B0F1A",
    "circle-opacity-transition": { duration: 600 },
  },
};

const clusterGlowLayer: LayerProps = {
  id: "cluster-glow",
  type: "circle",
  filter: ["has", "point_count"],
  paint: {
    "circle-radius": ["step", ["get", "point_count"], 22, 5, 28, 15, 34],
    "circle-color": "#D9A552",
    "circle-opacity": 0.2,
  },
};

const clusterLayer: LayerProps = {
  id: "clusters",
  type: "circle",
  filter: ["has", "point_count"],
  paint: {
    "circle-radius": ["step", ["get", "point_count"], 14, 5, 18, 15, 22],
    "circle-color": "#D9A552",
    "circle-stroke-width": 1.5,
    "circle-stroke-color": "#0B0F1A",
  },
};

const clusterCountLayer: LayerProps = {
  id: "cluster-count",
  type: "symbol",
  filter: ["has", "point_count"],
  layout: {
    "text-field": "{point_count_abbreviated}",
    "text-size": 12,
    "text-font": ["Open Sans Regular"],
  },
  paint: {
    "text-color": "#0B0F1A",
  },
};

interface ClusterSource {
  getClusterExpansionZoom(
    clusterId: number,
    callback: (error: unknown, zoom: number) => void,
  ): void;
}

/**
 * Client-only Mapbox GL view (dynamic-imported by the caller with
 * `ssr:false` — Mapbox GL needs `window`/WebGL). Native GeoJSON clustering,
 * no extra clustering library, per slice-3-map-experience.md.
 */
export function MapView({
  companies,
  center,
  selectedCompanyId,
  onSelectCompany,
}: MapViewProps) {
  const mapRef = useRef<MapRef | null>(null);
  const selectedFeatureId = useRef<string | null>(null);
  const prefersReducedMotion = useReducedMotion();

  const geojson = useMemo(
    () => ({
      type: "FeatureCollection" as const,
      features: companies.map((c) => ({
        type: "Feature" as const,
        id: c.id,
        properties: { companyId: c.id, color: colorForIndustry(c.industry) },
        geometry: {
          type: "Point" as const,
          coordinates: [c.longitude, c.latitude],
        },
      })),
    }),
    [companies],
  );

  const handleClick = useCallback(
    (event: MapMouseEvent) => {
      const map = mapRef.current?.getMap();
      const feature = event.features?.[0];
      if (!map || !feature) return;

      if (feature.properties?.cluster) {
        const source = map.getSource("companies") as unknown as
          ClusterSource | undefined;
        const coordinates =
          feature.geometry.type === "Point" ? feature.geometry.coordinates : undefined;
        if (!coordinates) return;
        source?.getClusterExpansionZoom(feature.properties.cluster_id, (err, zoom) => {
          if (err) return;
          map.easeTo({ center: coordinates as [number, number], zoom, duration: 500 });
        });
        return;
      }

      const companyId = feature.properties?.companyId as string | undefined;
      if (companyId) onSelectCompany(companyId);
    },
    [onSelectCompany],
  );

  const handleLoad = useCallback(() => {
    const map = mapRef.current?.getMap();
    if (!map) return;
    // Reduced-motion users get the final view immediately — no camera
    // fly-in forced on them (Accessibility, slice-3-map-experience.md).
    map.flyTo({
      center: [center.longitude, center.latitude],
      zoom: 11,
      duration: prefersReducedMotion ? 0 : 1400,
    });
  }, [center, prefersReducedMotion]);

  // Sync Mapbox feature-state so the selected card's node visibly grows —
  // "clicking a card focuses the marker" (slice-3-map-experience.md).
  useEffect(() => {
    const map = mapRef.current?.getMap();
    if (!map || !map.getSource("companies")) return;
    if (selectedFeatureId.current !== null) {
      map.setFeatureState(
        { source: "companies", id: selectedFeatureId.current },
        { selected: false },
      );
    }
    if (selectedCompanyId) {
      map.setFeatureState(
        { source: "companies", id: selectedCompanyId },
        { selected: true },
      );
    }
    selectedFeatureId.current = selectedCompanyId;
  }, [selectedCompanyId, geojson]);

  if (!MAPBOX_TOKEN) {
    return (
      <div
        role="status"
        className="flex h-full w-full items-center justify-center bg-ns-surface text-sm text-ns-mist"
      >
        Map unavailable — missing NEXT_PUBLIC_MAPBOX_TOKEN.
      </div>
    );
  }

  return (
    <Map
      ref={mapRef}
      mapboxAccessToken={MAPBOX_TOKEN}
      initialViewState={{
        longitude: HYDERABAD_CENTER.longitude,
        latitude: HYDERABAD_CENTER.latitude,
        zoom: 9,
      }}
      style={{ width: "100%", height: "100%" }}
      mapStyle="mapbox://styles/mapbox/dark-v11"
      interactiveLayerIds={["clusters", "career-node-core"]}
      onClick={handleClick}
      onLoad={handleLoad}
    >
      <Source
        id="companies"
        type="geojson"
        data={geojson}
        cluster
        clusterMaxZoom={13}
        clusterRadius={50}
      >
        <Layer {...clusterGlowLayer} />
        <Layer {...clusterLayer} />
        <Layer {...clusterCountLayer} />
        <Layer {...glowLayer} />
        <Layer {...coreLayer} />
      </Source>
    </Map>
  );
}
