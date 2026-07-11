---
name: update-adr
description: Create a new immutable Architecture Decision Record, or supersede an existing one. Use whenever an architectural decision is made or changed — architecture changes MUST begin here, before implementation.
---

# update-adr

Records architectural decisions immutably. Architecture changes in NorthStar begin with an ADR **before** implementation.

## Rules

- **ADRs are immutable.** Never edit an accepted ADR. To change a decision, create a NEW ADR that supersedes the old one and references it; mark the old one `Superseded by NNNN`.
- Numbering is sequential, zero-padded: `docs/adr/NNNN-kebab-title.md`.
- Every significant architectural decision is captured before code, not reconstructed later.

## Steps

1. Determine the next number from `docs/adr/`.
2. Create `docs/adr/NNNN-<kebab-title>.md` with:
   - **Title**, **Status** (Proposed | Accepted | Superseded), **Date**, **Context**, **Decision**, **Consequences**, **Alternatives considered**, and links to related ADRs / blueprint sections.
3. If superseding: set the old ADR's status to `Superseded by NNNN` (this is the one permitted edit — a status pointer, not a rewrite).
4. Update `docs/adr/README.md` index and, if it changes a principle, `docs/architecture/principles.md`.
5. If the blueprint's frozen design changes, note it in `docs/architecture/blueprint.md` §10 change log.

## Do NOT

- Implement the decision in this Skill — record only. Implementation follows separately.
