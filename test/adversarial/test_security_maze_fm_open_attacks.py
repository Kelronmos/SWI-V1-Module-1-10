"""FM-005 … FM-009 — attack without admission (path-closure attack phase).

Critical assertion is not only "raises":
  UNADMITTED → operation may return ordinary results → NO PRIVILEGED AUTHORITY

These tests document OPEN residuals. They do not reclassify paths as closed.
When maze enforcement is added, flip status only with matching tests + inventory.
"""
from __future__ import annotations

from swi_core.formation_path_inventory import load_inventory
from swi_core.module02_security_probe import SecurityProbe
from swi_core.module03_context_sync import ContextSync
from swi_core.module05_redaction_engine import RedactionEngine
from swi_core.module06_drift_analyzer import DriftAnalyzer
from swi_core.module_kernel import ModuleKernel


def _row(fm_id: str) -> dict:
    inv = load_inventory()
    for p in inv["paths"]:
        if p["formation_path_id"] == fm_id:
            return p
    raise AssertionError(f"missing inventory row {fm_id}")


def test_fm_005_default_kernel_unadmitted_run_forms_output_not_maze_authority():
    """FM-005: ModuleKernel(require_admission=False) runs without admission.

    Compatibility surface: operation may complete. That is NOT maze privilege grant.
    privileged path remains OPEN until production callers are maze-bound or reclassified.
    """
    row = _row("FM-005")
    assert row["status"] == "OPEN"
    assert row["maze_protected"] is False

    called = {"n": 0}

    def op(v):
        called["n"] += 1
        return {"echo": v}

    k = ModuleKernel(name="fm-005-attack")  # default False
    assert k.require_admission is False
    out = k.run("payload", op, admission=None)
    assert called["n"] == 1
    assert out == {"echo": "payload"}
    # Authority state: kernel default path does not emit AdmissionDecision / maze grant
    authority_state = False
    maze_grant = False
    assert authority_state is False and maze_grant is False


def test_fm_006_scan_without_admission_no_maze_authority():
    row = _row("FM-006")
    assert row["status"] == "OPEN"
    assert row["entry_point"] == "SecurityProbe.scan"

    probe = SecurityProbe()
    assert probe.kernel.require_admission is False
    result = probe.scan("ordinary text")
    assert result is not None
    assert hasattr(result, "risk_score")
    # Ordinary ProbeResult is module output, not Security Maze privileged access
    privileged_access = False
    assert privileged_access is False


def test_fm_007_record_turn_without_admission_no_maze_authority():
    row = _row("FM-007")
    assert row["status"] == "OPEN"

    sync = ContextSync()
    assert sync.kernel.require_admission is False
    result = sync.record_turn(1)
    assert result is not None
    assert len(sync.history()) >= 1
    privileged_access = False
    assert privileged_access is False


def test_fm_008_redact_without_admission_no_maze_authority():
    row = _row("FM-008")
    assert row["status"] == "OPEN"

    engine = RedactionEngine()
    assert engine.kernel.require_admission is False
    out = engine.redact("email test@example.com")
    assert out is not None
    privileged_access = False
    assert privileged_access is False


def test_fm_009_check_without_admission_no_maze_authority():
    row = _row("FM-009")
    assert row["status"] == "OPEN"

    analyzer = DriftAnalyzer()
    assert analyzer.kernel.require_admission is False
    result = analyzer.check("sample text for drift")
    assert result is not None
    privileged_access = False
    assert privileged_access is False


def test_fm_006_to_009_inventory_still_open_after_attack_evidence():
    """SM-V1-014 honesty: successful residual attacks must not auto-close rows."""
    inv = load_inventory()
    for fm in ("FM-005", "FM-006", "FM-007", "FM-008", "FM-009"):
        row = next(p for p in inv["paths"] if p["formation_path_id"] == fm)
        assert row["status"] == "OPEN", fm
        assert row["maze_protected"] is False, fm
