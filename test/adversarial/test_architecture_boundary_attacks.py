"""Architecture-boundary attack suite + Phase 7 input hardening.

These tests make anti-overclaim rules executable.
They do NOT prove Module 10 or any other proposed component is admitted.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from swi_core.admission_boundary import evaluate_claim, is_module_sealed


# ---------------------------------------------------------------------------
# Attack 1 — Fake seal
# ---------------------------------------------------------------------------

def test_attack_01_fake_seal_without_record():
    claim = {"module": "10", "status": "SEALED"}
    result = evaluate_claim(claim, seal_records={})
    assert result["ok"] is False
    assert result["reason"] == "SEAL_WITHOUT_SEAL_RECORD"


def test_attack_01_fake_seal_missing_module():
    claim = {"status": "SEALED"}
    result = evaluate_claim(claim, seal_records={})
    assert result["ok"] is False
    assert result["reason"] == "SEAL_CLAIM_MISSING_MODULE"


def test_attack_01_empty_seal_record_rejected():
    claim = {"module": "10", "status": "SEALED"}
    result = evaluate_claim(claim, seal_records={"10": {}})
    assert result["ok"] is False
    assert result["reason"] in ("SEAL_WITHOUT_SEAL_RECORD", "SEAL_RECORD_EMPTY")


# ---------------------------------------------------------------------------
# Attack 2 — Documentation injection
# ---------------------------------------------------------------------------

def test_attack_02_documentation_cannot_seal():
    claim = {"module": "10", "status": "SEALED", "source": "documentation"}
    result = evaluate_claim(claim, seal_records={})
    assert result["ok"] is False
    assert result["reason"] in (
        "DOCUMENTATION_IS_NOT_ADMISSION",
        "SEAL_WITHOUT_SEAL_RECORD",
    )


def test_attack_02_readme_source_rejected_for_sealed():
    claim = {"module": "M05", "status": "SEALED", "source": "readme"}
    result = evaluate_claim(claim, seal_records={})
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Attack 3 — Old CI substitution
# ---------------------------------------------------------------------------

def test_attack_03_old_ci_does_not_seal_new_commit():
    claim = {
        "module": "10",
        "status": "SEALED",
        "seal_commit": "aaaaaaa",
        "ci_commit": "aaaaaaa",
    }
    result = evaluate_claim(
        claim,
        seal_records={"10": {"commit": "aaaaaaa"}},
        current_commit="bbbbbbb",
    )
    assert result["ok"] is False
    assert result["reason"] in (
        "OLD_CI_DOES_NOT_SEAL_NEW_COMMIT",
        "SEAL_COMMIT_MISMATCH",
        "SEAL_MUTATION",
    )


# ---------------------------------------------------------------------------
# Attack 4 — Module-number injection
# ---------------------------------------------------------------------------

def test_attack_04_module_number_is_construction_reference():
    claim = {"module": "10", "implementation": "anything"}
    result = evaluate_claim(claim)
    assert result["ok"] is True
    assert result.get("execution_authority") is False
    assert result.get("architectural_admission") is False
    assert result.get("seal") is False
    assert "CONSTRUCTION_REFERENCE" in result.get("note", "")


# ---------------------------------------------------------------------------
# Attack 5 — Fake upstream receipt chain
# ---------------------------------------------------------------------------

def test_attack_05_synthetic_upstream_receipts_rejected():
    claim = {
        "module": "10",
        "status": "IMPLEMENTED",
        "upstream_receipts": [
            {"hash": "a" * 64, "synthetic": True},
            {"hash": "b" * 64, "synthetic": True},
        ],
    }
    result = evaluate_claim(claim)
    assert result["ok"] is False
    assert result["reason"] == "SYNTHETIC_UPSTREAM_RECEIPT"


def test_attack_05_receipt_missing_provenance_rejected():
    claim = {
        "module": "10",
        "upstream_receipts": [{"hash": "a" * 64}],
    }
    result = evaluate_claim(claim)
    assert result["ok"] is False
    assert result["reason"] == "UPSTREAM_RECEIPT_MISSING_PROVENANCE"


# ---------------------------------------------------------------------------
# Attack 6 — Hash laundering
# ---------------------------------------------------------------------------

def test_attack_06_hash_laundering_rejected():
    claim = {
        "module": "10",
        "payload_modified": True,
        "hash_recalculated": True,
        "evidence_sha256": "d" * 64,
    }
    result = evaluate_claim(claim)
    assert result["ok"] is False
    assert result["reason"] == "HASH_LAUNDERING"


# ---------------------------------------------------------------------------
# Attack 7 — Seal laundering
# ---------------------------------------------------------------------------

def test_attack_07_seal_laundering_rejected():
    claim = {
        "module": "10",
        "status": "SEALED",
        "original_seal_module": "03",
        "rebound_from_module": "10",
    }
    result = evaluate_claim(
        claim,
        seal_records={"10": {"commit": "abcdef0"}},
        current_commit="abcdef0",
    )
    assert result["ok"] is False
    assert result["reason"] == "SEAL_DOMAIN_MISMATCH"


# ---------------------------------------------------------------------------
# Attack 8 — Authority laundering
# ---------------------------------------------------------------------------

def test_attack_08_verified_does_not_imply_executable():
    claim = {
        "module": "10",
        "verified": True,
        "authorized": True,
        "executable": True,
    }
    result = evaluate_claim(claim)
    assert result["ok"] is False
    assert result["reason"] == "AUTHORITY_LAUNDERING"


def test_attack_08_verified_alone_is_not_authority():
    claim = {"module": "10", "verified": True, "executable": True}
    result = evaluate_claim(claim)
    assert result["ok"] is False
    assert result["reason"] == "AUTHORITY_LAUNDERING"


# ---------------------------------------------------------------------------
# Attack 9 — Blocked-path bypass
# ---------------------------------------------------------------------------

def test_attack_09_blocked_path_cannot_execute():
    claim = {"module": "10", "status": "BLOCKED", "force_execute": True}
    result = evaluate_claim(claim)
    assert result["ok"] is False
    assert result["reason"] == "BLOCKED_PATH_BYPASS"
    assert "required_evidence" in result


def test_attack_09_proposed_not_admitted_cannot_execute():
    claim = {"module": "10", "status": "PROPOSED", "executable": True}
    result = evaluate_claim(claim)
    assert result["ok"] is False
    assert result["reason"] == "BLOCKED_PATH_BYPASS"


def test_attack_09_module_10_admission_status_is_blocked():
    claim = {"module": "10", "status": "NOT ADMITTED", "executable": True}
    result = evaluate_claim(claim)
    assert result["ok"] is False
    assert result["reason"] == "BLOCKED_PATH_BYPASS"


# ---------------------------------------------------------------------------
# Attack 10 — Seal mutation
# ---------------------------------------------------------------------------

def test_attack_10_old_seal_does_not_cover_new_tip():
    # Valid 7+ character hex commit identifiers (required by COMMIT_NOT_HEX rule)
    claim = {"module": "M05", "status": "SEALED", "seal_commit": "aaaaaaa"}
    result = evaluate_claim(
        claim,
        seal_records={"M05": {"commit": "aaaaaaa"}},
        current_commit="bbbbbbb",
    )
    assert result["ok"] is False
    assert result["reason"] in ("SEAL_COMMIT_MISMATCH", "SEAL_MUTATION")


def test_is_module_sealed_requires_record_and_tip():
    result = is_module_sealed(
        "10",
        seal_records={},
        current_commit="abc1234",
        documentation_says_sealed=True,
    )
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Phase 7 — Input / type / encoding attacks (fail closed)
# ---------------------------------------------------------------------------

def test_phase7_claim_not_a_mapping():
    result = evaluate_claim("not-a-dict")  # type: ignore[arg-type]
    assert result["ok"] is False
    assert result["reason"] == "CLAIM_NOT_A_MAPPING"


def test_phase7_module_id_not_string():
    result = evaluate_claim({"module": 10, "status": "IMPLEMENTED"})
    assert result["ok"] is False
    assert result["reason"] == "MODULE_ID_NOT_A_STRING"


def test_phase7_module_id_empty():
    result = evaluate_claim({"module": "", "status": "IMPLEMENTED"})
    assert result["ok"] is False
    assert result["reason"] == "MODULE_ID_EMPTY"


def test_phase7_module_id_whitespace():
    result = evaluate_claim({"module": " 10 ", "status": "IMPLEMENTED"})
    assert result["ok"] is False
    assert result["reason"] == "MODULE_ID_HAS_SURROUNDING_WHITESPACE"


def test_phase7_status_not_string():
    result = evaluate_claim({"module": "10", "status": True})
    assert result["ok"] is False
    assert result["reason"] == "STATUS_NOT_A_STRING"


def test_phase7_unknown_status_token():
    result = evaluate_claim({"module": "10", "status": "SUPER_SEALED"})
    assert result["ok"] is False
    assert result["reason"] == "UNKNOWN_STATUS_TOKEN"


def test_phase7_boolean_string_confusion_verified():
    result = evaluate_claim({"module": "10", "verified": "true", "executable": True})
    assert result["ok"] is False
    assert result["reason"] == "BOOLEAN_STRING_CONFUSION"


def test_phase7_commit_not_hex():
    result = evaluate_claim(
        {"module": "10", "status": "SEALED", "seal_commit": "not-hex!!!"},
        seal_records={"10": {"commit": "abcdef0"}},
        current_commit="abcdef0",
    )
    assert result["ok"] is False
    assert result["reason"] == "COMMIT_NOT_HEX"


def test_phase7_commit_empty():
    result = evaluate_claim(
        {"module": "10", "seal_commit": ""},
    )
    assert result["ok"] is False
    assert result["reason"] == "COMMIT_EMPTY"


def test_phase7_current_commit_malformed():
    result = evaluate_claim(
        {"module": "10", "status": "IMPLEMENTED"},
        current_commit="zzz",
    )
    assert result["ok"] is False
    assert result["reason"] == "COMMIT_NOT_HEX"


def test_phase7_case_variant_status_sealed_still_requires_record():
    # "sealed" lower-case must normalize and still require seal record
    result = evaluate_claim({"module": "10", "status": "sealed"}, seal_records={})
    assert result["ok"] is False
    assert result["reason"] == "SEAL_WITHOUT_SEAL_RECORD"


def test_phase7_upstream_not_sequence():
    result = evaluate_claim(
        {"module": "10", "upstream_receipts": {"hash": "a" * 64}}
    )
    assert result["ok"] is False
    assert result["reason"] == "UPSTREAM_RECEIPTS_NOT_A_SEQUENCE"
