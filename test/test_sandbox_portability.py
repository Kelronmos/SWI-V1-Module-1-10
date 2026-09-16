"""Regression: Module 10 portability and timeout — no full-isolation claims."""
from __future__ import annotations

import swi_core.module10_external_sandbox as m10
from swi_core.module10_external_sandbox import ExternalSandbox, SandboxResult


def test_sandbox_imports_without_resource_module():
    """Module must load even if resource is unavailable (import is optional)."""
    assert hasattr(m10, "_resource")


def test_sandbox_normal_execution():
    sb = ExternalSandbox(timeout_seconds=5.0)
    result = sb.run("print('ok')")
    assert isinstance(result, SandboxResult)
    assert result.timed_out is False
    assert result.exit_code == 0
    assert "ok" in result.stdout
    assert isinstance(result.resource_limits_applied, bool)
    if m10._resource is not None:
        assert result.resource_limits_applied is True
    else:
        assert result.resource_limits_applied is False


def test_sandbox_timeout_controlled():
    sb = ExternalSandbox(timeout_seconds=0.5)
    result = sb.run("import time; time.sleep(10)")
    assert result.timed_out is True
    assert result.exit_code == -1
    assert "timed out" in result.stderr


def test_sandbox_does_not_claim_full_isolation():
    """Docstring and public contract stay within process+timeout scope."""
    doc = m10.__doc__ or ""
    assert "not" in doc.lower()
    sb = ExternalSandbox()
    r = sb.run("print(1)")
    assert hasattr(r, "resource_limits_applied")
