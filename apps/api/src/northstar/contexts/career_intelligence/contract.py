"""Public contract for the `career_intelligence` context (Core tier).

This module is the ONLY surface other contexts may import. Access to
`career_intelligence`'s internals (domain / application / infrastructure) from another
context is forbidden and enforced by import-linter. Expose here only what
other contexts are permitted to consume.

Phase 0 exposes the Facts-First contract shape: the standard `EngineResult`
envelope (with `Trace`) and the `Engine` protocol. Polaris and other contexts
consume engine results through this surface — never through CIE internals.
Concrete engines are added additively in the Career Intelligence phase.
"""

from __future__ import annotations

from northstar.contexts.career_intelligence.domain.engine import Engine
from northstar.contexts.career_intelligence.domain.engine_result import (
    EngineResult,
    Trace,
)

__all__ = ["Engine", "EngineResult", "Trace"]
