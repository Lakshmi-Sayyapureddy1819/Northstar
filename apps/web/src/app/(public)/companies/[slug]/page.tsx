import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { api } from "@/lib/api/client";

interface PageProps {
  params: Promise<{ slug: string }>;
}

/**
 * Deep-linkable, server-rendered company detail page — the
 * shareable/SEO-crawlable path (Core tier, ADR 0004). The map's inline
 * detail panel is the fast in-context path; this route is the real,
 * indexable URL. See slice-3-map-experience.md, "Company detail panel."
 */
export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const { data } = await api.GET("/companies/by-slug/{slug}", {
    params: { path: { slug } },
  });
  if (!data) return { title: "Company not found — NorthStar" };
  return { title: `${data.name} — NorthStar`, description: data.description };
}

export default async function CompanyDetailPage({ params }: PageProps) {
  const { slug } = await params;
  const { data, response } = await api.GET("/companies/by-slug/{slug}", {
    params: { path: { slug } },
  });

  if (response.status === 404 || !data) {
    notFound();
  }

  return (
    <main className="mx-auto flex max-w-2xl flex-col gap-4 px-6 py-12">
      <p className="text-sm text-ns-mist">{data.industry}</p>
      <h1 className="font-display text-3xl font-medium text-foreground">{data.name}</h1>
      <p className="text-foreground">{data.description}</p>

      <dl className="mt-2 grid grid-cols-[auto_1fr] gap-x-3 gap-y-1 text-sm">
        {data.founded_year && (
          <>
            <dt className="text-ns-mist">Founded</dt>
            <dd className="font-mono">{data.founded_year}</dd>
          </>
        )}
      </dl>

      <div className="mt-4 flex flex-col gap-2">
        <a
          href={data.website}
          target="_blank"
          rel="noreferrer"
          className="text-sm font-medium text-ns-gold hover:underline"
        >
          Visit website ↗
        </a>
        {data.careers_page_url && (
          <a
            href={data.careers_page_url}
            target="_blank"
            rel="noreferrer"
            className="text-sm font-medium text-ns-gold hover:underline"
          >
            Careers page ↗
          </a>
        )}
      </div>
    </main>
  );
}
