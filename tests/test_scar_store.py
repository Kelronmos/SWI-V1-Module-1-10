"""Tests for Scar model and ScarStore — working behaviour, not mocks."""
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from swi_core.scar import Scar, ScarClass, ScarStatus, ScarStore, ScarStoreError


def test_create_and_hash():
    store = ScarStore()
    scar = store.create(
        title="Prompt injection attempt",
        description="User tried to override system instructions",
        scar_class=ScarClass.SOVEREIGN,
        failure_signature="ignore previous instructions",
        recommended_response="HALT and log",
    )
    assert scar.scar_id
    assert scar.content_hash == scar.compute_content_hash()
    assert scar.is_sovereign()
    assert scar.priority_score >= 2.0
    assert store.count() == 1


def test_sovereign_priority_over_functional():
    store = ScarStore()
    store.create(title="func", description="d", scar_class=ScarClass.FUNCTIONAL)
    store.create(title="sov", description="d", scar_class=ScarClass.SOVEREIGN)
    active = store.list_active()
    assert active[0].scar_class == ScarClass.SOVEREIGN


def test_integrity_root_changes_on_mutation():
    store = ScarStore()
    s = store.create(title="t", description="d")
    root1 = store.integrity_root()
    s.title = "mutated"
    # content_hash not recomputed → integrity check fails
    result = store.validate_integrity()
    assert result["valid"] is False
    assert s.scar_id in result["broken_scar_ids"]


def test_prune_protection():
    store = ScarStore()
    s = store.create(title="locked", description="d", protection_level=3)
    with pytest.raises(ScarStoreError):
        store.prune(s.scar_id, reason="test", authorized_by="random")
    pruned = store.prune(s.scar_id, reason="architect decision", authorized_by="architect")
    assert pruned.status == ScarStatus.PRUNED


def test_sqlite_persistence():
    with tempfile.TemporaryDirectory() as tmp:
        path = str(Path(tmp) / "scars.db")
        store1 = ScarStore(db_path=path)
        s = store1.create(title="persist me", description="across restart")
        scar_id = s.scar_id
        root = store1.integrity_root()

        store2 = ScarStore(db_path=path)
        loaded = store2.get(scar_id)
        assert loaded is not None
        assert loaded.title == "persist me"
        assert store2.integrity_root() == root
