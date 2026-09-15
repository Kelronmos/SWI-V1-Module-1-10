"""
Ed25519 signature helpers (V1 side).

STATUS: IMPLEMENTED / TESTED for the cryptographic primitive only.
Not CRTG. Not certificate validation. Private keys must not be committed.
"""
from __future__ import annotations

import json
from typing import Any, Mapping, Union

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)

PUBLIC_KEY_LEN = 32
SIGNATURE_LEN = 64
PRIVATE_KEY_LEN = 32


class SignatureVerificationError(ValueError):
    """Raised when Ed25519 verification fails or inputs are malformed."""


def canonical_message(material: Mapping[str, Any]) -> bytes:
    if not isinstance(material, Mapping):
        raise TypeError("canonical_message requires a mapping")
    return json.dumps(
        material, sort_keys=True, separators=(",", ":"), default=str
    ).encode("utf-8")


def _as_public_key(public_key: Union[bytes, Ed25519PublicKey]) -> Ed25519PublicKey:
    if isinstance(public_key, Ed25519PublicKey):
        return public_key
    if not isinstance(public_key, (bytes, bytearray)):
        raise SignatureVerificationError(
            f"public_key must be bytes or Ed25519PublicKey, got {type(public_key).__name__}"
        )
    raw = bytes(public_key)
    if len(raw) != PUBLIC_KEY_LEN:
        raise SignatureVerificationError(
            f"Ed25519 public key must be {PUBLIC_KEY_LEN} bytes, got {len(raw)}"
        )
    try:
        return Ed25519PublicKey.from_public_bytes(raw)
    except Exception as exc:
        raise SignatureVerificationError(f"invalid Ed25519 public key: {exc}") from exc


def verify_ed25519(
    public_key: Union[bytes, Ed25519PublicKey],
    message: bytes,
    signature: bytes,
) -> bool:
    if not isinstance(message, (bytes, bytearray)):
        raise SignatureVerificationError(
            f"message must be bytes, got {type(message).__name__}"
        )
    if not isinstance(signature, (bytes, bytearray)):
        raise SignatureVerificationError(
            f"signature must be bytes, got {type(signature).__name__}"
        )
    sig = bytes(signature)
    if len(sig) != SIGNATURE_LEN:
        raise SignatureVerificationError(
            f"Ed25519 signature must be {SIGNATURE_LEN} bytes, got {len(sig)}"
        )
    key = _as_public_key(public_key)
    try:
        key.verify(sig, bytes(message))
    except InvalidSignature as exc:
        raise SignatureVerificationError("Ed25519 signature verification failed") from exc
    except Exception as exc:
        raise SignatureVerificationError(f"Ed25519 verification error: {exc}") from exc
    return True


def verify_canonical_mapping(
    public_key: Union[bytes, Ed25519PublicKey],
    material: Mapping[str, Any],
    signature: bytes,
) -> bool:
    return verify_ed25519(public_key, canonical_message(material), signature)


def sign_ed25519(private_key: Union[bytes, Ed25519PrivateKey], message: bytes) -> bytes:
    if not isinstance(message, (bytes, bytearray)):
        raise TypeError(f"message must be bytes, got {type(message).__name__}")
    if isinstance(private_key, Ed25519PrivateKey):
        key = private_key
    else:
        raw = bytes(private_key)
        if len(raw) != PRIVATE_KEY_LEN:
            raise ValueError(
                f"Ed25519 private key must be {PRIVATE_KEY_LEN} bytes, got {len(raw)}"
            )
        key = Ed25519PrivateKey.from_private_bytes(raw)
    return key.sign(bytes(message))


def generate_keypair() -> tuple[bytes, bytes]:
    priv = Ed25519PrivateKey.generate()
    priv_raw = priv.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
    pub_raw = priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return priv_raw, pub_raw
