"""Tests for the generic ModuleKernel (not Module 02-specific).

Proves the enforcement mechanism itself is fail-closed before any module
migration depends on it.
"""
import pytest

from swi_core.module_kernel import CheckResult, ModuleKernel, ModuleKernelError


def passing_check(value):
    return CheckResult(name="pass", passed=True)


def failing_check(value):
    return CheckResult(name="fail", passed=False, reason="intentional failure")


def test_pre_fails_operation_never_runs():
    called = {"n": 0}

    def operation(value):
        called["n"] += 1
        return value

    kernel = ModuleKernel(name="test", pre_checks=[failing_check])
    with pytest.raises(ModuleKernelError) as exc:
        kernel.run("input", operation)
    assert called["n"] == 0
    assert "pre-check" in str(exc.value)


def test_pre_passes_operation_runs():
    called = {"n": 0}

    def operation(value):
        called["n"] += 1
        return value.upper()

    kernel = ModuleKernel(name="test", pre_checks=[passing_check])
    assert kernel.run("input", operation) == "INPUT"
    assert called["n"] == 1


def test_operation_exception_is_visible():
    def operation(value):
        raise RuntimeError("operation boom")

    kernel = ModuleKernel(name="test", pre_checks=[passing_check])
    with pytest.raises(RuntimeError, match="operation boom"):
        kernel.run("input", operation)


def test_post_fails_output_never_released():
    kernel = ModuleKernel(name="test", post_checks=[failing_check])
    with pytest.raises(ModuleKernelError) as exc:
        result = kernel.run("input", lambda value: "SECRET_OUTPUT")
        pytest.fail(f"output was released: {result!r}")
    assert "post-check" in str(exc.value)


def test_post_passes_output_released():
    kernel = ModuleKernel(
        name="test",
        pre_checks=[passing_check],
        post_checks=[passing_check],
    )
    assert kernel.run("input", lambda value: "ok") == "ok"


def test_check_crash_fail_closed():
    def broken(value):
        raise RuntimeError("check boom")

    kernel = ModuleKernel(name="test", pre_checks=[broken])
    with pytest.raises(ModuleKernelError):
        kernel.run("input", lambda value: value)


def test_bad_check_type_fail_closed():
    def bad_check(value):
        return True  # not CheckResult

    kernel = ModuleKernel(name="test", pre_checks=[bad_check])
    with pytest.raises(ModuleKernelError):
        kernel.run("input", lambda value: value)


def test_post_check_crash_fail_closed():
    def broken_post(value):
        raise ValueError("post boom")

    kernel = ModuleKernel(name="test", post_checks=[broken_post])
    with pytest.raises(ModuleKernelError):
        kernel.run("input", lambda value: value)


def test_multiple_pre_checks_any_fail_halts():
    order = []

    def a(value):
        order.append("a")
        return CheckResult(name="a", passed=True)

    def b(value):
        order.append("b")
        return CheckResult(name="b", passed=False, reason="b failed")

    def c(value):
        order.append("c")
        return CheckResult(name="c", passed=True)

    kernel = ModuleKernel(name="test", pre_checks=[a, b, c])
    called = False

    def operation(value):
        nonlocal called
        called = True
        return value

    with pytest.raises(ModuleKernelError):
        kernel.run("x", operation)
    assert called is False
    assert "b" in order
