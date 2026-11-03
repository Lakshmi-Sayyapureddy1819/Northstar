# Phase 1, Slice 3 — Map Experience (Feature Specification)

> **Status:** Approved and implemented. Backend and frontend both complete
> and verified — see "As implemented" notes throughout and
> `docs/roadmap/phase-1.md`'s Slice 3 section for the full verification
> record. Parent spec: `docs/features/phase1/hyperlocal-career-navigation.md`.
> Builds on `phase1-slice1` (Company) and `phase1-slice2` (Location/geo seed
> data, tagged and committed). Traces to `docs/product/prd.md` and
> `docs/product/mvp-scope.md`. Builds inside ADRs 0001–0009 — no new bounded
> context, no new import-linter contract, no ADR change.

## Vision

This is the slice where NorthStar becomes visible and becomes itself. Someone
opens `localhost:3100` and, within one screen, understands "Google Maps for
Careers" — not from a tagline, but from seeing real Hyderabad companies
plotted on a real map, with no login wall in the way. Everything built in
Slices 1–2 (a real `Company` aggregate, real geolocated data for 30 real
companies) has been leading to this moment. The first five seconds should
land the idea; the visual identity should be memorable enough that no one
mistakes a screenshot of this for a generic job board or an admin dashboard.

## Visual Design Direction

Calibration points named directly: **Apple Maps + Airbnb + Linear + Arc
Browser** — clean, spacious, map-dominant, very little text. Explicitly
avoid the "admin dashboard" failure mode (sidebar + map + data table +
buttons). This section fixes a concrete design language before
implementation so the build doesn't drift into generic defaults.

The root CLAUDE.md's own design language ("subtle navigation/universe
metaphor... enterprise-quality and elegant, never game-like") already gives
this a real subject to draw from: **wayfinding instruments** — star charts,
compass roses, coordinate readouts, brass sextants — not generic sci-fi or a
literal starfield.

**Color** (named, to become CSS custom properties in `globals.css` when
implemented):

- `--ns-ink` `#0B0F1A` — near-black indigo, the map/hero background (a night
sky, not a pure black).
- `--ns-surface` `#141B2E` — elevated surface (cards, the nearby-list panel).
- `--ns-mist` `#8A93A8` — muted secondary text, body copy on dark.
- `--ns-paper` `#F3F1EA` — warm off-white, used for light-mode surfaces and
high-contrast text on dark.
- `--ns-gold` `#D9A552` — the North Star accent: brand mark, primary CTA,
the default career-node glow. Used deliberately sparingly.
- `--ns-teal` `#4FB6A8` — secondary accent for map/location UI (the locality
picker, "Near Me," distance labels) — keeps "wayfinding" visually distinct
from "brand/CTA."

**Type** — three roles, none of them the default-everywhere Inter:

- **Display** (hero headline, section labels): a warm, confident serif with
real character (e.g. Fraunces) — used sparingly, just the hero line and
major section headers. This is what makes "Your career has a location."
read as a statement, not a caption.
- **UI/body** (nav, buttons, card text, copy): a clean, precise humanist sans
(e.g. General Sans) — the Linear/Arc-browser register: quiet, confident,
never decorative.
- **Utility/data** (coordinates, distances, the reserved score slot): a
monospace (e.g. IBM Plex Mono or JetBrains Mono) for anything that reads
like an instrument readout — `2.3 km`, `17.44°N`, a future score value.
This is a deliberate structural device: monospace numerals signal "this is
measured data," distinct from prose.

**Layout concept** — the exact stacked structure requested (hero → map →
nearby list → CTA), executed spaciously rather than densely:

```
┌──────────────────────────────────────────────┐
│  NorthStar                                     │
│                                                │
│  Your career has a location.        (Fraunces)│
│  Discover opportunities around you.            │
│                                                │
│  [ Search companies...      ] 📍Hyderabad▾ [Near Me]│
│  ○ AI/ML  ○ Fintech  ○ Enterprise  ○ Semiconductors │  (filter chips)
├──────────────────────────────────────────────┤
│                                                │
│              full-bleed live map              │
│         (career nodes, not map pins)           │
│                                                │
├──────────────────────────────────────────────┤
│  Nearby Companies                              │
│  ✦ Google        📍 Gachibowli                 │
│  ✦ Microsoft     📍 Gachibowli                 │
│  ✦ Darwinbox     📍 Raidurg                    │
├──────────────────────────────────────────────┤
│  Explore Career Universe →        Coming Soon  │
└──────────────────────────────────────────────┘
```

**Signature element** — the one thing this page is remembered by: **career
nodes that glow and gently pulse like distant stars**, rendered with the
`--ns-gold` (or, per category — see "Career nodes" below) glow, replacing
Mapbox's default pin entirely. This is the single deliberate risk: everything
else on the page stays quiet and disciplined so this one visual idea reads
clearly, and it's the literal seed of Phase 2's "nodes become planets."

## Problem Statement

Right now `localhost:3100` shows the Phase 0 placeholder page
(`apps/web/src/app/(public)/page.tsx` — a static title and tagline, no data).
30 real, geolocated companies exist in the database (Slice 2) with a fully
working API (Slice 1), but nothing renders them. There is no map, no company
card, no detail view, and no way to search by location or find what's
nearby. This slice must turn real backend data into the product's actual
first impression — anonymous, fast, and honest about what exists today
(no Career Universe, no AI, no accounts) while gesturing at what's coming.

## Goals

1. Replace the Phase 0 placeholder home page with the real, memorable
  landing experience: hero framing ("Discover opportunities around you" /
   Hyderabad), a live map, a nearby-companies list, and a **disabled**
   "Explore Career Universe →" call-to-action that previews Phase 2 without
   implementing anything from it.
2. Integrate Mapbox GL JS, showing all 30 seeded companies as markers,
  clustered when zoomed out.
3. Ship company cards (from the map or the nearby list) that open a company
  detail panel/page with the Slice-1 factual profile.
4. Ship two ways to change what "nearby" means: **search by location**
  (picking one of the seven known Hyderabad tech localities) and **"Near
   Me"** (browser geolocation, permission-gated, graceful fallback).
5. Make it responsive (mobile → desktop) and meet explicit performance and
  accessibility bars — not "make it work," but make it fast and usable by
   keyboard/screen-reader users too.
6. Add exactly one new backend capability: a nearby-companies query, closing
  the loop Slice 2 opened (`company_locations` has been queryable via raw
   SQL since Slice 2's verification; this slice wraps it in a real
   application use case and API endpoint).

## Non-goals (explicitly out of scope for this slice)

- **Search by role** — there is no `Opportunity` yet (Slice 4, later in the
revised order). Only location-based search/filtering exists this slice.
- `**Opportunity` modeling, Mapbox routing/directions, commute times** — not
this slice.
- **The Career Universe itself** — only a disabled/"Coming Soon" CTA that
visually gestures at it. Zero Phase 2 logic, components, or routes.
- **Company Intelligence fields** (team size, funding stage, tech stack,
growth signal) on the detail panel — Slice 5. The detail view shows only
Slice-1 factual fields this slice.
- **Auth, saved searches, personalization** — everything here is anonymous,
`(public)` tier, per ADR 0004.
- **Free-text geocoding search** — "search by location" is a curated picker
over the seven known localities (the actual shape of our seed data), not a
general geocoder. See "Search by location" below for why.
- **D3 or a custom map renderer** — Mapbox GL JS only, per
`apps/web/CLAUDE.md`'s visualization roadmap.

## Personas

Unchanged from the parent spec — this is the slice where all three
(Anonymous Active Explorer, Final-Year Student, Relocating Professional)
finally get a real screen to use.

## User Stories

- As any anonymous visitor, I want to open the site and immediately
understand "this is a map of careers near me," so I don't mistake it for
another job board.
- As an anonymous visitor, I want to see companies plotted on a real map,
clustered when there are many close together, so the map stays readable
rather than a wall of overlapping pins.
- As an anonymous visitor, I want to click a company (marker or card) and see
its real profile — description, industry, website, careers link — so I can
go from "where" to "what" without leaving the page.
- As an anonymous visitor, I want to pick a known Hyderabad tech locality
(e.g. "Gachibowli") and see the map/list re-center on companies there, so I
can explore by area without typing a fuzzy search query.
- As an anonymous visitor, I want a "Near Me" option that uses my actual
location (with my permission) to show what's nearby, so I don't have to
know Hyderabad's neighborhood names at all.
- As a mobile visitor, I want the same experience to work well on a phone —
map and list don't fight each other for space — so the product isn't
desktop-only.
- As a keyboard or screen-reader user, I want to reach every company's
information without being able to operate the map itself, so the product
isn't gated behind a widget I can't use.
- As any visitor, I want to see a hint that there's more coming (Career
Universe) without it pretending to work today, so the product's ambition
is visible without being misleading.

## Acceptance Criteria

### Mapbox integration

- Mapbox GL JS (via `react-map-gl`, the maintained React wrapper) renders a
map centered on Hyderabad, loaded **client-side only** (dynamic import,
`ssr: false` — Mapbox GL requires `window`/WebGL, incompatible with Next.js
server rendering).
- Mapbox access token read from a `NEXT_PUBLIC_`-prefixed env var (Next.js's
required convention for client-exposed env vars — see "Risks" for how this
reconciles with ADR 0003's `NORTHSTAR_`-prefix backend convention).
Never hardcoded, never committed.

### Public home page

- `apps/web/src/app/(public)/page.tsx` is replaced entirely (no more Phase 0
placeholder), stacked in this exact order (see Visual Design Direction's
wireframe): **hero** (wordmark, "Your career has a location." display
headline, "Discover opportunities around you" subhead, a search input, the
locality picker, "Near Me," and the industry filter chips) → **full-bleed
live map** → **Nearby Companies** list → **Explore Career Universe →**
footer CTA. Map dominates the vertical space; hero controls are compact
and don't push the map below the fold on desktop.
- Built in `features/map/` per the feature-first convention
(`apps/web/CLAUDE.md`) — no business-specific UI added to `packages/ui`.
- No login wall anywhere on this page or the detail view (ADR 0004). No
sidebar, no data table, no admin-dashboard chrome — map-dominant, spacious,
minimal text, per Visual Design Direction.

### Career nodes (custom markers) + clustering + map animation

- **No default Mapbox pins.** Every company renders as a **career node**: a
single consistent glyph (not a generic teardrop pin) with a soft glow,
tinted by the company's `industry` (the same real, already-modeled field
the filter chips use — not a fabricated categorization). One shape, not a
different icon per company; this is a brand device, not per-company
iconography inflation.
- Nodes render with a gentle pulse (subtle, not a strobe) — the literal seed
of Phase 2's "nodes become planets" framing from the root CLAUDE.md design
language.
- Clustering uses Mapbox's native GeoJSON cluster support (no extra
library), decluster smoothly on zoom-in. At 30 seeded companies this is
about establishing the pattern correctly, not solving a real density
problem yet — must scale past 30 without a redesign.
- **Map-load animation** (Framer Motion, already in the stack per
`apps/web/CLAUDE.md` — used sparingly, per that same file's existing
guidance): on first load, the camera eases into the Hyderabad view (a
brief fly-in, not a long cinematic sequence), then nodes fade/scale in,
then clusters resolve. One orchestrated moment, not scattered effects.
Respects `prefers-reduced-motion` (already handled globally per
`apps/web/CLAUDE.md`'s theming section) — reduced-motion users get the
final state immediately, no animation forced on them.

### Company cards

- Rendered from `CompanySummary` (Slice 1's existing shape: name, industry,
description) plus **locality label** (derived the same way the map's
locality picker knows the seven areas — a small lookup, not a new backend
field) and **distance** from the current search origin. No new backend
fields required for any of this.
- Reserves visual space for a future score/rating row (the "Career Score"
Slice 5 will compute), but **does not render a fabricated star rating now**
— there is no real score to show yet, and inventing one would quietly
break Facts-First (ADR 0005) a full two slices before the Career
Intelligence Engine exists. The reserved slot shows a quiet, honest
placeholder (e.g. a muted "Career Score — coming soon" label in the
utility/mono type) instead of empty/filled stars. **Flagging this
explicitly as a deliberate deviation from the literal "★★★★☆" mockup** —
confirm if a different honest treatment is preferred.
- Ends with a clear "View Company →" action (opens the detail
panel/page).
- Clicking a card highlights/pans to its node; clicking a node highlights
its card — the two views stay in sync.

### Filter chips (by industry — companies only, not opportunities)

- A row of chips derived from the real, already-seeded `industry` values
(e.g. "AI/ML," "Fintech," "Enterprise Software," "Semiconductors" — a
small deduplicated set from the 30 seeded companies, not a new taxonomy).
Selecting one filters the current map/list to matching companies.
- **Client-side only** — the nearby/search result set (≤50 companies per the
existing pagination convention) is already fetched; filtering by industry
is a local operation, not a new backend endpoint or query parameter. No
schema change, no new contract surface.
- These are **company filters, not opportunity filters** — they narrow which
companies show, using a field `Company` already has (`industry`). This
does not reintroduce `Opportunity` scope; there is still nothing to
"apply" to or "match" against.

### Company detail panel

- Clicking a card or marker opens a detail view with the full `CompanyDetail`
shape (description, website, careers page, founded year — Slice 1 fields
only, nothing from Slice 5 yet).
- Available both as an **inline panel** (fast, no navigation, for the
map-browsing flow) and a **deep-linkable route**
(`/companies/[slug]`, server-rendered, so a company detail page is a real,
shareable, SEO-crawlable URL — consistent with Core tier being
"cacheable, SEO-friendly" per ADR 0004).

### Search by location

- A picker (dropdown or typeahead) over the **seven known localities**
(Madhapur, Hitech City, Gachibowli, Financial District, Kondapur, Raidurg,
Nanakramguda) — not a free-text geocoder. Selecting one re-centers the map
and re-queries nearby companies from that locality's known center point.
These seven points are a small **frontend constant** (`features/map/`), not
a new backend concept — `geo` doesn't need a "Locality" entity for seven
well-known, unchanging landmarks; introducing one now would be exactly the
kind of speculative abstraction the Slice 1/2 reviews have been catching.

### "Near Me"

- Uses the browser Geolocation API (`navigator.geolocation.getCurrentPosition`),
gated on the browser's own permission prompt — no account, no login,
consistent with anonymous-first. On denial, error, or an unsupported
browser, falls back gracefully to the default Hyderabad map center with a
visible (not silent) message — never a broken or blank state.

### Responsive layout

- Mobile: map and the nearby-companies list do not compete for the full
viewport at once — list collapses to a bottom sheet/drawer over the map.
- Desktop: map and list render side-by-side.
- Verified at a small set of concrete breakpoints (e.g. 375px, 768px, 1280px)
as part of the DoD, not "looks fine on my monitor."

### Performance goals

- Largest Contentful Paint (LCP) target **< 2.5s** on a throttled connection
(Lighthouse "Fast 3G"/mobile preset) for the initial page — the map itself
loads after first paint (client-only dynamic import), so it never blocks
LCP.
- Mapbox GL JS bundle is code-split and loaded only on the page(s) that need
it — never bundled into shared/first-load JS.
- The nearby-companies query (new backend endpoint) responds in
**< 200ms p95** locally against the 30-row seeded dataset (PostGIS
`ST_DWithin` + GIST index, already proven queryable in Slice 2's
verification).

### Accessibility

- Per `apps/web/CLAUDE.md`'s existing standard (semantic HTML, keyboard
complete, labeled controls, AA contrast, `prefers-reduced-motion`
respected) — **plus one map-specific rule**: the map is a visual
complement, never the only way to reach the data. Every company reachable
via keyboard/screen reader through the list view; nothing is
map-widget-gated. Locality picker and "Near Me" control are both real,
labeled, keyboard-operable controls (not map-only gestures).

### Future hook — "Explore Career Universe →"

- A visibly present but **disabled** (or "Coming Soon" labeled) button/link
on the home page. No route, no component, no logic behind it — purely a
static, honest visual signal of what's next. Must not silently do nothing
on click (a disabled state or a "Coming soon" tooltip/toast is required —
not a dead link that looks broken).

### Cross-slice

- `ruff` / `black --check` / `mypy --strict` / `lint-imports` / `pytest`
(backend); `prettier` / `tsc --noEmit` / `eslint` / Vitest (frontend) all
pass. Playwright e2e: load home → see map + list → search by locality →
see results update → open a company detail → land on a real URL — all
anonymous, zero auth in the flow (first real proof of ADR 0004 for a
full user journey, not just an endpoint).
- OpenAPI regenerates with zero unexpected drift beyond the one new
`GET /companies/nearby` endpoint.

## Domain Model

No new bounded context. Two contexts gain their first real cross-context
collaboration:

### `geo` — first read port (a real caller exists now)

- **Application:** `FindNearbyCompanies` use case — given an origin
`Location` and a radius, returns `CompanyId`s ordered by distance
(`ST_DWithin` + distance ordering against `company_locations`, the table
Slice 2 already proved queryable).
- **Contract:** adds `NearbyQuery` (origin + radius) and `NearbyResult`
(`CompanyId` + `distance_km`) to `geo.contract`, and a narrow read
port/protocol other code depends on — this is exactly the adapter the
Slice 1 and Slice 2 reviews deferred ("build it when there's a real
caller"). There is one now.

### `companies` — no shape change, one convenience addition

- `Company`/`CompanyId`/`CompanySummary`/`CompanyDetail` are unchanged.
- The API layer needs to hydrate a `CompanySummary` for each nearby
`CompanyId`. At 30 rows, N sequential `GetCompany` calls is acceptable
(no N+1 concern at this scale); a batched `get_many(ids)` is a nice-to-have
the implementation may add to `CompanyRepository`, not a hard requirement
— noted in Risks so it isn't silently forgotten if the dataset grows.

### `apps/web` — first real feature module

- `features/map/` (Mapbox wrapper, marker/cluster layer, locality picker,
"Near Me" control, nearby-list, company card) and reuse of
`features/company-intelligence/`-equivalent detail rendering (per the
parent spec's UI Flow) — business-specific UI stays out of `packages/ui`.

## Database Changes

**None.** `company_locations` (Slice 2) is already the right shape for
`ST_DWithin` queries — this slice adds a query, not a schema change.

## API Changes

One new endpoint:

- `GET /companies/nearby?lat=&lng=&radius_km=&limit=` — returns
`CompanySummary` + `distance_km` per result, ordered by distance, using
the same pagination convention (`docs/api/pagination.md`) as
`GET /companies`.

`GET /companies/{company_id}` (Slice 1) is reused unchanged for the detail
panel/page. No changes to `GET /companies` (list) or its response shape.
OpenAPI regenerates; the diff should show exactly one new path.

**As implemented — two corrections found only by building the real thing:**

- `NearbyCompanyResponse` also carries `latitude`/`longitude` per company —
not anticipated when this spec was written, but the map cannot place a
marker with a distance alone; it needs the actual coordinate. Additive
field, not a redesign; `geo.contract`'s `NearbyResult` gained a `location: Location` field to carry it.
- A second new endpoint was required beyond what this section originally
scoped: `GET /companies/by-slug/{slug}` — the deep-linkable
`/companies/[slug]` route (below) needs to resolve a slug to a company,
and Slice 1 only exposed lookup by UUID. Backed by `CompanyRepository. get_by_slug`, which already existed since Slice 1; only the use case
(`GetCompanyBySlug`) and router were new. Registered ahead of
`/{company_id}` in the router, same reasoning as `/nearby`.

## UI Flow

`apps/web/src/app/(public)/`:

1. **Home (`/`, replaces the Phase 0 placeholder)** — hero copy ("Discover
  opportunities around you" / Hyderabad), the live map (clustered markers,
   default-centered on Hyderabad), a nearby-companies list beside/below it,
   the locality picker, the "Near Me" control, and the disabled "Explore
   Career Universe →" CTA at the bottom.
2. **Company card** (list or map popup) → **inline detail panel** (fast path)
  or `**/companies/[slug]**` (deep-linkable, server-rendered detail page —
   the SEO/shareable path).
3. Mobile: list becomes a bottom sheet; desktop: side-by-side.

Per `apps/web/CLAUDE.md`: feature-first (`features/map/`), generated API
types only (`packages/api-contracts`, regenerated after the new endpoint),
Framer Motion sparingly (marker/cluster transitions, panel open/close — not
spectacle), semantic tokens only for theming, accessibility as DoD not
follow-up.

## Testing Strategy

- **Unit (backend):** `FindNearbyCompanies` against an in-memory fake (no
DB) for ordering/radius logic; a real-DB integration test asserting the
`ST_DWithin` query returns correct, distance-ordered results (extends the
manual proof already done in Slice 2's verification into a committed test).
- **Unit (frontend, Vitest):** locality picker, "Near Me" control (mocked
Geolocation API, including the denied/unsupported paths), company card,
map wrapper in isolation (mocked Mapbox).
- **E2E (Playwright):** the full anonymous journey described in Acceptance
Criteria — home → locality search → results update → detail page — zero
auth. A second flow covers "Near Me" denied → graceful fallback, not a
broken state.
- **Accessibility:** an automated a11y check (axe or equivalent) on the home
page and detail page, plus a manual keyboard-only pass confirming every
company is reachable without touching the map.
- **Performance:** a Lighthouse run (or `chrome-devtools` MCP trace) against
the home page recording LCP, checked against the < 2.5s target as part of
verification, not assumed.

## Risks


| Risk                                                                                                                                        | Mitigation                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Mapbox token is `NEXT_PUBLIC_`-prefixed (client-exposed), which looks like it conflicts with ADR 0003's `NORTHSTAR_`-prefix env convention. | Reconcile explicitly: ADR 0003 governs *backend* config (Pydantic Settings); Next.js *requires* `NEXT_PUBLIC_` for anything shipped to the browser bundle, and a Mapbox public token is designed to be client-visible (scoped, restrictable in the Mapbox dashboard) — this is a platform-mandated naming convention, not an architecture violation. Document this once in `contexts/geo/CLAUDE.md` or a new `apps/web` env doc so it isn't relitigated per PR. |
| Marker clustering is easy to get visually wrong (jumpy re-clustering, popups misaligned after cluster-expand).                              | Use Mapbox's native cluster support exactly as documented rather than hand-rolling; test at the three breakpoints named above, not just desktop.                                                                                                                                                                                                                                                                                                                |
| The map, if built carelessly, becomes the *only* way to reach company data — an accessibility trap.                                         | Explicit acceptance criterion: the list view is a fully keyboard/screen-reader-complete path to every company, independent of the map.                                                                                                                                                                                                                                                                                                                          |
| N sequential `GetCompany` calls to hydrate nearby results could become a real N+1 problem once the dataset grows past a demo.               | Acceptable now (30 rows); flagged explicitly so a future slice doesn't have to rediscover the need for a batched `get_many`.                                                                                                                                                                                                                                                                                                                                    |
| "Near Me" geolocation can be denied, unsupported, or slow — a naive implementation shows a blank map.                                       | Explicit fallback state required by acceptance criteria, tested in Playwright, not left as an edge case.                                                                                                                                                                                                                                                                                                                                                        |
| Performance targets (LCP < 2.5s) are easy to blow past once Mapbox GL's bundle is in play.                                                  | Client-only dynamic import (`ssr:false`) keeps Mapbox off the critical path for first paint; verified via a real Lighthouse/trace run, not assumed from code review.                                                                                                                                                                                                                                                                                            |
| Locality picker's 7 hardcoded coordinates could drift from the seed data's actual coordinates (Slice 2) if either changes independently.    | Keep both derived from the same source of truth conceptually (the same 7 named localities); note in the picker's code comment that it must stay in sync with `apps/api/scripts/data/hyderabad_companies.json`'s `locality` groupings if that data is ever regenerated.                                                                                                                                                                                          |


## Rollout Plan

Single slice, one new backend endpoint, one new frontend feature module,
same discipline as Slices 1–2: this spec → approval → implementation →
verification (including a live Lighthouse/perf check and a manual
accessibility pass, not just automated tests) → documentation → Slice
Boundary Review → commit → tag `phase1-slice3`.

## Future Extensions

- **Career Universe (Phase 2)** replaces the disabled CTA with the real
experience, reusing the exact same `companies`/`geo` canonical data — no
new data pipeline.
- **Search by role** arrives with Slice 4 (Opportunity Foundation), likely
as an additional filter alongside the existing locality picker/"Near Me",
not a redesign of either.
- **Free-text/general geocoding search** — if the product ever needs
location search beyond the seven known localities (e.g. after Slice 3
covers more cities), replace the frontend constant with a real geocoding
call. Additive, not a redesign of the search UI itself.
- **Batched `get_many(ids)` on `CompanyRepository`** — if nearby-result
hydration ever shows up as a real perf problem past demo scale.
- **Real "Career Score"** replaces the honest placeholder reserved on the
company card once Slice 5 (Company Intelligence) or Phase 3 (CIE) computes
a real, explainable value — the reserved layout slot means this is a
additive UI change, not a card redesign.
- **Per-category node glyph variation** (not just color/glow tint) if a
richer, real taxonomy exists later (e.g. Slice 5's fields) — deferred now
because inventing shape-per-category without real driving data would be
decoration, not signal.

