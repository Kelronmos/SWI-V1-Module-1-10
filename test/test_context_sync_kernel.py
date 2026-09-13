"""Module 03 kernel contract — type/shape only; flags are not halt conditions."""
import datetime as dt

import pytest

from swi_core.module00_trainer import Trainer
from swi_core.module03_context_sync import ContextSync
from swi_core.module_kernel import ModuleKernelError


def test_first_turn_not_stale_gap_zero():
    sync = ContextSync(staleness_seconds=60)
    t0 = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
    r = sync.record_turn(1, t0)
    assert r.stale is False
    assert r.out_of_order is False
    assert r.gap_seconds == 0.0


def test_stale_only_when_gap_strictly_greater():
    t0 = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
    sync = ContextSync(staleness_seconds=60)
    sync.record_turn(1, t0)
    at_limit = sync.record_turn(2, t0 + dt.timedelta(seconds=60))
    assert at_limit.stale is False
    assert at_limit.gap_seconds == 60.0
    sync2 = ContextSync(staleness_seconds=60)
    sync2.record_turn(1, t0)
    over2 = sync2.record_turn(2, t0 + dt.timedelta(seconds=61))
    assert over2.stale is True
    assert over2.gap_seconds == 61.0


def test_out_of_order_flag_does_not_raise():
    sync = ContextSync()
    t0 = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
    sync.record_turn(1, t0)
    r = sync.record_turn(2, t0 - dt.timedelta(seconds=5))
    assert r.out_of_order is True
    assert len(sync.history()) == 2


def test_precheck_rejects_non_datetime_timestamp():
    sync = ContextSync()
    with pytest.raises(ModuleKernelError):
        sync.record_turn(1, timestamp="2026-01-01")  # type: ignore[arg-type]


def test_precheck_failure_does_not_append():
    sync = ContextSync()
    t0 = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
    sync.record_turn(1, t0)
    with pytest.raises(ModuleKernelError):
        sync.record_turn(2, timestamp=12345)  # type: ignore[arg-type]
    assert len(sync.history()) == 1


def test_postcheck_rejects_non_sync_result(monkeypatch):
    sync = ContextSync()

    def bad(value):
        return "not-a-sync-result"

    monkeypatch.setattr(sync, "_record_turn_impl", bad)
    with pytest.raises(ModuleKernelError):
        sync.record_turn(1, dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc))


def test_ctor_rejects_negative_staleness():
    with pytest.raises(ValueError):
        ContextSync(staleness_seconds=-1)


def test_ctor_rejects_bool_staleness():
    with pytest.raises(ValueError):
        ContextSync(staleness_seconds=True)  # type: ignore[arg-type]


def test_trainer_halt_on_module_03_kernel(tmp_path, monkeypatch):
    log = tmp_path / "audit.jsonl"
    trainer = Trainer(str(log))
    called = {"n": 0}
    original = trainer.security.scan

    def wrapped(text):
        called["n"] += 1
        return original(text)

    monkeypatch.setattr(trainer.security, "scan", wrapped)
    with pytest.raises(ModuleKernelError) as ei:
        trainer.process("hello", timestamp="not-a-datetime")  # type: ignore[arg-type]
    assert "halted_by_module_03_kernel" in str(ei.value)
    assert called["n"] == 0


def test_trainer_stale_does_not_halt(tmp_path):
    log = tmp_path / "audit.jsonl"
    cfg = tmp_path / "cfg.yaml"
    cfg.write_text("context_sync:\n  staleness_seconds: 10\n")
    trainer = Trainer(str(log), config_path=str(cfg))
    t0 = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
    trainer.process("hello", timestamp=t0)
    result = trainer.process(
        "hello again", timestamp=t0 + dt.timedelta(seconds=100)
    )
    assert result.sync.stale is True
    assert result.allowed is True
