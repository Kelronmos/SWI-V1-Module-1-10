"""Trainer → Module 05 kernel boundary: halt cannot be bypassed."""
import pytest

from swi_core.module00_trainer import Trainer
from swi_core.module05_redaction_engine import RedactionMatch, RedactionResult
from swi_core.module_kernel import ModuleKernelError


def test_trainer_halts_on_module05_post_failure(tmp_path, monkeypatch):
    trainer = Trainer(str(tmp_path / "audit.log"))
    monkeypatch.setattr(
        trainer.redaction,
        "_redact_impl",
        lambda text: "bad",
    )
    with pytest.raises(ModuleKernelError) as exc:
        trainer.process("hello world")
    assert "halted_by_module_05_kernel" in str(exc.value)


def test_module05_failure_does_not_reach_drift(tmp_path, monkeypatch):
    trainer = Trainer(str(tmp_path / "audit.log"))
    drift_called = {"n": 0}
    monkeypatch.setattr(
        trainer.redaction,
        "_redact_impl",
        lambda text: RedactionResult(
            redacted_text="x",
            matches=[RedactionMatch(category="SECRET", original="x", start=0, end=1)],
        ),
    )

    def spy(text):
        drift_called["n"] += 1
        return None

    monkeypatch.setattr(trainer.drift, "check", spy)
    with pytest.raises(ModuleKernelError):
        trainer.process("ordinary text")
    assert drift_called["n"] == 0


def test_module05_halt_records_reason(tmp_path, monkeypatch):
    trainer = Trainer(str(tmp_path / "audit.log"))
    events = []
    monkeypatch.setattr(trainer.audit, "log_event", lambda e: events.append(e))
    monkeypatch.setattr(trainer.redaction, "_redact_impl", lambda text: None)
    with pytest.raises(ModuleKernelError):
        trainer.process("hello")
    assert events and events[-1].get("halt") is True
    assert "halted_by_module_05_kernel" in str(events[-1].get("reason", ""))


def test_module05_audit_failure_does_not_swallow_halt(tmp_path, monkeypatch):
    trainer = Trainer(str(tmp_path / "audit.log"))
    monkeypatch.setattr(trainer.redaction, "_redact_impl", lambda text: None)

    def boom(_):
        raise RuntimeError("audit down")

    monkeypatch.setattr(trainer.audit, "log_event", boom)
    monkeypatch.setattr(
        trainer.memory,
        "append",
        lambda _: (_ for _ in ()).throw(RuntimeError("memory down")),
    )
    with pytest.raises(ModuleKernelError):
        trainer.process("hello")
