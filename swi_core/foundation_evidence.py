"""
V1 Foundation Evidence Producer

Produces a versioned FoundationEvidenceEnvelope from a successful PipelineResult
for cross-repository consumption (V2 M11).

Integrity (SHA-256) covers ONLY:
  payload, foundation_version, evidence_schema_version,
  evidence_id, source_reference

created_at is export metadata and is NOT included in the integrity digest.

This does NOT: sign the envelope (CRTG pending); prove truth/safety;
authenticate the sender; replace Foundation Seal 5.
"""
from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import asdict, dataclass
from typing import Any, Optional

from .module00_trainer import PipelineResult

FOUNDATION_VERSION = "1.0-proposed"
EVIDENCE_SCHEMA_VERSION = "1.0-proposed"
VERIFICATION_STATUS_V1_PIPELINE = "v1_trainer_pipeline_completed"
SOURCE_REFERENCE = "Kelronmos/SWI-V1-Module-1-10:Trainer.process"


@dataclass(frozen=True)
class FoundationEvidenceEnvelope:
    """Versioned V1→V2 foundation evidence (producer side)."""

    payload: Any
    foundation_version: str
    evidence_schema_version: str
    evidence_id: str
    integrity_reference: str
    verification_status: str
    source_reference: str
    created_at: float  # metadata only — not part of integrity digest


def compute_integrity_reference(
    payload: Any,
    foundation_version: str,
    evidence_schema_version: str,
    evidence_id: str,
    source_reference: str,
) -> str:
    """Digest of integrity-covered fields only (excludes created_at)."""
    material = {
        "payload": payload,
        "foundation_version": foundation_version,
        "evidence_schema_version": evidence_schema_version,
        "evidence_id": evidence_id,
        "source_reference": source_reference,
    }
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _payload_from_pipeline(result: PipelineResult) -> dict:
    security = None
    if result.security is not None:
        sec = result.security
        security = {
            "risk_score": sec.risk_score,
            "triggered": list(sec.triggered),
            "block_threshold": sec.block_threshold,
            "blocked": sec.risk_score >= sec.block_threshold,
        }
    redaction = None
    if result.redaction is not None:
        redaction = {
            "redacted_text": result.redaction.redacted_text,
            "match_categories": [m.category for m in result.redaction.matches],
        }
    drift = None
    if result.drift is not None:
        drift = {
            "similarity": result.drift.similarity,
            "drifted": result.drift.drifted,
        }
    sync = {
        "gap_seconds": result.sync.gap_seconds,
        "stale": result.sync.stale,
        "out_of_order": result.sync.out_of_order,
    }
    return {
        "allowed": result.allowed,
        "reason": result.reason,
        "security": security,
        "sync": sync,
        "redaction": redaction,
        "drift": drift,
    }


def export_foundation_evidence(
    result: PipelineResult,
    *,
    evidence_id: Optional[str] = None,
    source_reference: str = SOURCE_REFERENCE,
) -> FoundationEvidenceEnvelope:
    if not isinstance(result, PipelineResult):
        raise TypeError(
            f"export requires PipelineResult, got {type(result).__name__}"
        )
    eid = evidence_id or f"v1-evidence-{uuid.uuid4().hex[:16]}"
    payload = _payload_from_pipeline(result)
    integrity = compute_integrity_reference(
        payload=payload,
        foundation_version=FOUNDATION_VERSION,
        evidence_schema_version=EVIDENCE_SCHEMA_VERSION,
        evidence_id=eid,
        source_reference=source_reference,
    )
    return FoundationEvidenceEnvelope(
        payload=payload,
        foundation_version=FOUNDATION_VERSION,
        evidence_schema_version=EVIDENCE_SCHEMA_VERSION,
        evidence_id=eid,
        integrity_reference=integrity,
        verification_status=VERIFICATION_STATUS_V1_PIPELINE,
        source_reference=source_reference,
        created_at=time.time(),
    )


def envelope_to_dict(envelope: FoundationEvidenceEnvelope) -> dict:
    return asdict(envelope)
