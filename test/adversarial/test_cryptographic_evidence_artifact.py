"""Cryptographic evidence artifact — canonicalization_v0 only.

Does not claim authority, truth, CRTG, or path closure.
"""
from __future__ import annotations

from swi_core.canonical import CANONICALIZATION_VERSION, canonical_hash
from swi_core.evidence_artifact import (
    CONTRACT_ID,
    build_fm_evidence_artifact,
    mutate_detectable,
    verify_fm_evidence_artifact,
)


def test_contract_is_canonicalization_v0():
    assert CONTRACT_ID == CANONICALIZATION_VERSION == "canonicalization_v0"


def test_build_artifact_signature_null_is_legitimate():
    art = build_fm_evidence_artifact(
        fm_id="FM-005",
        status="OPEN",
        test_id="test_fm_005",
        commit="c8a7e120b27311e0597aaa0d4b76bfc8bd9b3ef8",
        decision="OBSERVED",
        maze_authority_granted=False,
        privileged_operation_performed=True,  # residual may run op
        signature=None,
    )
    assert art["signature"] is None
    assert art["canonicalization_contract"] == "canonicalization_v0"
    assert art["status"] == "OPEN"
    assert art["maze_authority_granted"] is False
    assert verify_fm_evidence_artifact(art)


def test_evidence_hash_stable_under_key_rebuild():
    art = build_fm_evidence_artifact(
        fm_id="FM-006",
        status="OPEN",
        test_id="t",
        commit="abcdef0",
    )
    assert verify_fm_evidence_artifact(art)
    # material hash excludes evidence_hash
    material = {k: v for k, v in art.items() if k not in ("evidence_hash", "signature")}
    assert art["evidence_hash"] == canonical_hash(material)


def test_mutation_of_status_invalidates_hash():
    art = build_fm_evidence_artifact(
        fm_id="FM-007",
        status="OPEN",
        test_id="t",
        commit="abcdef0",
    )
    assert mutate_detectable(art, "status", "TESTED") is True


def test_mutation_of_fm_id_invalidates_hash():
    art = build_fm_evidence_artifact(
        fm_id="FM-008",
        status="OPEN",
        test_id="t",
        commit="abcdef0",
    )
    assert mutate_detectable(art, "fm_id", "FM-999") is True


def test_signature_does_not_close_path():
    """Valid-looking signature field must not imply closure."""
    art = build_fm_evidence_artifact(
        fm_id="FM-009",
        status="OPEN",
        test_id="t",
        commit="abcdef0",
        signature="deadbeef",  # not a real sig — still OPEN
    )
    assert art["status"] == "OPEN"
    assert art["maze_authority_granted"] is False
    assert verify_fm_evidence_artifact(art)


def test_fm_open_attack_can_emit_artifact():
    art = build_fm_evidence_artifact(
        fm_id="FM-005",
        status="OPEN",
        test_id="test_fm_005_default_kernel_unadmitted_run_forms_output_not_maze_authority",
        commit="c8a7e120b27311e0597aaa0d4b76bfc8bd9b3ef8",
        decision="OBSERVED",
        maze_authority_granted=False,
        privileged_operation_performed=True,
        limitations=[
            "Default ModuleKernel runs without admission",
            "Not maze authority",
            "Universal Gate NOT_PROVEN",
        ],
    )
    assert verify_fm_evidence_artifact(art)
    assert art["status"] == "OPEN"
