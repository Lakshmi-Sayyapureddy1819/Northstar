# ADR 0007 — LLM Port; no agent framework for the MVP

- **Status:** Accepted
- **Date:** 2026-07-12

## Context

The original stack proposed Claude + OpenAI + LiteLLM + LangGraph + PydanticAI —
four overlapping AI abstractions. That contradicts the Simplicity principle and
risks coupling the platform to a specific provider and to premature agent
orchestration before any product requirement justifies it.

## Decision

Introduce a single internal **`LLMPort`** from day one, with **one**
implementation: a thin adapter over the official Anthropic SDK (default model
`claude-opus-4-8`), using the SDK's native structured-output/validation. The AI
layer is a **platform capability** (`platform/llm/`), not a business context;
domain/application layers depend on the port, never a vendor SDK. **No
LangGraph** and **no PydanticAI** for the MVP: the SDK already provides typed,
validated outputs, and the port already provides provider-agnosticism, so both
would be redundant complexity. If a real requirement later needs multi-step
agentic loops, reach first for the SDK's own tool-runner; adopt a heavier
framework only if that is outgrown — via a new ADR.

## Consequences

- Provider is swappable behind the port without touching business logic.
- The AI surface stays minimal and testable; no "framework of the week."
- A clear, low-cost upgrade path exists if orchestration needs grow.

## As implemented

- `platform/llm/` is the reserved home for the `LLMPort` + Claude adapter +
  prompt infrastructure + AI observability (scaffolded in Phase 0; the concrete
  adapter lands with the Polaris phase).
- The "AI is a platform capability, not business logic" boundary is documented
  in `contexts/polaris/CLAUDE.md` and the root `CLAUDE.md`.
- No `langgraph` / `pydantic-ai` dependencies are present in `apps/api`.
