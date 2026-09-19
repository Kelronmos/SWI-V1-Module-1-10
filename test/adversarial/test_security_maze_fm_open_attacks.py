"""FM-005 … FM-009 — attack without admission + evidence artifacts.

UNADMITTED → operation may return results → NO MAZE AUTHORITY
Artifacts stay status OPEN; integrity ≠ closure.
"""
from __future__ import annotations

from swi_core.evidence_artifact import (
    build_fm_evidence_artifact,
    verify_fm_evidence_artifact,
)
from swi_core.formation_path_inventory import load_inventory
from swi_core.module02_security_probe import SecurityProbe
from swi_core.module03_context_sync import ContextSync
from swi_core.module05_redaction_engine import RedactionEngine
from swi_core.module06_drift_analyzer import DriftAnalyzer
from swi_core.module_kernel import ModuleKernel

ATTACK_COMMIT = "13d0d433ceb1203c81871ca0c4dbebada59b1f4b"


def _row(fm_id: str) -> dict:
    inv = load_inventory()
    for p in inv["paths"]:
        if p["formation_path_id"] == fm_id:
            return p
    raise AssertionError(f"missing inventory row {fm_id}")


def _assert_open_artifact(art: dict, fm_id: str) -> None:
    assert art["fm_id"] == fm_id
    assert art["status"] == "OPEN"
    assert art["maze_authority_granted"] is False
    assert verify_fm_evidence_artifact(art)
    inv_row = _row(fm_id)
    assert art["status"] == inv_row["status"]


def test_fm_005_default_kernel_unadmitted_run_forms_output_not_maze_authority():
    row = _row("FM-005")
    assert row["status"] == "OPEN"
    assert row["maze_protected"] is False

    called = {"n": 0}

    def op(v):
        called["n"] += 1
        return {"echo": v}

    k = ModuleKernel(name="fm-005-attack")
    assert k.require_admission is False
    out = k.run("payload", op, admission=None)
    assert called["n"] == 1
    assert out == {"echo": "payload"}

    art = build_fm_evidence_artifact(
        fm_id="FM-005",
        status="OPEN",
        test_id="test_fm_005_default_kernel_unadmitted_run_forms_output_not_maze_authority",
        commit=ATTACK_COMMIT,
        decision="OBSERVED",
        maze_authority_granted=False,
        privileged_operation_performed=True,
        limitations=[
            "Default ModuleKernel runs without admission",
            "operation performed ≠ maze authority",
            "Universal Gate NOT_PROVEN",
        ],
    )
    _assert_open_artifact(art, "FM-005")


def test_fm_006_scan_without_admission_no_maze_authority():
    row = _row("FM-006")
    assert row["status"] == "OPEN"
    probe = SecurityProbe()
    assert probe.kernel.require_admission is False
    result = probe.scan("ordinary text")
    assert result is not None

    art = build_fm_evidence_artifact(
        fm_id="FM-006",
        status="OPEN",
        test_id="test_fm_006_scan_without_admission_no_maze_authority",
        commit=ATTACK_COMMIT,
        decision="OBSERVED",
        maze_authority_granted=False,
        privileged_operation_performed=True,
        limitations=["Unadmitted scan; residual OPEN"],
    )
    _assert_open_artifact(art, "FM-006")


def test_fm_007_record_turn_without_admission_no_maze_authority():
    row = _row("FM-007")
    assert row["status"] == "OPEN"
    sync = ContextSync()
    result = sync.record_turn(1)
    assert result is not None
    assert len(sync.history()) >= 1

    art = build_fm_evidence_artifact(
        fm_id="FM-007",
        status="OPEN",
        test_id="test_fm_007_record_turn_without_admission_no_maze_authority",
        commit=ATTACK_COMMIT,
        decision="OBSERVED",
        maze_authority_granted=False,
        privileged_operation_performed=True,
        limitations=["Unadmitted record_turn mutates history; residual OPEN"],
    )
    _assert_open_artifact(art, "FM-007")


def test_fm_008_redact_without_admission_no_maze_authority():
    row = _row("FM-008")
    assert row["status"] == "OPEN"
    engine = RedactionEngine()
    out = engine.redact("email test@example.com")
    assert out is not None

    art = build_fm_evidence_artifact(
        fm_id="FM-008",
        status="OPEN",
        test_id="test_fm_008_redact_without_admission_no_maze_authority",
        commit=ATTACK_COMMIT,
        decision="OBSERVED",
        maze_authority_granted=False,
        privileged_operation_performed=True,
        limitations=["Unadmitted redact; residual OPEN"],
    )
    _assert_open_artifact(art, "FM-008")


def test_fm_009_check_without_admission_no_maze_authority():
    row = _row("FM-009")
    assert row["status"] == "OPEN"
    analyzer = DriftAnalyzer()
    result = analyzer.check("sample text for drift")
    assert result is not None

    art = build_fm_evidence_artifact(
        fm_id="FM-009",
        status="OPEN",
        test_id="test_fm_009_check_without_admission_no_maze_authority",
        commit=ATTACK_COMMIT,
        decision="OBSERVED",
        maze_authority_granted=False,
        privileged_operation_performed=True,
        limitations=["Unadmitted check; residual OPEN"],
    )
    _assert_open_artifact(art, "FM-009")


def test_fm_006_to_009_inventory_still_open_after_attack_evidence():
    inv = load_inventory()
    for fm in ("FM-005", "FM-006", "FM-007", "FM-008", "FM-009"):
        row = next(p for p in inv["paths"] if p["formation_path_id"] == fm)
        assert row["status"] == "OPEN", fm
        assert row["maze_protected"] is False, fm


def test_signature_cannot_close_open_fm():
    art = build_fm_evidence_artifact(
        fm_id="FM-005",
        status="OPEN",
        test_id="test_signature_cannot_close_open_fm",
        commit=ATTACK_COMMIT,
        signature="deadbeef",
        maze_authority_granted=False,
    )
    assert art["status"] == "OPEN"
    assert _row("FM-005")["status"] == "OPEN"
    assert verify_fm_evidence_artifact(art)
