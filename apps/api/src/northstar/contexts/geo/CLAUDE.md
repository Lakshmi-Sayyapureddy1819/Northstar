# contexts/geo — Location as a First-Class Value Object

Read the root `CLAUDE.md` and `apps/api/CLAUDE.md` first.

## One location per company (MVP)

`company_locations` is keyed by `company_id` (primary key = FK to
`companies.id`) — one `Location` per company. Multiple offices per company is
an additive extension for whenever a real need justifies it (more rows per
`CompanyId`, not a redesign) — don't model it before then.

## `Location`, never raw lat/lng

Every other context and every future geo feature (nearby query, commute
engine, …) depends on `geo.contract.Location`, not on bare
latitude/longitude floats. `geo`'s own domain validates the ranges once, at
construction — don't re-validate ad hoc elsewhere.

## What's deliberately not here yet (Slice 2)

- **No nearby-query use case.** `find_nearby` (candidate `CompanyId`s → those
  within a radius, ordered by distance) is Slice 3's job. Don't add it early.
- **No read port/adapter for other contexts.** `geo.contract` exposes only
  `Location` this slice — no `CompanyLocationReader` — because nothing
  outside `geo` consumes it yet. Build the port when Slice 3 actually needs
  one (same lesson as Slice 1's removed `SqlAlchemyCompanyReader`).
- **`geo` doesn't know what a "company" is.** It only ever receives an opaque
  `CompanyId` (imported from `companies.contract`) — never a `Company`.
