"""Value objects for the `companies` domain.

`CompanyId` is the aggregate's stable, immutable identity — the only thing
another context (e.g. `opportunities` in Slice 2) is ever allowed to hold a
reference to. `CompanySlug` is deliberately a *separate* value object: it is
unique and URL-friendly but may change (a rename regenerates it) without
touching identity anywhere it's referenced.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass

_SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


@dataclass(frozen=True, slots=True)
class CompanyId:
    """Stable identity of a `Company` aggregate. Never derived from mutable data."""

    value: uuid.UUID

    @classmethod
    def new(cls) -> CompanyId:
        return cls(uuid.uuid4())

    @classmethod
    def from_str(cls, raw: str) -> CompanyId:
        return cls(uuid.UUID(raw))

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class CompanySlug:
    """A mutable, URL-friendly identifier — never used as identity.

    Two companies must not share a slug (enforced at persistence), but a slug
    itself may be regenerated (e.g. after a rename) without affecting the
    `CompanyId` any reference to the company already holds.
    """

    value: str

    def __post_init__(self) -> None:
        if not _SLUG_RE.match(self.value):
            raise ValueError(
                f"invalid slug {self.value!r}: must be lowercase "
                "alphanumeric segments separated by single hyphens"
            )

    @classmethod
    def from_name(cls, name: str) -> CompanySlug:
        """Derive a slug from a company name. Deterministic, not stored as identity."""
        normalized = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
        if not normalized:
            raise ValueError(f"cannot derive a slug from name {name!r}")
        return cls(normalized)

    def __str__(self) -> str:
        return self.value
