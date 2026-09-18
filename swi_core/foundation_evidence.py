"""
V1 Foundation Evidence Producer

Produces a versioned FoundationEvidenceEnvelope from a successful PipelineResult
for cross-repository consumption (V2 M11).

Integrity (SHA-256) covers ONLY:
  payload, foundation_version, evidence_schema_version,
  evidence_id, source_reference

created_at is export metadata and is NOT included in the integrity digest.

Seal 5 path (v0): optional Ed25519 over integrity-bound material.
Does NOT: prove truth/safety; CRTG; production key custody; HSM.
Private keys must never be committed.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import asdict, dataclass
from typing import Any, Optional

from .module00_trainer import PipelineResult

FOUNDATION_VERSION = "1.0-proposed"
EVIDENCE_SCHEMA_VERSION = "1.0-proposed"
VERIFICATION_STATUS_V1_PIPELINE = "v1_trainer_pipeline_completed"
SOURCE_REFERENCE = "Kelronmos/SWI-V1-Module-1-10:Trainer.process"
SEAL5_VERSION = "seal5-v0"


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


@dataclass(frozen=True)
class SignedFoundationEvidence:
    envelope: FoundationEvidenceEnvelope
    signature_hex: str
    public_key_hex: str
    seal5_version: str = SEAL5_VERSION


def compute_integrity_reference(
    payload: Any,
    foundation_version: str,
    evidence_schema_version: str,
    evidence_id: str,
    source_reference: str,
) -> str:
    """Digest of integrity-covered fields only (excludes created_at).

    Delegates to swi_core.canonical (Lane B canonicalization_v0).
    """
    from .canonical import compute_integrity_reference as _canonical_integrity

    return _canonical_integrity(
        payload,
        foundation_version,
        evidence_schema_version,
        evidence_id,
        source_reference,
    )


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
        red = result.redaction
        redaction = {
            "redacted_text": red.redacted_text,
            "match_count": len(red.matches),
            "categories": sorted({m.category for m in red.matches}),
        }
    drift = None
    if result.drift is not None:
        d = result.drift
        drift = {"similarity": d.similarity, "drifted": d.drifted}
    sync = None
    if result.sync is not None:
        s = result.sync
        sync = {
            "stale": s.stale,
            "out_of_order": s.out_of_order,
            "gap_seconds": s.gap_seconds,
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
        raise TypeError("export_foundation_evidence requires a PipelineResult")
    payload = _payload_from_pipeline(result)
    eid = evidence_id or str(uuid.uuid4())
    integrity = compute_integrity_reference(
        payload,
        FOUNDATION_VERSION,
        EVIDENCE_SCHEMA_VERSION,
        eid,
        source_reference,
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


def seal5_sign_material(envelope: FoundationEvidenceEnvelope) -> dict:
    """Material covered by Seal 5 signature (integrity-bound fields only)."""
    return {
        "payload": envelope.payload,
        "foundation_version": envelope.foundation_version,
        "evidence_schema_version": envelope.evidence_schema_version,
        "evidence_id": envelope.evidence_id,
        "integrity_reference": envelope.integrity_reference,
        "verification_status": envelope.verification_status,
        "source_reference": envelope.source_reference,
    }


def sign_foundation_evidence(
    envelope: FoundationEvidenceEnvelope,
    private_key: bytes,
    public_key: bytes,
) -> SignedFoundationEvidence:
    """Optional Seal 5 Ed25519 signature over integrity-bound material."""
    from .ed25519_sig import canonical_message, sign_ed25519

    material = seal5_sign_material(envelope)
    msg = canonical_message(material)
    sig = sign_ed25519(private_key, msg)
    return SignedFoundationEvidence(
        envelope=envelope,
        signature_hex=sig.hex(),
        public_key_hex=public_key.hex(),
        seal5_version=SEAL5_VERSION,
    )


def verify_signed_foundation_evidence(signed: SignedFoundationEvidence) -> bool:
    """Verify Seal 5 signature. Raises SignatureVerificationError on failure."""
    from .ed25519_sig import SignatureVerificationError, canonical_message, verify_ed25519

    if signed.seal5_version != SEAL5_VERSION:
        raise SignatureVerificationError("seal5_version mismatch")
    material = seal5_sign_material(signed.envelope)
    msg = canonical_message(material)
    pub = bytes.fromhex(signed.public_key_hex)
    sig = bytes.fromhex(signed.signature_hex)
    return verify_ed25519(pub, msg, sig)


def signed_to_dict(signed: SignedFoundationEvidence) -> dict:
    d = envelope_to_dict(signed.envelope)
    d["seal5"] = {
        "version": signed.seal5_version,
        "signature_hex": signed.signature_hex,
        "public_key_hex": signed.public_key_hex,
    }
    return d
