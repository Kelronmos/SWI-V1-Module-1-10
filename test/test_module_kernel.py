"""Tests for the generic ModuleKernel (not Module 02-specific)."""
import pytest

from swi_core.module_kernel import CheckResult, ModuleKernel, ModuleKernelError


def passing_check(value):
    return CheckResult(name="pass", passed=True)


def failing_check(value):
    return CheckResult(name="fail", passed=False, reason="intentional failure")


def test_kernel_runs_operation_when_precheck_passes():
    kernel = ModuleKernel(name="test", pre_checks=[passing_check])
    result = kernel.run("input", lambda value: value.upper())
    assert result == "INPUT"


def test_kernel_blocks_operation_when_precheck_fails():
    called = False

    def operation(value):
        nonlocal called
        called = True
        return value

    kernel = ModuleKernel(name="test", pre_checks=[failing_check])
    with pytest.raises(ModuleKernelError):
        kernel.run("input", operation)
    assert called is False


def test_kernel_blocks_failed_postcheck():
    kernel = ModuleKernel(name="test", post_checks=[failing_check])
    with pytest.raises(ModuleKernelError):
        kernel.run("input", lambda value: value)


def test_kernel_accepts_valid_pre_and_post_checks():
    kernel = ModuleKernel(
        name="test",
        pre_checks=[passing_check],
        post_checks=[passing_check],
    )
    assert kernel.run("input", lambda value: value) == "input"


def test_kernel_fails_if_check_returns_wrong_type():
    def bad_check(value):
        return True

    kernel = ModuleKernel(name="test", pre_checks=[bad_check])
    with pytest.raises(ModuleKernelError):
        kernel.run("input", lambda value: value)


def test_kernel_fails_if_check_raises():
    def broken(value):
        raise RuntimeError("boom")

    kernel = ModuleKernel(name="test", pre_checks=[broken])
    with pytest.raises(ModuleKernelError):
        kernel.run("input", lambda value: value)
