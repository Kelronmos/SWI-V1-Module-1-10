"""V1 Foundation Evidence producer tests — real PipelineResult export."""
from __future__ import annotations

import pytest

from swi_core.foundation_evidence import (
    VERIFICATION_STATUS_V1_PIPELINE,
    compute_integrity_reference,
    envelope_to_dict,
    export_foundation_evidence,
)
from swi_core.module00_trainer import Trainer
from swi_core.module_kernel import ModuleKernelError


@pytest.fixture
def trainer(tmp_path):
    return Trainer(str(tmp_path / "audit.log"))


def test_export_from_successful_pipeline(trainer):
    result = trainer.process("hello world contact@example.com")
    env = export_foundation_evidence(result)
    assert env.foundation_version == "1.0-proposed"
    assert env.evidence_schema_version == "1.0-proposed"
    assert env.verification_status == VERIFICATION_STATUS_V1_PIPELINE
    assert env.source_reference.startswith("Kelronmos/SWI-V1-Module-1-10")
    expected = compute_integrity_reference(
        env.payload,
        env.foundation_version,
        env.evidence_schema_version,
        env.evidence_id,
        env.source_reference,
    )
    assert env.integrity_reference == expected
    assert "allowed" in env.payload
    assert "security" in env.payload
    assert "sync" in env.payload
    assert env.payload["redaction"] is not None


def test_export_rejects_non_pipeline_result():
    with pytest.raises(TypeError):
        export_foundation_evidence({"allowed": True})  # type: ignore[arg-type]


def test_envelope_to_dict_serializable(trainer):
    result = trainer.process("plain text")
    env = export_foundation_evidence(result, evidence_id="v1-test-fixed-id")
    d = envelope_to_dict(env)
    assert d["evidence_id"] == "v1-test-fixed-id"
    assert d["verification_status"] == VERIFICATION_STATUS_V1_PIPELINE
    assert isinstance(d["integrity_reference"], str)
    assert len(d["integrity_reference"]) == 64


def test_integrity_changes_when_payload_mutated(trainer):
    result = trainer.process("alpha beta")
    env = export_foundation_evidence(result)
    tampered = dict(env.payload)
    tampered["allowed"] = not tampered["allowed"]
    bad = compute_integrity_reference(
        tampered,
        env.foundation_version,
        env.evidence_schema_version,
        env.evidence_id,
        env.source_reference,
    )
    assert bad != env.integrity_reference


def test_halt_does_not_produce_success_export(trainer, monkeypatch):
    def boom(*a, **k):
        raise ModuleKernelError("forced")

    monkeypatch.setattr(trainer.security, "scan", boom)
    with pytest.raises(ModuleKernelError):
        trainer.process("x")
