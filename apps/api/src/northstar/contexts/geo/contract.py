"""Public contract for the `geo` context (Core tier).

This module is the ONLY surface other contexts may import. Access to
`geo`'s internals (domain / application / infrastructure) from another
context is forbidden and enforced by import-linter. Expose here only what
other contexts are permitted to consume.

Slice 2 (Seed Hyderabad Dataset) exposes: `Location`, a validated
latitude/longitude value object. No read port (e.g. a nearby-query reader)
ships yet — there is no cross-context consumer this slice. Slice 3 (Map
Experience) adds the `find_nearby` capability and whatever read port it
actually needs, learned from the Slice 1 review: build the adapter when
there's a real caller, not before.
"""

from __future__ import annotations

from northstar.contexts.geo.domain.value_objects import Location

__all__ = ["Location"]
