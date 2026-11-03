"use client";

import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import Link from "next/link";
import { useEffect, useRef } from "react";

import { useCompanyDetail } from "./use-company-detail";

export interface CompanyDetailPanelProps {
  companyId: string | null;
  onClose: () => void;
}

/**
 * Inline detail panel (fast path, no navigation) — the deep-linkable path
 * is `/companies/[slug]` (see app/(public)/companies/[slug]/page.tsx). Only
 * Slice-1 fields render here; Slice 5's Company Intelligence fields don't
 * exist yet (slice-3-map-experience.md).
 */
export function CompanyDetailPanel({ companyId, onClose }: CompanyDetailPanelProps) {
  const state = useCompanyDetail(companyId);
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const prefersReducedMotion = useReducedMotion();

  useEffect(() => {
    if (companyId) closeButtonRef.current?.focus();
  }, [companyId]);

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") onClose();
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [onClose]);

  return (
    <AnimatePresence>
      {companyId && (
        <motion.aside
          role="dialog"
          aria-modal="true"
          aria-label="Company detail"
          initial={prefersReducedMotion ? false : { x: "100%" }}
          animate={{ x: 0 }}
          exit={prefersReducedMotion ? undefined : { x: "100%" }}
          transition={{ duration: prefersReducedMotion ? 0 : 0.25, ease: "easeOut" }}
          className="fixed inset-y-0 right-0 z-50 w-full max-w-md overflow-y-auto border-l border-border bg-ns-surface p-6 shadow-xl"
        >
          <button
            ref={closeButtonRef}
            type="button"
            onClick={onClose}
            aria-label="Close company detail"
            className="mb-4 rounded-md border border-border px-3 py-1 text-sm text-ns-mist hover:text-foreground focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ns-gold"
          >
            Close ✕
          </button>

          {state.kind === "loading" && (
            <p role="status" className="text-sm text-ns-mist">
              Loading…
            </p>
          )}
          {state.kind === "error" && (
            <p role="alert" className="text-sm text-ns-mist">
              Couldn&apos;t load this company. Try again.
            </p>
          )}
          {state.kind === "ready" && (
            <div className="flex flex-col gap-3">
              <h2 className="font-display text-2xl font-medium text-foreground">
                {state.company.name}
              </h2>
              <p className="text-sm text-ns-mist">{state.company.industry}</p>
              <p className="text-foreground">{state.company.description}</p>
              <dl className="mt-2 grid grid-cols-[auto_1fr] gap-x-3 gap-y-1 text-sm">
                {state.company.foundedYear && (
                  <>
                    <dt className="text-ns-mist">Founded</dt>
                    <dd className="font-mono">{state.company.foundedYear}</dd>
                  </>
                )}
              </dl>
              <div className="mt-4 flex flex-col gap-2">
                <a
                  href={state.company.website}
                  target="_blank"
                  rel="noreferrer"
                  className="text-sm font-medium text-ns-gold hover:underline"
                >
                  Visit website ↗
                </a>
                {state.company.careersPageUrl && (
                  <a
                    href={state.company.careersPageUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="text-sm font-medium text-ns-gold hover:underline"
                  >
                    Careers page ↗
                  </a>
                )}
                <Link
                  href={`/companies/${state.company.slug}`}
                  className="text-sm text-ns-mist hover:text-foreground"
                >
                  Open shareable page →
                </Link>
              </div>
            </div>
          )}
        </motion.aside>
      )}
    </AnimatePresence>
  );
}
