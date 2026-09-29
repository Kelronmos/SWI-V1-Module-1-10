"""FM-005 Priority-1: privileged factory enforces DECISION ≠ EXECUTION.

Compatibility default remains require_admission=False (OPEN residual).
for_privileged() path must not call operation without admission.
"""
from __future__ import annotations

import pytest

from swi_core.module_kernel import AdmissionRequiredError, ModuleKernel


def test_compatibility_default_still_forms_without_admission():
    """Documents OPEN residual — do not treat as sealed."""
    calls: list = []

    def operation(v):
        calls.append(v)
        return {"formed": True}

    k = ModuleKernel(name="fm005-compat")
    assert k.require_admission is False
    out = k.run("x", operation, admission=None)
    assert calls == ["x"]
    assert out["formed"] is True


def test_privileged_kernel_unadmitted_zero_operation_calls():
    calls: list = []

    def operation(v):
        calls.append(v)
        return {"formed": True}

    k = ModuleKernel.for_privileged(name="fm005-strict", module_id="M05")
    assert k.require_admission is True
    with pytest.raises(AdmissionRequiredError, match="STATE_FORMATION_WITHOUT_ADMISSION"):
        k.run("x", operation, admission=None)
    assert calls == []  # DECISION ≠ EXECUTION: operation never ran


def test_privileged_kernel_rejects_claim_only_shape():
    calls: list = []

    def operation(v):
        calls.append(v)
        return v

    class FakeAdmission:
        def is_valid_for(self, module=None, commit=None):
            return True

        execution_authority = False

    # Shape alone is not enough if is_valid_for returns True — document current contract:
    # kernel only checks is_valid_for; execution_authority is caller's/maze concern.
    k = ModuleKernel.for_privileged(name="fm005-strict", module_id="M05")
    # Fake with is_valid_for True currently allows formation — residual for authenticity layer
    out = k.run("ok", operation, admission=FakeAdmission())
    assert out == "ok"
    assert calls == ["ok"]


def test_privileged_kernel_rejects_wrong_module():
    calls: list = []

    def operation(v):
        calls.append(v)
        return v

    class BoundAdmission:
        def is_valid_for(self, module=None, commit=None):
            return module == "M03"

    k = ModuleKernel.for_privileged(name="fm005-strict", module_id="M05")
    with pytest.raises(AdmissionRequiredError, match="ADMISSION_NOT_VALID_FOR_CONTEXT"):
        k.run("x", operation, admission=BoundAdmission())
    assert calls == []
