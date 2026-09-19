"""Trainer.process / foundation export admission gate — production bypass removal."""
from __future__ import annotations

from pathlib import Path

import pytest

from swi_core.admission_boundary import AdmissionDecision
from swi_core.foundation_evidence import export_foundation_evidence
from swi_core.module00_trainer import Trainer
from swi_core.module_kernel import AdmissionRequiredError
from test.helpers_admission import (
    TEST_COMMIT,
    export_admission,
    pipeline_admission,
)


def test_process_rejects_without_admission_no_turn_increment(tmp_path):
    trainer = Trainer(str(tmp_path / "audit.log"))
    assert trainer._turn_counter == 0
    with pytest.raises(AdmissionRequiredError, match="STATE_FORMATION_WITHOUT_ADMISSION"):
        trainer.process("hello")
    assert trainer._turn_counter == 0


def test_process_rejects_without_admission_no_audit_file(tmp_path):
    log = tmp_path / "audit.log"
    trainer = Trainer(str(log))
    with pytest.raises(AdmissionRequiredError):
        trainer.process("hello")
    assert not log.exists() or log.read_text(encoding="utf-8").strip() == ""


def test_process_rejects_wrong_module(tmp_path):
    trainer = Trainer(str(tmp_path / "audit.log"), expected_commit=TEST_COMMIT)
    bad = pipeline_admission(module="M05")
    with pytest.raises(AdmissionRequiredError, match="ADMISSION_NOT_VALID_FOR_CONTEXT"):
        trainer.process("hello", admission=bad)
    assert trainer._turn_counter == 0


def test_process_rejects_wrong_commit(tmp_path):
    trainer = Trainer(
        str(tmp_path / "audit.log"),
        expected_commit="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    )
    adm = pipeline_admission(commit=TEST_COMMIT)
    with pytest.raises(AdmissionRequiredError, match="ADMISSION_NOT_VALID_FOR_CONTEXT"):
        trainer.process("hello", admission=adm)
    assert trainer._turn_counter == 0


def test_process_rejects_forged_boolean_like_object(tmp_path):
    trainer = Trainer(str(tmp_path / "audit.log"))

    class Fake:
        def is_valid_for(self, **kwargs):
            return False

    with pytest.raises(AdmissionRequiredError):
        trainer.process("hello", admission=Fake())
    assert trainer._turn_counter == 0


def test_process_accepts_valid_admission(tmp_path):
    trainer = Trainer(str(tmp_path / "audit.log"), expected_commit=TEST_COMMIT)
    result = trainer.process(
        "ordinary customer support message",
        admission=pipeline_admission(),
    )
    assert result.allowed is True
    assert trainer._turn_counter == 1


def test_export_rejects_without_admission(tmp_path):
    trainer = Trainer(str(tmp_path / "audit.log"), expected_commit=TEST_COMMIT)
    result = trainer.process("export me", admission=pipeline_admission())
    with pytest.raises(AdmissionRequiredError, match="STATE_FORMATION_WITHOUT_ADMISSION"):
        export_foundation_evidence(result)


def test_export_accepts_valid_admission(tmp_path):
    trainer = Trainer(str(tmp_path / "audit.log"), expected_commit=TEST_COMMIT)
    result = trainer.process("export me", admission=pipeline_admission())
    env = export_foundation_evidence(
        result,
        admission=export_admission(),
        expected_commit=TEST_COMMIT,
    )
    assert env.integrity_reference
    assert len(env.integrity_reference) == 64


def test_claim_only_decision_cannot_run_process(tmp_path):
    trainer = Trainer(str(tmp_path / "audit.log"))
    claim_only = AdmissionDecision(
        ok=True,
        module="00",
        commit=None,
        decision="ACCEPT_CLAIM_ONLY",
        reason="no artifact",
        execution_authority=False,
    )
    with pytest.raises(AdmissionRequiredError):
        trainer.process("x", admission=claim_only)
    assert trainer._turn_counter == 0
