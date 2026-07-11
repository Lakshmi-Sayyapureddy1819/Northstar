# contexts/ingestion — Source-Agnostic Ingestion

Pluggable data ingestion. The platform must never depend on a single source.

## The `JobProvider` port

Every source is an independent adapter behind the `JobProvider` port, normalizing into ONE **canonical Opportunity schema**. Nothing downstream (opportunities, matching, geo) knows or cares where a posting came from.

```
providers/
├── <provider>/        # e.g. greenhouse/, lever/, ashby/, career_page/
│   └── adapter.py     # implements JobProvider; maps raw → canonical
└── registry.py        # capability manifest: rate limits, freshness, legal basis, dedup keys
```

## First-class concerns

- **Provenance** — every canonical opportunity retains source lineage.
- **Dedup** — the same role from two sources collapses to one canonical opportunity.
- **Legal basis** — recorded per provider in the capability manifest.

## Preferred source order (legal + maintainable first)

1. Official company career pages
2. Public ATS providers (Greenhouse, Lever, Ashby, Workable, SmartRecruiters)
3. Public structured JobPosting metadata
4. Employer-submitted [future]
5. User-contributed [future]

## Hard rule

**Never** scrape LinkedIn, Naukri, or Indeed. Adding a provider = new adapter + registry entry + `docs/runbooks/ingestion-provider-onboarding.md` steps. Never a change to core. Use the `add-provider` Skill.
