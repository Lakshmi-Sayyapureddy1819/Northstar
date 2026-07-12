# MVP Scope

> The scope-creep guardrail. If a proposed feature isn't **in** the list below,
> it is **out** until an ADR moves it in. Companion to `prd.md`.

## In scope (MVP)

- **Geography:** Hyderabad only.
- **Domain:** Software Engineering and AI/ML roles only.
- **Experiences:**
  - Hyperlocal map of nearby companies (Mapbox).
  - Company cards, company details, search by role and by location.
  - Career Universe (lightweight, same canonical data as the map).
  - Career Navigation and Career GPS.
  - Resume Intelligence and Company Intelligence.
  - The Career Intelligence Engine (deterministic recommendations).
  - Polaris (AI assistant) — explains/personalizes engine outputs.

The MVP must read immediately as **career navigation**, not a job board.

## Explicitly out of scope (deferred)

Each returns only when its user value is justified — via a new ADR.

- Other cities beyond Hyderabad.
- Other professions/verticals (CA/CS/MBA, law, medicine, design, research, …).
- Other opportunity types beyond SWE/AI-ML roles (articleships,
  apprenticeships, campus hiring, research positions, freelance) as first-class
  flows.
- Employer-submitted and user-contributed opportunities (ingestion sources 4–5).
- D3.js / heavy custom visualization.
- LangGraph / PydanticAI or any agent-orchestration framework.
- Mobile apps.
- Real-time / collaborative features.

## Phasing

The MVP is delivered as thin vertical slices after Phase 0 (Foundation):
`Data → Visualization → Career Intelligence → Identity → Resume Intelligence →
Career GPS → Polaris`. See `docs/roadmap/` and `docs/project-history.md`.

## Deferral policy

Deferred ≠ rejected. When evidence shows an out-of-scope item would create
measurable user value, record the decision as an ADR (using the `update-adr`
skill) and move it in — never by ad-hoc scope drift.
