# NorthStar — Product Requirements (PRD)

> The canonical business specification. **Every feature traces back to this
> document.** Scope boundaries live in `mvp-scope.md`; the "why/how it evolved"
> narrative is in `docs/project-history.md`.

## Problem

People steering a career are served by job *portals* — keyword search over
listings. What they actually need is *navigation*: understanding where they
stand, what's around them, and what move to make next. Existing products
optimize for applying to jobs, not for making good career decisions.

## Vision

NorthStar is an AI-powered **Hyperlocal Career Navigation Platform** — "Google
Maps for Careers." Navigation over search; decision intelligence over filtering;
AI guidance over keyword matching. It is explicitly **not** a job board and does
not compete with LinkedIn / Naukri / Indeed on their terms.

## Who it's for

Professionals and students making career decisions. The long-term audience spans
many professions (engineers, data scientists, CA/CS/MBA students, lawyers,
doctors, designers, researchers, freshers, and experienced professionals) and
opportunity types (full-time, internships, articleships, apprenticeships,
freelance, campus hiring, research). The **MVP audience is narrowed** — see
`mvp-scope.md`.

## What it answers

- Where am I, and which companies/opportunities are near me?
- What is my best next career move?
- Which nearby companies match my profile?
- What skills should I learn next?
- What salary should I expect?
- Which opportunity offers the highest long-term growth?

## Product pillars

1. **Hyperlocal map** — nearby companies and opportunities on a real map (the
   product's identity; "where are opportunities?").
2. **Career Universe** — a lightweight second perspective over the same data
   ("how do opportunities relate to me?").
3. **Career Intelligence** — deterministic engines producing explainable,
   traceable recommendations (matches, salary, skill gaps, commute, rankings).
4. **Company & Resume Intelligence** — structured understanding of companies and
   of the user's profile.
5. **Polaris** — an AI assistant that explains and personalizes the above; it
   never computes the facts (ADR 0005).

## How we build it (product-shaping constraints)

- **Anonymous-first (ADR 0004):** core exploration works without login;
  personalization unlocks with an account.
- **Facts First, AI Second (ADR 0005):** every objective recommendation is
  explainable and traceable to structured data.
- **Legal, source-agnostic data (ADR 0002):** opportunities come from legitimate
  sources; no scraping of prohibited sites.
- **Simplicity:** the simplest implementation that delivers the intended UX.

## Success signals (directional, MVP)

- A first-time anonymous visitor understands within one screen that this is
  *career navigation*, not a job board.
- Users can find nearby, relevant companies for their role and location.
- Recommendations, when shown, come with an explanation a user trusts.

## Out of scope

See `mvp-scope.md` for the explicit in/out list and the deferral policy (each
deferred item returns only when user value justifies it, via a new ADR).
