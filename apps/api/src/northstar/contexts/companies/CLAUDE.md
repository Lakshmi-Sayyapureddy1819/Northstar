# contexts/companies — Company as Aggregate Root

Read the root `CLAUDE.md` and `apps/api/CLAUDE.md` first. This context owns
`Company`, the central entity many future capabilities (opportunities,
offices/geo, company intelligence, reviews, Career Universe, Polaris
knowledge) will hang off without ever redesigning it.

## Identity: stable ID, mutable slug

- `CompanyId` (UUID-backed) is the **only** identity. It's what `Opportunity`
  (Slice 2) references, what other contexts hold across the `contract.py`
  boundary, and what never changes for a company's lifetime.
- `CompanySlug` is a **separate**, mutable value object for URLs/SEO. A rename
  regenerates the slug; every existing `CompanyId` reference stays valid.
  Never use the slug as a foreign key or identity anywhere.

## Extending the aggregate — additive, not speculative

`Company` (Slice 1) ships only the fields it needs today: name, description,
industry, website, careers page, founded year. Future slices attach new
capability by **adding** — never by renaming, restructuring, or repurposing
what already shipped:

- Slice 4 (`geo`) adds offices/locations — modeled as a related concept the
  `companies` contract can expose (e.g. `CompanyDetail.offices`), not as
  lat/lng fields bolted onto `Company` itself.
- Slice 5 (Company Intelligence) adds factual fields (team size bucket,
  funding stage, tech stack, growth signal) as new optional attributes on
  `CompanyDetail` — existing consumers of the Slice-1 shape keep working
  unchanged.
- Anything further out (reviews, benefits, ESG, hiring velocity, campus
  hiring, internship/articleship programs, Career Universe node data, Polaris
  knowledge) follows the same rule: a new optional field or a new related
  value object, added when its slice actually needs it — never a speculative
  column today.

If a change would require renaming or removing something already shipped in
`contract.py`, that's a breaking change — follow `docs/api/evolution.md`
(expand → migrate → contract), not a silent edit.

## What NOT to do

- Don't duplicate company fields into another context's models (e.g.
  `opportunities` must hold a `CompanyId`, never a copy of `name`/`industry`).
- Don't add fields for a capability that isn't being implemented this slice.
- Don't let `CompanySlug` become identity anywhere — it's for URLs only.
