"""Serialized travel: PipelineResult → envelope → JSON → reload integrity."""
from __future__ import annotations

import json

import pytest

from swi_core.foundation_evidence import (
    VERIFICATION_STATUS_V1_PIPELINE,
    compute_integrity_reference,
    envelope_to_dict,
    export_foundation_evidence,
)
from swi_core.module00_trainer import Trainer


def test_json_roundtrip_preserves_integrity(tmp_path):
    trainer = Trainer(str(tmp_path / "audit.log"))
    result = trainer.process("cross-repo travel test user@example.com")
    env = export_foundation_evidence(result, evidence_id="v1-json-travel-001")
    assert env.verification_status == VERIFICATION_STATUS_V1_PIPELINE

    # Serialize as if crossing a process/repo boundary (no shared memory).
    raw = json.dumps(envelope_to_dict(env), sort_keys=True, separators=(",", ":"))
    loaded = json.loads(raw)

    # created_at may be present; must not be required for integrity match
    expected = compute_integrity_reference(
        loaded["payload"],
        loaded["foundation_version"],
        loaded["evidence_schema_version"],
        loaded["evidence_id"],
        loaded["source_reference"],
    )
    assert loaded["integrity_reference"] == expected
    assert loaded["verification_status"] == VERIFICATION_STATUS_V1_PIPELINE
    assert "created_at" in loaded


def test_json_tamper_breaks_integrity(tmp_path):
    trainer = Trainer(str(tmp_path / "audit.log"))
    env = export_foundation_evidence(
        trainer.process("tamper travel"), evidence_id="v1-json-tamper-001"
    )
    loaded = json.loads(json.dumps(envelope_to_dict(env)))
    loaded["payload"] = dict(loaded["payload"])
    loaded["payload"]["allowed"] = not loaded["payload"]["allowed"]
    expected = compute_integrity_reference(
        loaded["payload"],
        loaded["foundation_version"],
        loaded["evidence_schema_version"],
        loaded["evidence_id"],
        loaded["source_reference"],
    )
    assert expected != loaded["integrity_reference"]
