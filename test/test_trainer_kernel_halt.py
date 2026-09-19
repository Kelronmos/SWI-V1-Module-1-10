"""Seal the Trainer → Module 02 boundary: halt cannot be bypassed."""
import pytest

from swi_core.module00_trainer import Trainer
from swi_core.module02_security_probe import ProbeResult
from swi_core.module_kernel import ModuleKernelError
from test.helpers_admission import TEST_COMMIT, pipeline_admission


def _trainer(tmp_path):
    return Trainer(str(tmp_path / "audit.log"), expected_commit=TEST_COMMIT)


def test_precheck_failure_probe_impl_never_runs(tmp_path, monkeypatch):
    trainer = _trainer(tmp_path)
    called = {"n": 0}
    original = trainer.security._scan_impl

    def wrapped(text):
        called["n"] += 1
        return original(text)

    monkeypatch.setattr(trainer.security, "_scan_impl", wrapped)
    with pytest.raises(ModuleKernelError):
        trainer.process(12345, admission=pipeline_admission())  # type: ignore[arg-type]
    assert called["n"] == 0


def test_postcheck_failure_halts_trainer(tmp_path, monkeypatch):
    trainer = _trainer(tmp_path)

    def bad_impl(text):
        return ProbeResult(risk_score=2.5, triggered=["x"], block_threshold=0.5)

    monkeypatch.setattr(trainer.security, "_scan_impl", bad_impl)
    with pytest.raises(ModuleKernelError) as exc:
        trainer.process("hello", admission=pipeline_admission())
    msg = str(exc.value)
    assert "halted_by_module_02_kernel" in msg or "post-check" in msg


def test_kernel_exception_not_swallowed(tmp_path):
    trainer = _trainer(tmp_path)
    with pytest.raises(ModuleKernelError):
        trainer.process(None, admission=pipeline_admission())  # type: ignore[arg-type]


def test_halt_records_reason_when_audit_works(tmp_path, monkeypatch):
    trainer = _trainer(tmp_path)
    events = []

    def capture(event):
        events.append(event)
        return None

    monkeypatch.setattr(trainer.audit, "log_event", capture)
    with pytest.raises(ModuleKernelError):
        trainer.process(999, admission=pipeline_admission())  # type: ignore[arg-type]
    assert events, "halt should attempt audit recording"
    assert events[-1].get("halt") is True
    assert events[-1].get("allowed") is False
    assert "halted_by_module_02_kernel" in str(events[-1].get("reason", ""))


def test_audit_failure_does_not_swallow_kernel_halt(tmp_path, monkeypatch):
    """Best-effort audit must not become a security bypass."""
    trainer = _trainer(tmp_path)

    def boom(_event):
        raise RuntimeError("audit unavailable")

    monkeypatch.setattr(trainer.audit, "log_event", boom)
    monkeypatch.setattr(
        trainer.memory,
        "append",
        lambda _payload: (_ for _ in ()).throw(RuntimeError("memory unavailable")),
    )
    with pytest.raises(ModuleKernelError):
        trainer.process(12345, admission=pipeline_admission())  # type: ignore[arg-type]


def test_failed_module_02_does_not_reach_redaction(tmp_path, monkeypatch):
    trainer = _trainer(tmp_path)
    redact_called = {"n": 0}
    original = trainer.redaction.redact

    def spy(text):
        redact_called["n"] += 1
        return original(text)

    monkeypatch.setattr(trainer.redaction, "redact", spy)
    with pytest.raises(ModuleKernelError):
        trainer.process(["not-a-string"], admission=pipeline_admission())  # type: ignore[arg-type]
    assert redact_called["n"] == 0


def test_failed_module_02_does_not_reach_drift(tmp_path, monkeypatch):
    trainer = _trainer(tmp_path)
    drift_called = {"n": 0}

    def spy(text):
        drift_called["n"] += 1
        return None

    monkeypatch.setattr(trainer.drift, "check", spy)
    with pytest.raises(ModuleKernelError):
        trainer.process(object(), admission=pipeline_admission())  # type: ignore[arg-type]
    assert drift_called["n"] == 0


def test_successful_probe_still_allows_downstream(tmp_path):
    trainer = _trainer(tmp_path)
    result = trainer.process(
        "ordinary customer support message",
        admission=pipeline_admission(),
    )
    assert result.security is not None
    assert result.redaction is not None
    assert result.allowed is True
