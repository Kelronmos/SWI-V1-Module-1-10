"""Ed25519 signature verification tests (primitive only)."""
from __future__ import annotations

import pytest

from swi_core.ed25519_sig import (
    SignatureVerificationError,
    canonical_message,
    generate_keypair,
    sign_ed25519,
    verify_canonical_mapping,
    verify_ed25519,
)


def test_round_trip_verify():
    priv, pub = generate_keypair()
    msg = b"swi-v1-trust-test"
    sig = sign_ed25519(priv, msg)
    assert verify_ed25519(pub, msg, sig) is True


def test_tampered_message_fails():
    priv, pub = generate_keypair()
    sig = sign_ed25519(priv, b"original")
    with pytest.raises(SignatureVerificationError):
        verify_ed25519(pub, b"tampered", sig)


def test_wrong_key_fails():
    priv, _ = generate_keypair()
    _, other = generate_keypair()
    sig = sign_ed25519(priv, b"msg")
    with pytest.raises(SignatureVerificationError):
        verify_ed25519(other, b"msg", sig)


def test_canonical_order_independent():
    priv, pub = generate_keypair()
    a = {"task_id": "1", "payload_hash": "x"}
    b = {"payload_hash": "x", "task_id": "1"}
    assert canonical_message(a) == canonical_message(b)
    sig = sign_ed25519(priv, canonical_message(a))
    assert verify_canonical_mapping(pub, b, sig) is True
