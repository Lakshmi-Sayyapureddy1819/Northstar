"""The pattern every CIE engine test follows (Blueprint §7, Engine DoD).

There are no real engines in Phase 0, so this uses a tiny example engine to pin
down the contract: deterministic, returns the standard EngineResult envelope,
and satisfies the Engine protocol. Real engines (matching, ranking, …) arrive in
the Career Intelligence phase via the `add-engine` Skill and follow this shape.
"""

import pytest
from pydantic import ValidationError

from northstar.contexts.career_intelligence.contract import (
    Engine,
    EngineResult,
    Trace,
)


class DoublingEngine:
    """Example deterministic engine (test fixture, not shipped)."""

    name = "doubling"

    def run(self, request: int) -> EngineResult[int]:
        return EngineResult(
            output=request * 2,
            confidence=1.0,
            explanation=f"Doubled {request}.",
            trace=Trace(sources=["request"], steps=[f"{request} * 2"]),
        )


def test_engine_is_deterministic():
    engine = DoublingEngine()
    assert engine.run(21).output == engine.run(21).output == 42


def test_engine_result_carries_the_standard_envelope():
    result = DoublingEngine().run(10)
    assert result.output == 20
    assert 0.0 <= result.confidence <= 1.0
    assert result.explanation
    assert result.trace.sources == ["request"]
    assert isinstance(result.metadata, dict)


def test_example_satisfies_engine_protocol():
    engine: Engine[int, int] = DoublingEngine()
    assert isinstance(engine, Engine)  # runtime_checkable protocol


def test_confidence_is_bounded_zero_to_one():
    with pytest.raises(ValidationError):
        EngineResult(
            output=1, confidence=1.5, explanation="too confident", trace=Trace()
        )
