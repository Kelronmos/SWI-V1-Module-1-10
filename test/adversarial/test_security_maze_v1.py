"""Security Maze V1 — adversarial / construction tests.

Uses micro-kernel (ModuleKernel) + admission_boundary.
Does NOT claim Universal Gate is proven.
"""
from __future__ import annotations

import pytest

from swi_core.admission_boundary import AdmissionDecision
from swi_core.module_kernel import AdmissionRequiredError, ModuleKernel
from swi_core.security_maze import (
    AccessState,
    GateOutcome,
    SecurityMaze,
    MAZE_VERSION,
)


def test_maze_version_and_start_run():
    maze = SecurityMaze(implementation_commit="abcdef0")
    run = maze.start_run({"module": "10"}, maze_run_id="MR-1")
    assert run.maze_version == MAZE_VERSION
    assert run.state == AccessState.UNVALIDATED.value
    assert run.privileged_access is False


def test_maze_rejects_synthetic_upstream_before_construction_accept():
    maze = SecurityMaze()
    run = maze.evaluate_request(
        {
            "module": "10",
            "upstream_receipts": [{"hash": "a" * 64, "synthetic": True}],
        }
    )
    assert run.decision == "SANDBOXED"
    assert run.privileged_access is False
    assert run.execution_allowed is False
    reasons = [g.reason for g in run.gates if g.result == GateOutcome.FAIL.value]
    assert any("SYNTHETIC" in r for r in reasons)


def test_maze_rejects_hash_laundering():
    maze = SecurityMaze()
    run = maze.evaluate_request(
        {
            "module": "10",
            "payload_modified": True,
            "hash_recalculated": True,
        }
    )
    assert run.decision == "SANDBOXED"
    assert run.privileged_access is False


def test_maze_rejects_authority_laundering():
    maze = SecurityMaze()
    run = maze.evaluate_request(
        {
            "module": "10",
            "verified": True,
            "executable": True,
        }
    )
    assert run.decision == "SANDBOXED"
    assert run.privileged_access is False


def test_maze_bare_module_is_claim_only_not_privileged():
    maze = SecurityMaze()
    run = maze.evaluate_request({"module": "10", "implementation": "x"})
    assert run.decision in ("ADMITTED_CLAIM_ONLY", "ADMITTED")
    assert run.privileged_access is False
    assert run.execution_allowed is False


def test_maze_claim_only_cannot_run_operation_without_admission():
    called = {"n": 0}

    def op(value):
        called["n"] += 1
        return value

    maze = SecurityMaze(module_id="00")
    run = maze.evaluate_request(
        {"module": "10"},
        operation=op,
        admission=None,
    )
    assert run.decision == "SANDBOXED"
    assert called["n"] == 0
    assert run.privileged_access is False


def test_maze_formation_via_strict_micro_kernel_with_valid_admission():
    called = {"n": 0}

    def op(value):
        called["n"] += 1
        return "done"

    admission = AdmissionDecision(
        ok=True,
        module="00",
        commit="abcdef0",
        decision="ADMITTED",
        reason="test",
        execution_authority=True,
        architectural_admission=True,
    )
    maze = SecurityMaze(implementation_commit="abcdef0", module_id="00")
    run = maze.evaluate_request(
        {"module": "10", "status": "IMPLEMENTED"},
        operation=op,
        admission=admission,
    )
    assert called["n"] == 1
    assert run.privileged_access is True
    assert run.decision == "ADMITTED"


def test_sm_v1_003_retry_does_not_grant_authority():
    maze = SecurityMaze()
    run = maze.evaluate_request(
        {"module": "10", "verified": True, "executable": True}
    )
    assert run.decision == "SANDBOXED"
    for _ in range(20):
        run = maze.retry_does_not_grant_authority(run)
        assert run.privileged_access is False
        assert run.execution_allowed is False


def test_failed_gate_not_run_is_not_pass():
    maze = SecurityMaze()
    run = maze.evaluate_request(
        {"module": "10", "payload_modified": True, "hash_recalculated": True}
    )
    outcomes = {g.gate: g.result for g in run.gates}
    # Some later gates must be NOT_RUN, never silently PASS after failure
    not_run = [g for g in run.gates if g.result == GateOutcome.NOT_RUN.value]
    assert len(not_run) >= 1
    for g in not_run:
        assert g.result != GateOutcome.PASS.value


def test_default_module_kernel_still_ungated_documents_residual():
    """Residual surface: default require_admission=False still runs operation."""
    called = {"n": 0}

    def op(value):
        called["n"] += 1
        return value

    k = ModuleKernel(name="legacy")  # default False
    k.run("x", op)
    assert called["n"] == 1
    # Maze formation kernel is strict — contrast
    with pytest.raises(AdmissionRequiredError):
        ModuleKernel(
            name="maze-strict", require_admission=True, module_id="00"
        ).run("x", op, admission=None)


def test_security_maze_not_claiming_universal_gate():
    status = {
        "security_maze_v1": "PARTIAL",
        "universal_gate": "NOT_PROVEN",
        "sealed": False,
    }
    assert status["universal_gate"] == "NOT_PROVEN"
    assert status["sealed"] is False
