"""Evidence artifact must not independently close FM inventory rows."""
from __future__ import annotations

from swi_core.evidence_artifact import build_fm_evidence_artifact, verify_fm_evidence_artifact
from swi_core.formation_path_inventory import load_inventory


def test_residual_artifacts_match_inventory_open_status():
    inv = load_inventory()
    rows = {p["formation_path_id"]: p for p in inv["paths"]}
    for fm in ("FM-005", "FM-006", "FM-007", "FM-008", "FM-009"):
        assert rows[fm]["status"] == "OPEN"
        art = build_fm_evidence_artifact(
            fm_id=fm,
            status="OPEN",
            test_id=f"bind_{fm}",
            commit="13d0d433ceb1203c81871ca0c4dbebada59b1f4b",
            maze_authority_granted=False,
            privileged_operation_performed=True,
        )
        assert art["status"] == rows[fm]["status"]
        assert verify_fm_evidence_artifact(art)


def test_artifact_cannot_claim_tested_while_inventory_open():
    """Even a well-formed artifact with status TESTED does not update inventory."""
    inv = load_inventory()
    row = next(p for p in inv["paths"] if p["formation_path_id"] == "FM-005")
    assert row["status"] == "OPEN"
    art = build_fm_evidence_artifact(
        fm_id="FM-005",
        status="TESTED",  # attacker paperwork
        test_id="forged_closure",
        commit="13d0d433ceb1203c81871ca0c4dbebada59b1f4b",
    )
    assert verify_fm_evidence_artifact(art)  # integrity can hold
    # Inventory remains authority for path-closure status
    inv2 = load_inventory()
    row2 = next(p for p in inv2["paths"] if p["formation_path_id"] == "FM-005")
    assert row2["status"] == "OPEN"
