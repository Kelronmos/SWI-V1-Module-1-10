"""Steps 126–150 — cryptographic evidence artifact boundary.

Integrity under canonicalization_v0 only. No parallel crypto. No path closure.
"""
from __future__ import annotations

from swi_core.canonical import CANONICALIZATION_VERSION, canonical_hash
from swi_core.evidence_artifact import (
    CONTRACT_ID,
    REQUIRED_ARTIFACT_KEYS,
    build_fm_evidence_artifact,
    load_serialized_artifact,
    mutate_detectable,
    serialize_artifact,
    verify_fm_evidence_artifact,
)


def _base(**kwargs):
    defaults = dict(
        fm_id="FM-005",
        status="OPEN",
        test_id="test_fm_005_default_kernel_unadmitted_run_forms_output_not_maze_authority",
        commit="13d0d433ceb1203c81871ca0c4dbebada59b1f4b",
        decision="OBSERVED",
        input_hash="deadbeef" * 8,
        previous_evidence_hash=None,
        maze_authority_granted=False,
        privileged_operation_performed=True,
        limitations=["Residual OPEN", "Universal Gate NOT_PROVEN"],
        signature=None,
    )
    defaults.update(kwargs)
    return build_fm_evidence_artifact(**defaults)


def test_contract_is_canonicalization_v0():
    assert CONTRACT_ID == CANONICALIZATION_VERSION == "canonicalization_v0"


def test_required_fields_present():
    art = _base()
    assert REQUIRED_ARTIFACT_KEYS <= set(art.keys())


def test_build_artifact_signature_null_is_legitimate():
    art = _base()
    assert art["signature"] is None
    assert art["status"] == "OPEN"
    assert art["maze_authority_granted"] is False
    assert verify_fm_evidence_artifact(art)


def test_determinism_identical_builds():
    a = _base()
    b = _base()
    assert a["evidence_hash"] == b["evidence_hash"]


def test_evidence_hash_matches_canonical_material():
    art = _base()
    material = {k: v for k, v in art.items() if k not in ("evidence_hash", "signature")}
    assert art["evidence_hash"] == canonical_hash(material)


def test_missing_evidence_hash_fails_verify():
    art = _base()
    bad = dict(art)
    bad["evidence_hash"] = ""
    assert verify_fm_evidence_artifact(bad) is False
    del bad["evidence_hash"]
    assert verify_fm_evidence_artifact(bad) is False


def test_unknown_canonicalization_contract_fails_verify():
    art = _base()
    bad = dict(art)
    bad["canonicalization_contract"] = "future_unknown_v99"
    # hash still old — material includes contract field so also mismatch; either way False
    assert verify_fm_evidence_artifact(bad) is False


def test_status_mutation_open_to_tested_fails_verify():
    art = _base(status="OPEN")
    assert mutate_detectable(art, "status", "TESTED") is True


def test_fm_id_mutation_fails_verify():
    art = _base(fm_id="FM-005")
    assert mutate_detectable(art, "fm_id", "FM-006") is True


def test_commit_mutation_fails_verify():
    art = _base()
    assert mutate_detectable(art, "commit", "0" * 40) is True


def test_test_id_mutation_fails_verify():
    art = _base()
    assert mutate_detectable(art, "test_id", "other_test") is True


def test_maze_authority_mutation_fails_verify():
    art = _base(maze_authority_granted=False)
    assert mutate_detectable(art, "maze_authority_granted", True) is True


def test_privileged_operation_mutation_fails_verify():
    art = _base(privileged_operation_performed=False)
    assert mutate_detectable(art, "privileged_operation_performed", True) is True


def test_fake_signature_does_not_close_path():
    art = _base(signature="deadbeef")
    assert art["status"] == "OPEN"
    assert art["maze_authority_granted"] is False
    assert verify_fm_evidence_artifact(art)


def test_signature_change_keeps_integrity_hash_valid():
    """signature excluded from material — changing it alone leaves evidence_hash valid."""
    art = _base(signature=None)
    altered = dict(art)
    altered["signature"] = "aabbccdd"
    assert verify_fm_evidence_artifact(altered) is True
    assert altered["status"] == "OPEN"


def test_json_roundtrip_verify():
    art = _base()
    blob = serialize_artifact(art)
    reloaded = load_serialized_artifact(blob)
    assert verify_fm_evidence_artifact(reloaded) is True
    reloaded["status"] = "TESTED"
    assert verify_fm_evidence_artifact(reloaded) is False


def test_verify_does_not_imply_authority_or_closure():
    art = _base(
        status="OPEN",
        maze_authority_granted=False,
        privileged_operation_performed=True,
    )
    assert verify_fm_evidence_artifact(art) is True
    assert art["status"] == "OPEN"
    assert art["maze_authority_granted"] is False
