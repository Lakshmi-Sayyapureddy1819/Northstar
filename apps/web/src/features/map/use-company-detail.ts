"use client";

import { useEffect, useState } from "react";

import { api } from "@/lib/api/client";

export interface CompanyDetail {
  id: string;
  slug: string;
  name: string;
  description: string;
  industry: string;
  website: string;
  careersPageUrl: string | null;
  foundedYear: number | null;
}

export type CompanyDetailState =
  | { kind: "idle" }
  | { kind: "loading" }
  | { kind: "error" }
  | { kind: "ready"; company: CompanyDetail };

/** Fetches `GET /companies/{company_id}` for the detail panel/page. */
export function useCompanyDetail(companyId: string | null): CompanyDetailState {
  const [state, setState] = useState<CompanyDetailState>({ kind: "idle" });

  useEffect(() => {
    if (!companyId) {
      setState({ kind: "idle" });
      return;
    }
    let cancelled = false;
    setState({ kind: "loading" });
    api
      .GET("/companies/{company_id}", { params: { path: { company_id: companyId } } })
      .then(({ data }) => {
        if (cancelled) return;
        if (!data) {
          setState({ kind: "error" });
          return;
        }
        setState({ kind: "ready", company: toDetail(data) });
      })
      .catch(() => {
        if (!cancelled) setState({ kind: "error" });
      });
    return () => {
      cancelled = true;
    };
  }, [companyId]);

  return state;
}

function toDetail(data: {
  id: string;
  slug: string;
  name: string;
  description: string;
  industry: string;
  website: string;
  careers_page_url: string | null;
  founded_year: number | null;
}): CompanyDetail {
  return {
    id: data.id,
    slug: data.slug,
    name: data.name,
    description: data.description,
    industry: data.industry,
    website: data.website,
    careersPageUrl: data.careers_page_url,
    foundedYear: data.founded_year,
  };
}
