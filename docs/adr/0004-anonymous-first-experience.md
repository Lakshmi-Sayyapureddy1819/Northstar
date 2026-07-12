# ADR 0004 — Anonymous-first experience with layered personalization

- **Status:** Accepted
- **Date:** 2026-07-12

## Context

NorthStar's value — exploring nearby companies and opportunities — should be
felt before any login wall. At the same time, personalized features (resume,
Career GPS, Polaris, saved items, tracking) genuinely need an account. We must
not fork into two apps, and auth must not sit in front of the product's core.

## Decision

The **Core tier is identity-agnostic**: navigation, company intelligence, geo,
and opportunity browsing know nothing about users, so they are fast, cacheable,
and available anonymously. **Personalization** is a separate set of auth-gated
contexts that *consume* the core but never pollute it. Authentication gates
specific capabilities; it is not a wall in front of the app. An anonymous
session can be upgraded to an authenticated one without losing context (e.g. a
search runs anonymously and is saved on login).

## Consequences

- The anonymous experience is performant and SEO-friendly with no auth
  dependency.
- The same core navigation components render for everyone; personalization is
  layered via props/context, not a parallel application.
- Auth complexity and PII stay contained in the personalization tier.

## As implemented

- Tiers Core → Personalization → Polaris (blueprint §3.2), realized as separate
  contexts (`companies`, `geo`, `opportunities`, … vs `identity`, `profile`,
  `resume`, `career_gps`, `engagement`).
- Frontend expresses the boundary with Next.js route groups `app/(public)/`
  (anonymous, server-rendered) and `app/(app)/` (auth-gated); documented in
  `apps/web/CLAUDE.md` as an architectural boundary, not merely an auth
  mechanism.
