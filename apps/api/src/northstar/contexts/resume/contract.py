"""Public contract for the `resume` context (Personalization tier).

This module is the ONLY surface other contexts may import. Access to
`resume`'s internals (domain / application / infrastructure) from another
context is forbidden and enforced by import-linter. Expose here only what
other contexts are permitted to consume.

Empty in Phase 0 — this context has no public surface yet.
"""

from __future__ import annotations

__all__: list[str] = []
