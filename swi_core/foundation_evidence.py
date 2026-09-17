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


# --- Foundation Seal 5 v0 (optional signature path) ---

SEAL5_VERSION = "0.1-proposed"
# Pinned verification key (hex). Empty = pin not established; verify still works with key on artifact.
SEAL5_PINNED_PUBLIC_KEY_HEX = ""


@dataclass(frozen=True)
class SignedFoundationEvidence:
    """Envelope plus Seal 5 signature material (producer-side)."""

    envelope: FoundationEvidenceEnvelope
    signature_hex: str
    public_key_hex: str
    seal5_version: str = SEAL5_VERSION


def seal5_sign_material(envelope: FoundationEvidenceEnvelope) -> dict:
    """Fields covered by Seal 5 signature (deterministic)."""
    return {
        "evidence_id": envelope.evidence_id,
        "foundation_version": envelope.foundation_version,
        "evidence_schema_version": envelope.evidence_schema_version,
        "integrity_reference": envelope.integrity_reference,
        "source_reference": envelope.source_reference,
        "verification_status": envelope.verification_status,
        "seal5_version": SEAL5_VERSION,
    }


def sign_foundation_evidence(
    envelope: FoundationEvidenceEnvelope,
    private_key: bytes,
) -> SignedFoundationEvidence:
    """Sign integrity-bound material. Private key from env/CI only — never from git."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

    from .ed25519_sig import canonical_message, sign_ed25519

    material = seal5_sign_material(envelope)
    msg = canonical_message(material)
    sig = sign_ed25519(private_key, msg)
    if isinstance(private_key, Ed25519PrivateKey):
        pub = private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    else:
        pub = Ed25519PrivateKey.from_private_bytes(bytes(private_key)).public_key().public_bytes(
            Encoding.Raw, PublicFormat.Raw
        )
    return SignedFoundationEvidence(
        envelope=envelope,
        signature_hex=sig.hex(),
        public_key_hex=pub.hex(),
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
