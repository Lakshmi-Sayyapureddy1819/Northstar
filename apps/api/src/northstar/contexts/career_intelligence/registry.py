"""The CIE engine registry — the single wiring point for engines (§3.4).

Adding an engine is additive: a new module under `engines/<name>/` plus one
`register()` call here. Existing engines are never modified. Empty in Phase 0
— engines arrive in the Career Intelligence phase via the `add-engine` Skill.
"""

from __future__ import annotations

from typing import Any

from northstar.contexts.career_intelligence.domain.engine import Engine


class EngineRegistry:
    """Holds the set of available engines, keyed by name."""

    def __init__(self) -> None:
        self._engines: dict[str, Engine[Any, Any]] = {}

    def register(self, engine: Engine[Any, Any]) -> None:
        if engine.name in self._engines:
            raise ValueError(f"Engine '{engine.name}' is already registered.")
        self._engines[engine.name] = engine

    def get(self, name: str) -> Engine[Any, Any]:
        return self._engines[name]

    def names(self) -> list[str]:
        return sorted(self._engines)


registry = EngineRegistry()
