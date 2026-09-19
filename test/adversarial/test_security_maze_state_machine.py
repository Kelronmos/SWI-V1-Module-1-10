"""Security Maze state machine — sandbox escape and retry (SM-V1-002, SM-V1-003).
"""
from __future__ import annotations

import pytest

from swi_core.module_kernel import AdmissionRequiredError
from swi_core.security_maze import (
    AccessState,
    SecurityMaze,
    transition,
)


def test_sandbox_cannot_transition_to_executing():
    with pytest.raises(AdmissionRequiredError, match="INVALID_STATE_TRANSITION"):
        transition(AccessState.SANDBOXED.value, AccessState.EXECUTING.value)


def test_halted_cannot_transition_to_executing():
    with pytest.raises(AdmissionRequiredError, match="INVALID_STATE_TRANSITION"):
        transition(AccessState.HALTED.value, AccessState.EXECUTING.value)


def test_unvalidated_cannot_transition_to_executing():
    with pytest.raises(AdmissionRequiredError, match="INVALID_STATE_TRANSITION"):
        transition(AccessState.UNVALIDATED.value, AccessState.EXECUTING.value)


def test_sandboxed_run_never_sets_privileged_or_executing():
    maze = SecurityMaze()
    run = maze.evaluate_request(
        {"module": "10", "verified": True, "executable": True}
    )
    assert run.state == AccessState.SANDBOXED.value
    assert run.privileged_access is False
    assert run.execution_allowed is False
    assert run.decision == "SANDBOXED"
    with pytest.raises(AdmissionRequiredError):
        transition(run.state, AccessState.EXECUTING.value)


def test_retry_escalation_does_not_grant_authority():
    maze = SecurityMaze()
    run = maze.evaluate_request(
        {"module": "10", "payload_modified": True, "hash_recalculated": True}
    )
    assert run.decision == "SANDBOXED"
    for i in range(50):
        run = maze.retry_does_not_grant_authority(run)
        assert run.retry_count == i + 1
        assert run.privileged_access is False
        assert run.execution_allowed is False
        assert run.state in (
            AccessState.SANDBOXED.value,
            AccessState.HALTED.value,
        )
