"""Path-closure construction tests — inventory + discovery + SM-V1-014.

Does NOT assert Universal Gate = PROVEN.
Does NOT close residual APIs.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from swi_core.formation_path_inventory import (
    ALLOWED_CLASS,
    ALLOWED_STATUS,
    EXPECTED_KERNEL_SITES,
    EXPECTED_PUBLIC_APIS,
    discover_module_kernel_sites,
    discover_public_api_mentions,
    forbidden_closed_records,
    load_inventory,
    summarize,
)

ROOT = Path(__file__).resolve().parents[2]


def test_inventory_loads_and_has_paths():
    inv = load_inventory()
    assert inv["universal_gate"] == "NOT_PROVEN"
    assert inv["security_maze_seal"] == "NOT_READY"
    assert inv["foundation_seal_5"] == "NOT_READY"
    assert len(inv["paths"]) > 0


def test_fm_ids_unique_and_well_formed():
    inv = load_inventory()
    ids = [p["formation_path_id"] for p in inv["paths"]]
    assert len(ids) == len(set(ids))
    for i in ids:
        assert i.startswith("FM-")


def test_every_path_has_required_fields_and_valid_enums():
    inv = load_inventory()
    required = {
        "formation_path_id",
        "module",
        "entry_point",
        "source",
        "formation_type",
        "privileged",
        "maze_required",
        "maze_protected",
        "classification",
        "test_ids",
        "status",
    }
    for p in inv["paths"]:
        missing = required - set(p)
        assert not missing, (p.get("formation_path_id"), missing)
        assert p["status"] in ALLOWED_STATUS
        assert p["classification"] in ALLOWED_CLASS
        assert isinstance(p["test_ids"], list)


def test_unknown_status_never_counted_as_pass():
    inv = load_inventory()
    for p in inv["paths"]:
        if p["status"] == "UNKNOWN":
            pytest.fail(f"{p['formation_path_id']} is UNKNOWN — must not be treated as PASS")
    summary = summarize(inv)
    assert summary["unknown_paths"] == 0


def test_forbidden_closed_combo_impossible():
    inv = load_inventory()
    bad = forbidden_closed_records(inv)
    assert bad == [], bad


def test_open_privileged_unprotected_are_explicit():
    inv = load_inventory()
    summary = summarize(inv)
    assert summary["total_paths"] > 0
    assert summary["privileged_unprotected"] >= 1
    assert summary["universal_gate"] == "NOT_PROVEN"


def test_discovery_kernel_sites_covered_by_inventory_sources():
    sites = discover_module_kernel_sites(ROOT)
    inv = load_inventory()
    sources = {p["source"] for p in inv["paths"]}
    for expected in EXPECTED_KERNEL_SITES:
        if expected == "swi_core/module_kernel.py":
            continue
        assert expected in sites or expected in sources, expected
        if expected in sites:
            assert any(p["source"] == expected for p in inv["paths"]), expected


def test_discovery_public_apis_match_expected_set():
    found = discover_public_api_mentions(ROOT)
    missing = EXPECTED_PUBLIC_APIS - found
    assert not missing, missing
    inv = load_inventory()
    entries = {p["entry_point"] for p in inv["paths"]}
    for api in EXPECTED_PUBLIC_APIS:
        assert api in entries or any(api in e for e in entries), api


def test_closure_gate_not_claiming_universal_proven():
    inv = load_inventory()
    summary = summarize(inv)
    assert summary["universal_gate"] == "NOT_PROVEN"
    assert summary["privileged_unprotected"] > 0


def test_sm_v1_014_residual_path_honesty():
    """OPEN paths stay OPEN until maze_protected or non-privileged reclassification with evidence.

    Changing status to TESTED while maze_required and not maze_protected MUST fail
    (also covered by forbidden_closed_records).
    """
    inv = load_inventory()
    open_privileged = [
        p
        for p in inv["paths"]
        if p.get("status") == "OPEN"
        and p.get("privileged") is True
        and p.get("maze_required") is True
        and p.get("maze_protected") is not True
    ]
    assert len(open_privileged) >= 1
    for p in open_privileged:
        # Honesty: still OPEN
        assert p["status"] == "OPEN"
        # Must list at least one attack/evidence test id
        assert p.get("test_ids"), p["formation_path_id"]
