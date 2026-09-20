"""Formation-path baseline tests (Phase 0-5).

These tests bind FM-xxx IDs from docs/FORMATION_PATH_INVENTORY.json.
They do not upgrade path status and do not assert Universal Gate or seals.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "docs" / "FORMATION_PATH_INVENTORY.json"


def load_paths():
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    return list(data.get("formation_paths") or [])


def test_inventory_file_exists():
    assert INVENTORY.is_file(), "FORMATION_PATH_INVENTORY.json missing"


def test_inventory_schema_and_open_status():
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    assert data.get("schema_version") == "1.0"
    assert data.get("universal_gate") == "NOT_PROVEN"
    assert data.get("foundation_seal_5") == "NOT_READY"
    paths = data.get("formation_paths") or []
    assert len(paths) >= 1
    for p in paths:
        assert "id" in p and p["id"].startswith("FM-")
        assert p.get("status") in {"OPEN", "TESTED", "BLOCKED", "NOT_PROVEN"}
        # Phase 0-5 baseline keeps mirror rows OPEN; no seal upgrade
        assert p.get("status") != "SEALED"


@pytest.mark.parametrize("path_id", [p["id"] for p in load_paths()])
def test_each_fm_has_required_fields(path_id):
    paths = {p["id"]: p for p in load_paths()}
    p = paths[path_id]
    for key in ("surface", "entry_type", "privileged", "inputs", "expected_boundary", "tests", "status"):
        assert key in p, f"{path_id} missing field {key}"


def test_no_unknown_status_as_pass():
    for p in load_paths():
        assert p.get("status") != "UNKNOWN", f"{p.get('id')} must not use UNKNOWN as PASS"
