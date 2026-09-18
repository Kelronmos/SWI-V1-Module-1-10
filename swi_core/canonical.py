"""Lane B — frozen canonicalization for integrity digests.

STATUS: IMPLEMENTED / TESTED (not sealed).

Contract id: canonicalization_v0

Rules:
  - json.dumps(..., sort_keys=True, separators=(",", ":"), default=str)
  - UTF-8 encode then SHA-256 hex digest
  - List order preserved; object keys sorted at every level
  - Does NOT establish truth, admission, authorization, or action rights

Foundation evidence material (covered fields only):
  payload, foundation_version, evidence_schema_version, evidence_id, source_reference
  (created_at is never included in integrity material)
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

CANONICALIZATION_VERSION = "canonicalization_v0"
_SEPARATORS = (",", ":")


def canonical_dumps(obj: Any) -> str:
    """Deterministic JSON string for integrity hashing."""
    return json.dumps(obj, sort_keys=True, separators=_SEPARATORS, default=str)


def canonical_bytes(obj: Any) -> bytes:
    return canonical_dumps(obj).encode("utf-8")


def canonical_hash(obj: Any) -> str:
    """SHA-256 hex digest of canonical UTF-8 bytes."""
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def foundation_integrity_material(
    payload: Any,
    foundation_version: str,
    evidence_schema_version: str,
    evidence_id: str,
    source_reference: str,
) -> dict[str, Any]:
    """Covered fields only — excludes created_at."""
    return {
        "payload": payload,
        "foundation_version": foundation_version,
        "evidence_schema_version": evidence_schema_version,
        "evidence_id": evidence_id,
        "source_reference": source_reference,
    }


def compute_integrity_reference(
    payload: Any,
    foundation_version: str,
    evidence_schema_version: str,
    evidence_id: str,
    source_reference: str,
) -> str:
    """Digest matching historical V1/V2 foundation evidence algorithm."""
    material = foundation_integrity_material(
        payload,
        foundation_version,
        evidence_schema_version,
        evidence_id,
        source_reference,
    )
    return canonical_hash(material)
