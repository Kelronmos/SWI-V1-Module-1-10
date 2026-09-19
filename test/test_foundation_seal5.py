"""Foundation Seal 5 v0 — sign/verify path (not production custody)."""
from __future__ import annotations

import pytest

from swi_core.ed25519_sig import SignatureVerificationError, generate_keypair
from swi_core.foundation_evidence import (
    FoundationEvidenceEnvelope,
    SEAL5_VERSION,
    SignedFoundationEvidence,
    compute_integrity_reference,
    sign_foundation_evidence,
    verify_signed_foundation_evidence,
)
from swi_core.module_kernel import AdmissionRequiredError
from swi_test_helpers.admission import TEST_COMMIT, sign_admission


def _sample_envelope() -> FoundationEvidenceEnvelope:
    payload = {"allowed": True, "reason": "test"}
    eid = "v1-evidence-seal5test01"
    src = "test:seal5"
    integrity = compute_integrity_reference(
        payload=payload,
        foundation_version="1.0-proposed",
        evidence_schema_version="1.0-proposed",
        evidence_id=eid,
        source_reference=src,
    )
    return FoundationEvidenceEnvelope(
        payload=payload,
        foundation_version="1.0-proposed",
        evidence_schema_version="1.0-proposed",
        evidence_id=eid,
        integrity_reference=integrity,
        verification_status="v1_trainer_pipeline_completed",
        source_reference=src,
        created_at=0.0,
    )


def test_seal5_sign_verify_roundtrip():
    priv, pub = generate_keypair()
    env = _sample_envelope()
    signed = sign_foundation_evidence(
        env, priv, admission=sign_admission(), expected_commit=TEST_COMMIT
    )
    assert signed.public_key_hex == pub.hex()
    assert signed.seal5_version == SEAL5_VERSION
    assert verify_signed_foundation_evidence(signed) is True


def test_seal5_tampered_integrity_fails():
    priv, _ = generate_keypair()
    env = _sample_envelope()
    signed = sign_foundation_evidence(
        env, priv, admission=sign_admission(), expected_commit=TEST_COMMIT
    )
    bad_env = FoundationEvidenceEnvelope(
        payload=env.payload,
        foundation_version=env.foundation_version,
        evidence_schema_version=env.evidence_schema_version,
        evidence_id=env.evidence_id,
        integrity_reference="0" * 64,
        verification_status=env.verification_status,
        source_reference=env.source_reference,
        created_at=env.created_at,
    )
    tampered = SignedFoundationEvidence(
        envelope=bad_env,
        signature_hex=signed.signature_hex,
        public_key_hex=signed.public_key_hex,
        seal5_version=signed.seal5_version,
    )
    with pytest.raises(SignatureVerificationError):
        verify_signed_foundation_evidence(tampered)


def test_seal5_wrong_key_fails():
    priv1, _ = generate_keypair()
    _, pub2 = generate_keypair()
    env = _sample_envelope()
    signed = sign_foundation_evidence(
        env, priv1, admission=sign_admission(), expected_commit=TEST_COMMIT
    )
    swapped = SignedFoundationEvidence(
        envelope=signed.envelope,
        signature_hex=signed.signature_hex,
        public_key_hex=pub2.hex(),
        seal5_version=signed.seal5_version,
    )
    with pytest.raises(SignatureVerificationError):
        verify_signed_foundation_evidence(swapped)


def test_seal5_sign_rejects_without_admission():
    priv, _ = generate_keypair()
    env = _sample_envelope()
    with pytest.raises(AdmissionRequiredError):
        sign_foundation_evidence(env, priv)
