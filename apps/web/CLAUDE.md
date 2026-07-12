# apps/web — Frontend Conventions

Next.js (App Router) + React + TypeScript + Tailwind + shadcn/ui + Framer Motion. Read the root `CLAUDE.md` first.

## Anonymous-first routing

- `app/(public)/` — anonymous-accessible: explore, company details, Career Universe, search. Server-rendered, cacheable, no auth dependency.
- `app/(app)/` — auth-gated: dashboard, Career GPS, resume, tracking.
- The **same** core navigation components render in both; personalization is layered via props/context — never a separate app.
- `(public)`/`(app)` are **architectural boundaries, not auth mechanisms.** They express the anonymous-first tiering (ADR 0004); anonymous and authenticated users share the same navigation experience wherever possible. Don't fork the UX along the group boundary.

## Feature-first organization

```
features/<capability>/     # career-universe, map, company-intelligence, career-gps, polaris
components/                # shared presentational (from packages/ui)
lib/api/                   # typed client generated from OpenAPI — DO NOT hand-write API types
```

- **`packages/ui` holds reusable primitives only** (Button, Input, Card, …) — generic, business-agnostic, presentational. **Business-specific UI lives inside its `features/<capability>/`**, never in the shared design system. If a component knows about companies, opportunities, or engines, it belongs to a feature.

## Hard rules

- **Consume generated API types only** (`packages/api-contracts`, via the `openapi-fetch` client in `src/lib/api/client.ts`). Never define your own interface for an API object, and never hand-edit generated files — change the backend and run `pnpm contracts:generate`. Drift = type error.
- **No ignored TS errors.** `tsc --noEmit` must pass. ESLint + Prettier clean.
- **Framer Motion sparingly** — subtle, premium interactions, not spectacle.

## Accessibility (project standard, not a later enhancement)

Accessibility is a first-class engineering standard from Phase 0. Every shared
component and every layout ships accessible by default:

- **Semantic HTML first.** Real `<button>`, `<nav>`, `<main>`, headings in order. Reach for ARIA only when semantics can't express the intent.
- **Keyboard complete.** Everything operable without a mouse; visible `focus-visible` state on all interactive elements (design-system primitives already carry a focus ring).
- **Labels & names.** Every control and icon-only button has an accessible name (`aria-label` / associated `<label>`). Images have `alt`.
- **Contrast.** Text/background pairs meet WCAG AA; verify token pairs when adding a theme.
- **Motion.** Respect `prefers-reduced-motion` (handled globally in `globals.css`); Framer Motion animations must degrade gracefully.
- **Landmarks & language.** Pages render inside a `<main>`; `<html lang>` is set.

New UI is not "done" until it meets these — treat a11y like tests and types.

## Theming (light · dark · brand)

Components reference **semantic tokens only** (`bg-background`, `text-primary`, …),
never raw colors. Each theme is just a selector redefining those tokens in
`globals.css`: `:root` (light), `.dark` (dark), `.theme-brand` (brand — palette
arrives with the design-language phase). Themes compose (`.theme-brand.dark`).
Because components never hardcode colors, adding or reskinning a theme touches
tokens only — never component code.

## Career Universe (product identity, lightweight)

- Reuses the **same canonical data** as the map — it is a second perspective, not a separate visualization pipeline.
- Map answers "Where are opportunities?"; Universe answers "How do opportunities relate to me?"
- Implementation: standard React components + positioning + Framer Motion. **No physics engine, no custom graphics engine, no D3** (deferred until a concrete viz truly needs it).
- Must communicate: (1) You are here. (2) These are the nearby companies. (3) These are your best opportunities.
- Elegant over technically impressive. Accessible and performant.

## Visualization roadmap

Mapbox (Day 1) · Framer Motion (Day 1) · React Flow (arrives with Career GPS) · D3 (deferred).
