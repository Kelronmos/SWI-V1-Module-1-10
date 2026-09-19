"""Serialized travel: PipelineResult → envelope → JSON → reload integrity."""
from __future__ import annotations

import json

from swi_core.foundation_evidence import (
    VERIFICATION_STATUS_V1_PIPELINE,
    compute_integrity_reference,
    envelope_to_dict,
    export_foundation_evidence,
)
from swi_core.module00_trainer import Trainer
from test.helpers_admission import TEST_COMMIT, export_admission, pipeline_admission


def test_json_roundtrip_preserves_integrity(tmp_path):
    trainer = Trainer(str(tmp_path / "audit.log"), expected_commit=TEST_COMMIT)
    result = trainer.process(
        "cross-repo travel test user@example.com",
        admission=pipeline_admission(),
    )
    env = export_foundation_evidence(
        result,
        admission=export_admission(),
        expected_commit=TEST_COMMIT,
        evidence_id="v1-json-travel-001",
    )
    assert env.verification_status == VERIFICATION_STATUS_V1_PIPELINE

    raw = json.dumps(envelope_to_dict(env), sort_keys=True, separators=(",", ":"))
    loaded = json.loads(raw)

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
    trainer = Trainer(str(tmp_path / "audit.log"), expected_commit=TEST_COMMIT)
    env = export_foundation_evidence(
        trainer.process("tamper travel", admission=pipeline_admission()),
        admission=export_admission(),
        expected_commit=TEST_COMMIT,
        evidence_id="v1-json-tamper-001",
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
