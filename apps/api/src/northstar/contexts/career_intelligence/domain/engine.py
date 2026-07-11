"""The common Engine contract every deterministic engine implements (§3.4).

An engine maps a typed input to a typed EngineResult. It must be
deterministic (same input → same output), make no LLM calls, and perform no
I/O to external opinion sources. See contexts/career_intelligence/CLAUDE.md
for the full Engine Definition of Done.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from northstar.contexts.career_intelligence.domain.engine_result import EngineResult


@runtime_checkable
class Engine[InputT, OutputT](Protocol):
    """A single-responsibility deterministic engine."""

    name: str

    def run(self, request: InputT) -> EngineResult[OutputT]:
        """Compute the result for a typed request. Deterministic and pure."""
        ...
