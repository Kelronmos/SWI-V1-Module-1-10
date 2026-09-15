"""Module 06 kernel — contract enforcement; drifted remains advisory."""
from collections import Counter

import pytest

from swi_core.module00_trainer import Trainer
from swi_core.module02_security_probe import ProbeResult
from swi_core.module06_drift_analyzer import DriftAnalyzer, DriftResult
from swi_core.module_kernel import ModuleKernelError


def test_topic_shift_still_detected():
    a = DriftAnalyzer(0.35)
    a.set_baseline(["quarterly revenue and expense forecasts for the finance team"])
    r = a.check("recipe for chocolate cake with vanilla frosting")
    assert r.drifted is True


def test_similar_topic_not_drifted():
    a = DriftAnalyzer(0.35)
    a.set_baseline(["quarterly revenue and expense forecasts for the finance team"])
    r = a.check(
        "quarterly revenue forecasts look strong for the finance team this year"
    )
    assert r.drifted is False


def test_strict_threshold_equality_not_drifted():
    a = DriftAnalyzer(0.5)
    a._baseline = Counter({"a": 1})
    a.drift_threshold = 1.0
    r = a.check("a")
    assert r.similarity == pytest.approx(1.0)
    assert r.drifted is False


def test_empty_baseline_preserved():
    a = DriftAnalyzer(0.35)
    r = a.check("hello world")
    assert r.similarity == 0.0
    assert r.drifted is True


def test_check_does_not_mutate_baseline():
    a = DriftAnalyzer()
    a.set_baseline(["alpha beta"])
    before = Counter(a._baseline)
    a.check("alpha beta gamma")
    assert a._baseline == before


def test_precheck_rejects_non_string_op_not_run(monkeypatch):
    a = DriftAnalyzer()
    called = {"n": 0}
    original = a._check_impl

    def wrapped(text):
        called["n"] += 1
        return original(text)

    monkeypatch.setattr(a, "_check_impl", wrapped)
    with pytest.raises(ModuleKernelError):
        a.check(12345)  # type: ignore[arg-type]
    assert called["n"] == 0


def test_postcheck_rejects_non_result(monkeypatch):
    a = DriftAnalyzer()
    monkeypatch.setattr(a, "_check_impl", lambda text: "nope")
    with pytest.raises(ModuleKernelError):
        a.check("hello")


def test_postcheck_rejects_nan_similarity(monkeypatch):
    a = DriftAnalyzer()

    def bad(text):
        return DriftResult(similarity=float("nan"), drifted=False)

    monkeypatch.setattr(a, "_check_impl", bad)
    with pytest.raises(ModuleKernelError):
        a.check("hello")


def test_postcheck_rejects_out_of_range_similarity(monkeypatch):
    a = DriftAnalyzer()
    monkeypatch.setattr(
        a, "_check_impl", lambda text: DriftResult(similarity=1.5, drifted=True)
    )
    with pytest.raises(ModuleKernelError):
        a.check("hello")


def test_postcheck_rejects_non_bool_drifted(monkeypatch):
    a = DriftAnalyzer()
    monkeypatch.setattr(
        a,
        "_check_impl",
        lambda text: DriftResult(similarity=0.5, drifted=1),  # type: ignore[arg-type]
    )
    with pytest.raises(ModuleKernelError):
        a.check("hello")


def test_ctor_rejects_invalid_threshold():
    with pytest.raises(ValueError):
        DriftAnalyzer(drift_threshold=-0.1)
    with pytest.raises(ValueError):
        DriftAnalyzer(drift_threshold=1.1)
    with pytest.raises(ValueError):
        DriftAnalyzer(drift_threshold=float("nan"))
    with pytest.raises(ValueError):
        DriftAnalyzer(drift_threshold=True)  # type: ignore[arg-type]


def test_trainer_halt_on_module_06_kernel(tmp_path, monkeypatch):
    trainer = Trainer(str(tmp_path / "a.log"))
    trainer.drift.set_baseline(["general customer support conversation about billing"])
    monkeypatch.setattr(
        trainer.drift,
        "_check_impl",
        lambda text: DriftResult(similarity=2.0, drifted=False),
    )
    with pytest.raises(ModuleKernelError) as ei:
        trainer.process("hello about billing support")
    assert "halted_by_module_06_kernel" in str(ei.value)


def test_trainer_drifted_true_does_not_halt(tmp_path):
    trainer = Trainer(str(tmp_path / "a.log"))
    trainer.drift.set_baseline(["quarterly revenue finance forecasts"])
    result = trainer.process("completely unrelated chocolate cake recipe frosting")
    assert result.drift is not None
    assert result.drift.drifted is True
    assert result.allowed is True


def test_security_block_skips_drift(tmp_path, monkeypatch):
    trainer = Trainer(str(tmp_path / "a.log"))
    called = {"n": 0}

    def spy(text):
        called["n"] += 1
        return DriftResult(similarity=1.0, drifted=False)

    monkeypatch.setattr(trainer.drift, "check", spy)
    monkeypatch.setattr(
        trainer.security,
        "scan",
        lambda text: ProbeResult(
            risk_score=0.9, triggered=["x"], block_threshold=0.5
        ),
    )
    result = trainer.process("hello")
    assert result.allowed is False
    assert called["n"] == 0
    assert result.drift is None
