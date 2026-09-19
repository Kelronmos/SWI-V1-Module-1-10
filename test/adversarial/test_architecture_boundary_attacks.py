"""Architecture-boundary attack suite.

These tests make anti-overclaim rules executable.

They do NOT prove Module 10 or any other proposed component is admitted.
They prove that common promotion / laundering attacks are rejected.

Governing chain that must never be short-circuited:

  DOCUMENTATION → CLAIM → EVIDENCE → VERIFY → ADMISSION → SEAL

Never:
  README says SEALED → SEALED
  test passes → SEALED
  hash exists → AUTHORITY
  module number exists → MODULE ADMITTED
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


# ---------------------------------------------------------------------------
# Attack 2 — Documentation injection
# ---------------------------------------------------------------------------

def test_attack_02_documentation_cannot_seal():
    claim = {
        "module": "10",
        "status": "SEALED",
        "source": "documentation",
    }
    # Even if a seal record existed, documentation source is still insufficient
    # for the primary rejection path when no proper evidence is bound.
    result = evaluate_claim(claim, seal_records={})
    assert result["ok"] is False
    assert result["reason"] in (
        "DOCUMENTATION_IS_NOT_ADMISSION",
        "SEAL_WITHOUT_SEAL_RECORD",
    )


def test_attack_02_readme_source_rejected_for_sealed():
    claim = {
        "module": "M05",
        "status": "SEALED",
        "source": "readme",
    }
    result = evaluate_claim(claim, seal_records={})
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Attack 3 — Old CI substitution
# ---------------------------------------------------------------------------

def test_attack_03_old_ci_does_not_seal_new_commit():
    claim = {
        "module": "10",
        "status": "SEALED",
        "seal_commit": "aaaa",
        "ci_commit": "aaaa",  # old green run
    }
    result = evaluate_claim(
        claim,
        seal_records={"10": {"commit": "aaaa"}},
        current_commit="bbbb",  # tip has moved
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
            {"hash": "c" * 64, "synthetic": True},
        ],
    }
    result = evaluate_claim(claim)
    assert result["ok"] is False
    assert result["reason"] == "SYNTHETIC_UPSTREAM_RECEIPT"


def test_attack_05_receipt_missing_provenance_rejected():
    claim = {
        "module": "10",
        "upstream_receipts": [
            {"hash": "a" * 64},  # no produced_by_module, no evidence_ref
        ],
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
# Attack 7 — Seal laundering (domain / module rebinding)
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
        seal_records={"10": {"commit": "tip"}},
        current_commit="tip",
    )
    assert result["ok"] is False
    assert result["reason"] == "SEAL_DOMAIN_MISMATCH"


# ---------------------------------------------------------------------------
# Attack 8 — Authority laundering (verified → authorized → executable)
# ---------------------------------------------------------------------------

def test_attack_08_verified_does_not_imply_executable():
    claim = {
        "module": "10",
        "verified": True,
        "authorized": True,
        "executable": True,
        # no admission_artifact, no execution_authority_record
    }
    result = evaluate_claim(claim)
    assert result["ok"] is False
    assert result["reason"] == "AUTHORITY_LAUNDERING"


def test_attack_08_verified_alone_is_not_authority():
    claim = {
        "module": "10",
        "verified": True,
        "executable": True,
    }
    result = evaluate_claim(claim)
    assert result["ok"] is False
    assert result["reason"] == "AUTHORITY_LAUNDERING"


# ---------------------------------------------------------------------------
# Attack 9 — Blocked-path bypass
# ---------------------------------------------------------------------------

def test_attack_09_blocked_path_cannot_execute():
    claim = {
        "module": "10",
        "status": "BLOCKED",
        "force_execute": True,
    }
    result = evaluate_claim(claim)
    assert result["ok"] is False
    assert result["reason"] == "BLOCKED_PATH_BYPASS"


def test_attack_09_proposed_not_admitted_cannot_execute():
    claim = {
        "module": "10",
        "status": "PROPOSED",
        "executable": True,
    }
    result = evaluate_claim(claim)
    assert result["ok"] is False
    assert result["reason"] == "BLOCKED_PATH_BYPASS"


def test_attack_09_module_10_admission_status_is_blocked():
    """Living check against the governance decision record."""
    # Module 10 BoundaryExporter remains PROPOSED / NOT ADMITTED
    claim = {
        "module": "10",
        "status": "NOT ADMITTED",
        "executable": True,
    }
    result = evaluate_claim(claim)
    assert result["ok"] is False
    assert result["reason"] == "BLOCKED_PATH_BYPASS"


# ---------------------------------------------------------------------------
# Attack 10 — Seal mutation (implementation changed after seal)
# ---------------------------------------------------------------------------

def test_attack_10_old_seal_does_not_cover_new_tip():
    claim = {
        "module": "M05",
        "status": "SEALED",
        "seal_commit": "oldsha",
    }
    result = evaluate_claim(
        claim,
        seal_records={"M05": {"commit": "oldsha"}},
        current_commit="newsha",
    )
    assert result["ok"] is False
    assert result["reason"] in ("SEAL_COMMIT_MISMATCH", "SEAL_MUTATION")


def test_is_module_sealed_requires_record_and_tip():
    result = is_module_sealed(
        "10",
        seal_records={},
        current_commit="abc",
        documentation_says_sealed=True,
    )
    assert result["ok"] is False
