"""Result / error primitives shared across all contexts.

Domain and application flows prefer an explicit `Result` over raising, so
success and failure are part of the type signature (see apps/api/CLAUDE.md).
Kept deliberately tiny — the shared kernel is not a junk drawer.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DomainError:
    """A named, typed failure in a domain/application flow."""

    code: str
    message: str


@dataclass(frozen=True, slots=True)
class Ok[T]:
    """A successful result carrying a value."""

    value: T

    def is_ok(self) -> bool:
        return True


@dataclass(frozen=True, slots=True)
class Err[E]:
    """A failed result carrying an error."""

    error: E

    def is_ok(self) -> bool:
        return False


type Result[T, E] = Ok[T] | Err[E]
