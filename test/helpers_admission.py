"""Test-only admission helpers. Not production authority."""
from __future__ import annotations

from swi_core.admission_boundary import AdmissionDecision, issue_admission_decision

# Fixed hex commit for binding tests (valid hex, not a real tip claim)
TEST_COMMIT = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


def pipeline_admission(
    *,
    commit: str | None = TEST_COMMIT,
    module: str = "00",
) -> AdmissionDecision:
    """Valid decision for Trainer.process (module 00)."""
    return issue_admission_decision(
        {
            "module": module,
            "status": "IMPLEMENTED",
            "admission_artifact": {
                "kind": "pipeline_v0",
                "scope": "Trainer.process",
                "test_only": True,
            },
        },
        current_commit=commit,
        grant_execution=True,
        request_identity="test-pipeline",
    )


def export_admission(*, commit: str | None = TEST_COMMIT) -> AdmissionDecision:
    return issue_admission_decision(
        {
            "module": "foundation_export",
            "status": "IMPLEMENTED",
            "admission_artifact": {
                "kind": "export_v0",
                "scope": "export_foundation_evidence",
                "test_only": True,
            },
        },
        current_commit=commit,
        grant_execution=True,
        request_identity="test-export",
    )


def sign_admission(*, commit: str | None = TEST_COMMIT) -> AdmissionDecision:
    return issue_admission_decision(
        {
            "module": "foundation_sign",
            "status": "IMPLEMENTED",
            "admission_artifact": {
                "kind": "sign_v0",
                "scope": "sign_foundation_evidence",
                "test_only": True,
            },
        },
        current_commit=commit,
        grant_execution=True,
        request_identity="test-sign",
    )
