# Architecture Decision Records

An ADR captures one significant architectural decision: its context, the
decision, and its consequences. **ADRs are immutable.** A decision that changes
is not edited — a new ADR supersedes it and references the old one, whose status
becomes `Superseded by NNNN`.

These nine records document NorthStar's foundational architecture **as
implemented in Phase 0** (not as originally brainstormed). They are the
authoritative "why" behind the frozen Engineering Blueprint
(`docs/architecture/blueprint.md`). New architectural decisions from Phase 1
onward continue the sequence (use the `update-adr` skill).

| ADR | Title | Status |
|-----|-------|--------|
| [0001](0001-modular-monolith.md) | Modular monolith with enforced context boundaries | Accepted |
| [0002](0002-source-agnostic-ingestion.md) | Source-agnostic, pluggable data ingestion | Accepted |
| [0003](0003-cloud-agnostic-infrastructure.md) | Cloud-agnostic, local-first infrastructure | Accepted |
| [0004](0004-anonymous-first-experience.md) | Anonymous-first experience with layered personalization | Accepted |
| [0005](0005-facts-first-ai-second.md) | Facts First, AI Second | Accepted |
| [0006](0006-career-intelligence-engine.md) | Career Intelligence Engine (deterministic engine tier) | Accepted |
| [0007](0007-llm-port-no-agent-framework.md) | LLM Port; no agent framework for the MVP | Accepted |
| [0008](0008-api-contracts-single-source-of-truth.md) | API contracts as the single source of truth | Accepted |
| [0009](0009-automation-enforces-architecture.md) | Automation enforces architecture | Accepted |

## Format

Each ADR follows: **Status · Date · Context · Decision · Consequences ·
As-implemented** (evidence in the code/config that the decision is real, not
just documented).
