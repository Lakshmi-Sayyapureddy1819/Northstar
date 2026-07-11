"""The standard EngineResult envelope (blueprint §3.4).

Every deterministic engine returns this uniform shape, so results are
explainable and traceable back to structured data. This is the architectural
heart of "Facts First, AI Second" (ADR 0005): engines compute the facts;
AI only narrates the EngineResults it is handed.

Contains no business logic — it is the typed contract shape, nothing more.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Trace(BaseModel):
    """Provenance for an engine result: how it was computed, from what data."""

    sources: list[str] = Field(
        default_factory=list,
        description="Identifiers of the structured data the result was derived from.",
    )
    steps: list[str] = Field(
        default_factory=list,
        description="Ordered, human-traceable computation steps.",
    )


class EngineResult[OutputT](BaseModel):
    """The uniform result every CIE engine returns."""

    output: OutputT
    confidence: float = Field(ge=0.0, le=1.0, description="0..1 confidence in the output.")
    explanation: str = Field(description="Human-readable rationale for the result.")
    trace: Trace = Field(description="Provenance back to structured data.")
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Timing, engine version, input digest — for analytics.",
    )
