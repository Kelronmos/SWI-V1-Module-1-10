"""Tests for Module 11 Continuity Lock — working behaviour."""
from __future__ import annotations

import tempfile
from pathlib import Path

from swi_core.module11_continuity_lock import ContinuityLock


def test_update_and_pin():
    lock = ContinuityLock(max_tags=3)
    lock.update_state("project", "SWI")
    lock.update_state("mode", "strict")
    ctx = lock.get_pinned_context()
    assert "project=SWI" in ctx
    assert "mode=strict" in ctx


def test_fifo_eviction():
    lock = ContinuityLock(max_tags=2)
    lock.update_state("a", "1")
    lock.update_state("b", "2")
    lock.update_state("c", "3")
    keys = [t.key for t in lock.snapshot().tags]
    assert keys == ["b", "c"]


def test_update_existing_key_moves_to_end():
    lock = ContinuityLock(max_tags=5)
    lock.update_state("x", "1")
    lock.update_state("y", "2")
    lock.update_state("x", "3")
    tags = lock.snapshot().tags
    assert tags[-1].key == "x"
    assert tags[-1].value == "3"


def test_persistence():
    with tempfile.TemporaryDirectory() as tmp:
        path = str(Path(tmp) / "state.json")
        lock1 = ContinuityLock(max_tags=5, persist_path=path)
        lock1.update_state("session", "alpha")

        lock2 = ContinuityLock(max_tags=5, persist_path=path)
        assert "session=alpha" in lock2.get_pinned_context()
