"""LLM platform capability (blueprint §3.5, ADR 0007).

AI is infrastructure, not business logic. This package will own the LLMPort,
a thin Claude adapter, prompt infrastructure, structured-output handling, and
AI observability. Polaris (a context) consumes this capability; it never
computes business facts. Implemented when the Polaris phase begins — kept an
empty documented seam in Phase 0.
"""
