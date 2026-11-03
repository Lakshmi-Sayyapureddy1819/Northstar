"use client";

import { motion, useReducedMotion } from "framer-motion";
import dynamic from "next/dynamic";
import { useMemo, useState } from "react";

import { CareerUniverseCta } from "./career-universe-cta";
import { CompanyDetailPanel } from "./company-detail-panel";
import { Hero } from "./hero";
import { DEFAULT_RADIUS_KM, HYDERABAD_CENTER, LOCALITIES } from "./localities";
import { NearbyList } from "./nearby-list";
import { useNearbyCompanies } from "./use-nearby-companies";

// Mapbox GL requires `window`/WebGL — client-only, off the critical
// rendering path for LCP (Performance goals, slice-3-map-experience.md).
const MapView = dynamic(() => import("./map-view").then((m) => m.MapView), {
  ssr: false,
  loading: () => (
    <div
      role="status"
      aria-label="Loading map"
      className="flex h-full w-full items-center justify-center bg-ns-surface text-sm text-ns-mist"
    >
      Loading map…
    </div>
  ),
});

export function HomeExperience() {
  // Framer Motion animations must degrade gracefully under reduced motion
  // (apps/web/CLAUDE.md) — the global CSS rule only catches native
  // animation/transition properties, not JS-driven motion, so this is
  // handled explicitly.
  const prefersReducedMotion = useReducedMotion();
  const [localityName, setLocalityName] = useState<string>(HYDERABAD_CENTER.name);
  const [origin, setOrigin] = useState({
    latitude: HYDERABAD_CENTER.latitude,
    longitude: HYDERABAD_CENTER.longitude,
  });
  const [search, setSearch] = useState("");
  const [selectedIndustry, setSelectedIndustry] = useState<string | null>(null);
  const [selectedCompanyId, setSelectedCompanyId] = useState<string | null>(null);

  const nearby = useNearbyCompanies(
    origin.latitude,
    origin.longitude,
    DEFAULT_RADIUS_KM,
  );
  const companies = useMemo(
    () => (nearby.kind === "ready" ? nearby.companies : []),
    [nearby],
  );

  const filtered = useMemo(() => {
    return companies.filter((c) => {
      const matchesSearch = c.name.toLowerCase().includes(search.toLowerCase());
      const matchesIndustry =
        !selectedIndustry || c.industry.includes(selectedIndustry);
      return matchesSearch && matchesIndustry;
    });
  }, [companies, search, selectedIndustry]);

  function handleLocalityChange(name: string) {
    setLocalityName(name);
    const locality = LOCALITIES.find((l) => l.name === name) ?? HYDERABAD_CENTER;
    setOrigin({ latitude: locality.latitude, longitude: locality.longitude });
  }

  function handleNearMe(latitude: number, longitude: number) {
    setLocalityName("Near me");
    setOrigin({ latitude, longitude });
  }

  function handleSelect(companyId: string) {
    setSelectedCompanyId(companyId);
  }

  return (
    <div className="min-h-screen">
      <Hero
        searchValue={search}
        onSearchChange={setSearch}
        localityValue={localityName}
        onLocalityChange={handleLocalityChange}
        onNearMe={handleNearMe}
        companies={companies}
        selectedIndustry={selectedIndustry}
        onSelectIndustry={setSelectedIndustry}
      />

      <main>
        <motion.div
          initial={prefersReducedMotion ? false : { opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: prefersReducedMotion ? 0 : 0.6 }}
          className="mx-auto h-[60vh] max-w-6xl px-6"
        >
          <div className="h-full w-full overflow-hidden rounded-xl border border-border">
            <MapView
              companies={filtered}
              center={origin}
              selectedCompanyId={selectedCompanyId}
              onSelectCompany={handleSelect}
            />
          </div>
        </motion.div>

        <section className="mx-auto max-w-6xl px-6 py-8">
          <h2 className="mb-4 font-display text-xl font-medium text-foreground">
            Nearby Companies
          </h2>
          {nearby.kind === "error" && (
            <p role="alert" className="text-sm text-ns-mist">
              Couldn&apos;t load nearby companies. Try again shortly.
            </p>
          )}
          {nearby.kind === "loading" && (
            <p role="status" className="text-sm text-ns-mist">
              Loading nearby companies…
            </p>
          )}
          {nearby.kind === "ready" && (
            <NearbyList
              companies={filtered}
              selectedCompanyId={selectedCompanyId}
              onSelect={handleSelect}
            />
          )}
        </section>

        <CareerUniverseCta />
      </main>

      <CompanyDetailPanel
        companyId={selectedCompanyId}
        onClose={() => setSelectedCompanyId(null)}
      />
    </div>
  );
}
