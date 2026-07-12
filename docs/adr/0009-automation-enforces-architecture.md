# ADR 0009 — Automation enforces architecture

- **Status:** Accepted
- **Date:** 2026-07-12

## Context

Architectural rules that rely on memory and goodwill erode. With a solo
developer and AI-assisted development, guardrails must be mechanical, and AI
tooling must protect the architecture rather than quietly redesign it.

## Decision

**Automation enforces architecture; it does not replace architectural thinking.**
Hooks, Skills, CI, and agents exist to protect the designed architecture. Any
architectural change begins with **discussion → documentation → ADR**, *before*
implementation; no new architectural concept is introduced unless an ADR changes
the design. Supporting rules: the `architecture-guardian` agent is the
repository's technical reviewer (reviews only, never implements); Skills are
deterministic (they scaffold/validate patterns, never make product decisions);
the root `CLAUDE.md` holds only permanent architectural truths so it stays
stable as the project grows.

## Consequences

- Boundary and contract violations fail mechanically (CI/local), independent of
  who or what wrote the code.
- The decision record stays honest: the architecture only changes through ADRs.
- AI assistance accelerates within guardrails instead of drifting the design.

## As implemented

- **CI** (`.github/workflows/ci.yml`) enforces import-linter (boundaries),
  contract-drift (ADR 0008), strict typing, lint, format, and tests; any
  violation fails the build.
- **Local hooks** (`.claude/hooks/quality-gate.sh`, `doc-drift.sh`, wired in
  `.claude/settings.json`) run the same guardrails on edits.
- **Skills** (`.claude/skills/`): `add-engine`, `add-provider`, `add-context`,
  `update-adr`, `update-documentation`, `generate-api-contracts` — deterministic
  scaffolders.
- **`architecture-guardian`** (`.claude/agents/`) is review-only; it performed
  the Phase 0 compliance audit (`docs/architecture/compliance-audit.md`).
- **Layered `CLAUDE.md`** files carry invariants (root) and procedures (per
  context).
