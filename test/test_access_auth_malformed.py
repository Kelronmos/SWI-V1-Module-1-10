"""Regression: Module 08 must fail closed on malformed tokens (no crashes)."""
from __future__ import annotations

import base64
import json
import time

from swi_core.module08_access_auth import AccessAuth


def _signed_token(auth: AccessAuth, payload: dict) -> str:
    payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
    sig = auth._sign(payload_bytes)
    return (
        base64.urlsafe_b64encode(payload_bytes)
        + b"."
        + base64.urlsafe_b64encode(sig)
    ).decode("ascii")


def test_access_auth_valid_token():
    auth = AccessAuth(secret_key=b"test-secret-key-32bytes-long!!!!")
    token = auth.issue_token("alice", ttl_seconds=60)
    result = auth.verify_token(token)
    assert result.valid is True
    assert result.subject == "alice"
    assert result.reason is None


def test_access_auth_rejects_malformed_json():
    auth = AccessAuth(secret_key=b"test-secret-key-32bytes-long!!!!")
    bad_payload = base64.urlsafe_b64encode(b"not-json")
    bad_sig = base64.urlsafe_b64encode(b"x" * 32)
    token = (bad_payload + b"." + bad_sig).decode("ascii")
    result = auth.verify_token(token)
    assert result.valid is False
    assert result.reason in ("malformed_token", "bad_signature")


def test_access_auth_rejects_malformed_but_signed_json():
    """Payload is valid base64 JSON object but missing required semantic fields."""
    auth = AccessAuth(secret_key=b"test-secret-key-32bytes-long!!!!")
    token = _signed_token(auth, {"not_exp": 123, "not_sub": "x"})
    result = auth.verify_token(token)
    assert result.valid is False
    assert result.reason == "malformed_token"


def test_access_auth_rejects_missing_fields():
    auth = AccessAuth(secret_key=b"test-secret-key-32bytes-long!!!!")
    token = _signed_token(auth, {"sub": "alice"})  # missing exp
    result = auth.verify_token(token)
    assert result.valid is False
    assert result.reason == "malformed_token"


def test_access_auth_rejects_missing_sub():
    auth = AccessAuth(secret_key=b"test-secret-key-32bytes-long!!!!")
    token = _signed_token(auth, {"exp": time.time() + 60})
    result = auth.verify_token(token)
    assert result.valid is False
    assert result.reason == "malformed_token"


def test_access_auth_rejects_invalid_expiration_type():
    auth = AccessAuth(secret_key=b"test-secret-key-32bytes-long!!!!")
    token = _signed_token(auth, {"sub": "alice", "exp": "not-a-number"})
    result = auth.verify_token(token)
    assert result.valid is False
    assert result.reason == "malformed_token"


def test_access_auth_rejects_null_expiration():
    auth = AccessAuth(secret_key=b"test-secret-key-32bytes-long!!!!")
    token = _signed_token(auth, {"sub": "alice", "exp": None})
    result = auth.verify_token(token)
    assert result.valid is False
    assert result.reason == "malformed_token"


def test_access_auth_rejects_invalid_base64():
    auth = AccessAuth()
    result = auth.verify_token("%%%not-base64%%%.%%%also-bad%%%")
    assert result.valid is False
    assert result.reason == "malformed_token"


def test_access_auth_rejects_wrong_part_count():
    auth = AccessAuth()
    result = auth.verify_token("only-one-part")
    assert result.valid is False
    assert result.reason == "malformed_token"


def test_access_auth_rejects_expired():
    auth = AccessAuth(secret_key=b"test-secret-key-32bytes-long!!!!")
    token = auth.issue_token("bob", ttl_seconds=-10)
    result = auth.verify_token(token)
    assert result.valid is False
    assert result.reason == "expired"


def test_access_auth_rejects_forged_signature():
    auth = AccessAuth(secret_key=b"test-secret-key-32bytes-long!!!!")
    other = AccessAuth(secret_key=b"different-secret-key-32bytes!!!!!")
    token = other.issue_token("alice", ttl_seconds=60)
    result = auth.verify_token(token)
    assert result.valid is False
    assert result.reason == "bad_signature"
