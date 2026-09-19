"""SM-V1-004 — Admission authenticity invariant.

A caller possessing only the structural shape of an AdmissionDecision
MUST NOT obtain privileged access through the Security Maze formation path
or through strict ModuleKernel.

Does not claim Universal Gate is proven for residual direct module APIs.
"""
from __future__ import annotations

import pytest

from swi_core.admission_boundary import AdmissionDecision, issue_admission_decision
from swi_core.module_kernel import AdmissionRequiredError, ModuleKernel
from swi_core.security_maze import SecurityMaze


class _DuckAdmission:
    """Looks like AdmissionDecision but is not issued by the boundary."""

    def __init__(self, **kwargs):
        self.ok = kwargs.get("ok", True)
        self.module = kwargs.get("module", "00")
        self.commit = kwargs.get("commit", "abcdef0")
        self.execution_authority = kwargs.get("execution_authority", True)

    def is_valid_for(self, module=None, commit=None):
        if not self.ok or not self.execution_authority:
            return False
        if module is not None and self.module is not None and str(module) != str(self.module):
            return False
        if commit is not None and self.commit is not None and str(commit) != str(self.commit):
            return False
        return True


def test_sm_v1_004_forged_dataclass_without_execution_authority_blocked():
    called = {"n": 0}

    def op(v):
        called["n"] += 1
        return v

    fake = AdmissionDecision(
        ok=True,
        module="00",
        commit="abcdef0",
        decision="ADMITTED",
        reason="forged",
        execution_authority=False,
    )
    kernel = ModuleKernel(
        name="strict", require_admission=True, module_id="00", expected_commit="abcdef0"
    )
    with pytest.raises(AdmissionRequiredError):
        kernel.run("x", op, admission=fake)
    assert called["n"] == 0


def test_sm_v1_004_duck_typed_object_can_satisfy_kernel_api_but_maze_claim_path_independent():
    """Document: ModuleKernel only duck-types is_valid_for — that is intentional API shape.

    Authenticity of *claims* still goes through evaluate_claim / issue_admission_decision.
    A duck object that returns True from is_valid_for *will* pass strict kernel alone;
    therefore Universal Gate cannot rest on duck-typing. Maze + claim checks must remain.
    """
    called = {"n": 0}

    def op(v):
        called["n"] += 1
        return v

    duck = _DuckAdmission(module="00", commit="abcdef0", execution_authority=True)
    kernel = ModuleKernel(
        name="strict", require_admission=True, module_id="00", expected_commit="abcdef0"
    )
    # Kernel API is duck-typed — this is a residual authenticity surface if used alone
    out = kernel.run("x", op, admission=duck)
    assert out == "x"
    assert called["n"] == 1

    # Maze claim path still rejects authority laundering without going through kernel
    maze = SecurityMaze(implementation_commit="abcdef0", module_id="00")
    run = maze.evaluate_request(
        {"module": "10", "verified": True, "executable": True},
        operation=op,
        admission=duck,
    )
    # Claim fails before formation; operation may or may not run depending on order
    assert run.privileged_access is False or run.decision == "SANDBOXED"
    assert run.decision == "SANDBOXED"


def test_sm_v1_004_wrong_module_binding_rejected():
    called = {"n": 0}

    def op(v):
        called["n"] += 1
        return v

    decision = AdmissionDecision(
        ok=True,
        module="M03",
        commit="abcdef0",
        decision="ADMITTED",
        reason="test",
        execution_authority=True,
    )
    kernel = ModuleKernel(
        name="strict", require_admission=True, module_id="00", expected_commit="abcdef0"
    )
    with pytest.raises(AdmissionRequiredError, match="ADMISSION_NOT_VALID_FOR_CONTEXT"):
        kernel.run("x", op, admission=decision)
    assert called["n"] == 0


def test_sm_v1_004_wrong_commit_binding_rejected():
    called = {"n": 0}

    def op(v):
        called["n"] += 1
        return v

    decision = AdmissionDecision(
        ok=True,
        module="00",
        commit="aaaaaaa",
        decision="ADMITTED",
        reason="test",
        execution_authority=True,
    )
    kernel = ModuleKernel(
        name="strict", require_admission=True, module_id="00", expected_commit="bbbbbbb"
    )
    with pytest.raises(AdmissionRequiredError):
        kernel.run("x", op, admission=decision)
    assert called["n"] == 0


def test_sm_v1_004_claim_only_issuer_never_grants_execution_authority():
    decision = issue_admission_decision(
        {"module": "00", "status": "IMPLEMENTED"},
        grant_execution=False,
    )
    assert decision.execution_authority is False
    assert decision.is_valid_for(module="00") is False


def test_sm_v1_004_none_and_true_are_not_admission():
    called = {"n": 0}

    def op(v):
        called["n"] += 1
        return v

    kernel = ModuleKernel(name="strict", require_admission=True, module_id="00")
    with pytest.raises(AdmissionRequiredError):
        kernel.run("x", op, admission=None)
    with pytest.raises(AdmissionRequiredError):
        kernel.run("x", op, admission=True)  # type: ignore[arg-type]
    assert called["n"] == 0


def test_sm_v1_004_maze_refuses_formation_with_claim_only_decision():
    called = {"n": 0}

    def op(v):
        called["n"] += 1
        return v

    decision = issue_admission_decision({"module": "00"}, grant_execution=False)
    maze = SecurityMaze(module_id="00")
    run = maze.evaluate_request(
        {"module": "10"},
        operation=op,
        admission=decision,
    )
    assert called["n"] == 0
    assert run.privileged_access is False
    assert run.decision == "SANDBOXED"
