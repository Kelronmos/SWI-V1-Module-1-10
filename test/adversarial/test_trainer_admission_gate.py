"""Trainer.process / foundation export admission gate — production bypass removal."""
from __future__ import annotations

import inspect
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

ROOT = Path(__file__).resolve().parents[2]


def test_process_requires_admission_keyword():
    """Omitting admission is a TypeError — no silent ungated path."""
    sig = inspect.signature(Trainer.process)
    param = sig.parameters["admission"]
    assert param.kind is inspect.Parameter.KEYWORD_ONLY
    assert param.default is inspect.Parameter.empty


def test_process_rejects_missing_admission_typeerror(tmp_path):
    trainer = Trainer(str(tmp_path / "audit.log"))
    with pytest.raises(TypeError):
        trainer.process("hello")  # type: ignore[call-arg]
    assert trainer._turn_counter == 0


def test_process_rejects_invalid_admission_no_turn_increment(tmp_path):
    trainer = Trainer(str(tmp_path / "audit.log"))
    with pytest.raises(AdmissionRequiredError, match="ADMISSION_NOT_VALID_FOR_CONTEXT"):
        trainer.process(
            "hello",
            admission=AdmissionDecision(
                ok=False,
                module="00",
                commit=None,
                decision="REJECT",
                reason="forced",
                execution_authority=False,
            ),
        )
    assert trainer._turn_counter == 0


def test_process_rejects_without_valid_admission_no_audit_file(tmp_path):
    log = tmp_path / "audit.log"
    trainer = Trainer(str(log))
    with pytest.raises(AdmissionRequiredError):
        trainer.process(
            "hello",
            admission=AdmissionDecision(
                ok=True,
                module="wrong",
                commit=None,
                decision="ADMITTED",
                reason="x",
                execution_authority=True,
            ),
        )
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
        trainer.process("hello", admission=Fake())  # type: ignore[arg-type]
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


def test_source_order_admission_before_turn_counter():
    """Regression: admission check must appear before _turn_counter in process()."""
    src = (ROOT / "swi_core" / "module00_trainer.py").read_text(encoding="utf-8")
    # Narrow to process method body
    start = src.index("def process(")
    body = src[start : src.index("return PipelineResult", start)]
    assert body.index("_require_admission") < body.index("_turn_counter += 1")


def test_child_module_kernels_still_default_ungated():
    """Residual surface: Universal Gate remains NOT PROVEN until these change."""
    from swi_core.module02_security_probe import SecurityProbe

    probe = SecurityProbe()
    assert probe.kernel.require_admission is False
