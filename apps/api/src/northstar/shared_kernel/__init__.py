"""Shared kernel — domain primitives shared across contexts. Keep it tiny."""

from northstar.shared_kernel.result import DomainError, Err, Ok, Result

__all__ = ["DomainError", "Err", "Ok", "Result"]
