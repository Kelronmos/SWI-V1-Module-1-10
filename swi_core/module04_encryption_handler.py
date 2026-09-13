"""
Module 04: Encryption Handler (AES-256 Shields)

WHAT THIS ACTUALLY DOES:
Wraps AES-256-GCM (via the `cryptography` package, which uses OpenSSL) to
encrypt and decrypt byte payloads with authenticated encryption -- tampering
with ciphertext causes decryption to fail loudly rather than silently
returning corrupted data.

WHAT THIS DOES NOT DO:
It does not manage key distribution, rotation, or storage -- callers must
handle key custody themselves (e.g. via an HSM or secrets manager). It is
"quantum-resistant" in no special sense beyond whatever AES-256 itself
offers against known quantum attacks (Grover's algorithm roughly halves
AES's effective key strength, so AES-256 remains adequate; this is not the
same as a purpose-built post-quantum scheme, and no such claim is made).
"""
from __future__ import annotations
import os
from dataclasses import dataclass
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


@dataclass
class EncryptedPayload:
    nonce: bytes
    ciphertext: bytes


class EncryptionHandler:
    """Module 04: AES-256-GCM authenticated encryption."""

    def __init__(self, key: bytes = None):
        self.key = key or AESGCM.generate_key(bit_length=256)
        self._aesgcm = AESGCM(self.key)

    def encrypt(self, plaintext: bytes, associated_data: bytes = None) -> EncryptedPayload:
        nonce = os.urandom(12)
        ciphertext = self._aesgcm.encrypt(nonce, plaintext, associated_data)
        return EncryptedPayload(nonce=nonce, ciphertext=ciphertext)

    def decrypt(self, payload: EncryptedPayload, associated_data: bytes = None) -> bytes:
        return self._aesgcm.decrypt(payload.nonce, payload.ciphertext, associated_data)
