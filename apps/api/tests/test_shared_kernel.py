"""Shared-kernel Result primitives behave as a tagged success/failure union."""

from northstar.shared_kernel import DomainError, Err, Ok


def test_ok_carries_value_and_is_ok():
    result = Ok(42)
    assert result.is_ok()
    assert result.value == 42


def test_err_carries_error_and_is_not_ok():
    result = Err(DomainError(code="not_found", message="missing"))
    assert not result.is_ok()
    assert result.error.code == "not_found"
