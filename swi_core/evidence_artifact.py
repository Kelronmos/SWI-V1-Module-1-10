"""Bounded FM / maze evidence artifact builder.

Uses only canonicalization_v0 (swi_core.canonical).
Optional Ed25519 is explicit and never required for a valid artifact.

HASH ≠ AUTHORITY ≠ TRUTH
SIGNATURE ≠ TRUTH ≠ COMPLIANCE
signature: null is a legitimate artifact.
"""
from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Optional

from .canonical import CANONICALIZATION_VERSION, canonical_hash

CONTRACT_ID = CANONICALIZATION_VERSION  # canonicalization_v0


def _material_for_hash(record: Mapping[str, Any]) -> dict[str, Any]:
    """Fields included in integrity digest — excludes evidence_hash and signature."""
    skip = {"evidence_hash", "signature"}
    return {k: record[k] for k in sorted(record.keys()) if k not in skip}


def build_fm_evidence_artifact(
    *,
    fm_id: str,
    status: str,
    test_id: str,
    commit: Optional[str] = None,
    decision: str = "OBSERVED",
    input_hash: Optional[str] = None,
    previous_evidence_hash: Optional[str] = None,
    maze_authority_granted: bool = False,
    privileged_operation_performed: bool = False,
    limitations: Optional[list[str]] = None,
    signature: Optional[str] = None,
    extra: Optional[Mapping[str, Any]] = None,
) -> dict[str, Any]:
    """Build a machine-readable FM evidence record and attach evidence_hash.

    Does not grant authority. Does not close formation paths.
    """
    record: dict[str, Any] = {
        "fm_id": fm_id,
        "status": status,
        "decision": decision,
        "input_hash": input_hash,
        "previous_evidence_hash": previous_evidence_hash,
        "commit": commit,
        "test_id": test_id,
        "canonicalization_contract": CONTRACT_ID,
        "maze_authority_granted": bool(maze_authority_granted),
        "privileged_operation_performed": bool(privileged_operation_performed),
        "limitations": list(limitations or []),
        "signature": signature,  # may be None — legitimate
    }
    if extra:
        for k, v in extra.items():
            if k not in ("evidence_hash", "signature"):
                record[k] = v
    record["evidence_hash"] = canonical_hash(_material_for_hash(record))
    return record


def verify_fm_evidence_artifact(record: Mapping[str, Any]) -> bool:
    """True if evidence_hash matches canonicalization_v0 over material fields."""
    if not isinstance(record, Mapping):
        return False
    stored = record.get("evidence_hash")
    if not isinstance(stored, str) or not stored:
        return False
    if record.get("canonicalization_contract") not in (None, CONTRACT_ID, "canonicalization_v0"):
        # Unknown contract — do not pretend verify
        return False
    return stored == canonical_hash(_material_for_hash(record))


def mutate_detectable(record: Mapping[str, Any], field: str, new_value: Any) -> bool:
    """Return True if changing field invalidates the stored evidence_hash."""
    if field in ("evidence_hash", "signature"):
        return False  # not part of material / or signature separate
    altered: MutableMapping[str, Any] = dict(record)
    altered[field] = new_value
    # recompute as attacker might forget to fix hash — stored hash should not match
    return not verify_fm_evidence_artifact(altered)
