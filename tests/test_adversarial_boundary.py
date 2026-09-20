"""Adversarial boundary scaffolding for formation paths (Phase 0-5).

Parametrized over FM IDs. These tests document the minimum adversarial
contract. They do not close paths or upgrade seals.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "docs" / "FORMATION_PATH_INVENTORY.json"


def load_privileged_paths():
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    return [p for p in (data.get("formation_paths") or []) if p.get("privileged") is True]


PRIVILEGED_IDS = [p["id"] for p in load_privileged_paths()]


@pytest.mark.parametrize("path_id", PRIVILEGED_IDS)
def test_privileged_path_is_marked_open_or_tested(path_id):
    paths = {p["id"]: p for p in load_privileged_paths()}
    p = paths[path_id]
    assert p["status"] in {"OPEN", "TESTED"}, f"{path_id} unexpected status {p['status']}"


@pytest.mark.parametrize("path_id", PRIVILEGED_IDS)
def test_privileged_path_has_expected_boundary_text(path_id):
    paths = {p["id"]: p for p in load_privileged_paths()}
    p = paths[path_id]
    assert isinstance(p.get("expected_boundary"), str) and len(p["expected_boundary"]) > 0


@pytest.mark.parametrize("path_id", PRIVILEGED_IDS)
def test_privileged_path_lists_tests_field(path_id):
    """Construction map: tests[] may be empty; must be present."""
    paths = {p["id"]: p for p in load_privileged_paths()}
    p = paths[path_id]
    assert "tests" in p and isinstance(p["tests"], list)


def test_adversarial_contract_documented():
    """Minimum adversarial contract for future expansion (not yet executable attacks)."""
    required_cases = [
        "valid input",
        "missing required input",
        "malformed input",
        "unexpected input",
        "boundary violation",
        "tampered value",
        "unauthorised transition",
        "duplicate/replay attempt",
    ]
    # This test only documents the contract; it does not execute attacks.
    assert len(required_cases) == 8
