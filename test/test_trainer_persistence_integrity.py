"""Trainer M07/M09 persistence integrity — fail-closed on normal path."""
import json

import pytest

from swi_core.config_loader import ConfigError, load_config
from swi_core.module00_trainer import Trainer
from swi_core.module06_drift_analyzer import DriftResult
from swi_core.module_kernel import ModuleKernelError
from test.helpers_admission import TEST_COMMIT, pipeline_admission


def _trainer(tmp_path):
    return Trainer(str(tmp_path / "audit.log"), expected_commit=TEST_COMMIT)


def test_corrupt_memory_chain_fails_closed(tmp_path):
    trainer = _trainer(tmp_path)
    trainer.memory.append({"event": "trusted"})
    trainer.memory.tamper_for_testing(0, {"event": "tampered"})
    with pytest.raises(ModuleKernelError) as exc:
        trainer.process("hello", admission=pipeline_admission())
    assert "halted_by_module_07_integrity" in str(exc.value)


def test_memory_append_failure_fails_closed(tmp_path, monkeypatch):
    trainer = _trainer(tmp_path)

    def boom(_payload):
        raise RuntimeError("memory unavailable")

    monkeypatch.setattr(trainer.memory, "append", boom)
    with pytest.raises(ModuleKernelError) as exc:
        trainer.process("hello", admission=pipeline_admission())
    assert "halted_by_module_07_integrity" in str(exc.value)


def test_corrupt_audit_chain_fails_closed(tmp_path):
    log_path = tmp_path / "audit.log"
    trainer = Trainer(str(log_path), expected_commit=TEST_COMMIT)
    trainer.process("first", admission=pipeline_admission())
    lines = log_path.read_text().strip().splitlines()
    assert lines
    rec = json.loads(lines[0])
    rec["event"] = {"tampered": True}
    log_path.write_text(json.dumps(rec) + "\n")
    with pytest.raises(ModuleKernelError) as exc:
        trainer.process("second", admission=pipeline_admission())
    assert "halted_by_module_09_integrity" in str(exc.value)


def test_audit_write_failure_fails_closed(tmp_path, monkeypatch):
    trainer = _trainer(tmp_path)

    def boom(_event):
        raise RuntimeError("audit unavailable")

    monkeypatch.setattr(trainer.audit, "log_event", boom)
    with pytest.raises(ModuleKernelError) as exc:
        trainer.process("hello", admission=pipeline_admission())
    assert "halted_by_module_09_persistence" in str(exc.value)


def test_halt_recording_failure_does_not_create_success(tmp_path, monkeypatch):
    trainer = _trainer(tmp_path)

    def boom_mem(_payload):
        raise RuntimeError("memory down")

    def boom_audit(_event):
        raise RuntimeError("audit down")

    monkeypatch.setattr(trainer.memory, "append", boom_mem)
    monkeypatch.setattr(trainer.audit, "log_event", boom_audit)
    monkeypatch.setattr(
        trainer.drift,
        "_check_impl",
        lambda text: DriftResult(similarity=2.0, drifted=False),
    )
    with pytest.raises(ModuleKernelError) as exc:
        trainer.process("hello world", admission=pipeline_admission())
    assert "halted_by_module_06_kernel" in str(exc.value)


def test_trainer_wires_drift_threshold_from_config(tmp_path):
    config_path = tmp_path / "swi.yaml"
    config_path.write_text("drift_analyzer:\n  drift_threshold: 0.9\n")
    trainer = Trainer(
        str(tmp_path / "audit.log"),
        config_path=str(config_path),
        expected_commit=TEST_COMMIT,
    )
    assert trainer.drift.drift_threshold == 0.9


def test_invalid_block_threshold_raises(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("security_probe:\n  block_threshold: 2.0\n")
    with pytest.raises(ConfigError):
        load_config(str(p))


def test_invalid_drift_threshold_raises(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("drift_analyzer:\n  drift_threshold: -1.0\n")
    with pytest.raises(ConfigError):
        load_config(str(p))


def test_invalid_staleness_raises(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("context_sync:\n  staleness_seconds: -1\n")
    with pytest.raises(ConfigError):
        load_config(str(p))
