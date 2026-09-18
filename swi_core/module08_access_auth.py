"""
Module 08: Access Auth (The Identity Anchor)

WHAT THIS ACTUALLY DOES:
Issues and verifies HMAC-SHA256-signed, expiring session tokens. A token
encodes a subject id and an expiry timestamp; the signature proves the
token was issued by a holder of the secret key and has not been altered.
Verification checks the signature and rejects expired tokens.

Fail-closed: malformed structure, bad base64, bad signature, non-object
JSON, missing sub/exp, non-numeric exp, boolean exp, non-string sub →
VerifyResult(valid=False, reason="malformed_token"). Unexpected exceptions
must not escape.

WHAT THIS DOES NOT DO:
This is a token issuer/verifier, not a full identity provider — it does
not do password storage, MFA, or biometric verification. Secret key
custody is the caller's responsibility.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class VerifyResult:
    valid: bool
    subject: Optional[str] = None
    reason: Optional[str] = None


class AccessAuth:
    """Module 08: HMAC-signed expiring session tokens (2-part payload.sig)."""

    def __init__(self, secret_key: bytes = None):
        self.secret_key = secret_key or hashlib.sha256(str(time.time()).encode()).digest()

    def _sign(self, message: bytes) -> bytes:
        return hmac.new(self.secret_key, message, hashlib.sha256).digest()

    def issue_token(self, subject: str, ttl_seconds: float = 3600.0) -> str:
        if not isinstance(subject, str) or not subject:
            raise ValueError("subject must be a non-empty string")
        payload = {"sub": subject, "exp": time.time() + ttl_seconds}
        payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        signature = self._sign(payload_bytes)
        token = (
            base64.urlsafe_b64encode(payload_bytes)
            + b"."
            + base64.urlsafe_b64encode(signature)
        )
        return token.decode("ascii")

    def verify_token(self, token: str) -> VerifyResult:
        """Verify token. Always returns VerifyResult; never raises on bad input."""
        try:
            parts = token.encode("ascii").split(b".")
            if len(parts) != 2:
                return VerifyResult(valid=False, reason="malformed_token")
            payload_b64, sig_b64 = parts
            payload_bytes = base64.urlsafe_b64decode(payload_b64)
            signature = base64.urlsafe_b64decode(sig_b64)
        except Exception:
            return VerifyResult(valid=False, reason="malformed_token")

        expected_sig = self._sign(payload_bytes)
        if not hmac.compare_digest(signature, expected_sig):
            return VerifyResult(valid=False, reason="bad_signature")

        try:
            payload = json.loads(payload_bytes)
            if not isinstance(payload, dict):
                return VerifyResult(valid=False, reason="malformed_token")
            if "exp" not in payload or "sub" not in payload:
                return VerifyResult(valid=False, reason="malformed_token")
            exp = payload["exp"]
            sub = payload["sub"]
            # bool is a subclass of int — reject explicitly
            if isinstance(exp, bool) or not isinstance(exp, (int, float)):
                return VerifyResult(valid=False, reason="malformed_token")
            if not isinstance(sub, str) or not sub:
                return VerifyResult(valid=False, reason="malformed_token")
        except Exception:
            return VerifyResult(valid=False, reason="malformed_token")

        if time.time() > exp:
            return VerifyResult(valid=False, subject=sub, reason="expired")

        return VerifyResult(valid=True, subject=sub)
