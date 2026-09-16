"""Regression: Module 08 must fail closed on malformed tokens (no crashes)."""
from __future__ import annotations

import base64
import json

from swi_core.module08_access_auth import AccessAuth


def test_access_auth_valid_token():
    auth = AccessAuth(secret_key=b"test-secret-key-32bytes-long!!!!")
    token = auth.issue_token("alice", ttl_seconds=60)
    result = auth.verify_token(token)
    assert result.valid is True
    assert result.subject == "alice"


def test_access_auth_rejects_malformed_json():
    auth = AccessAuth(secret_key=b"test-secret-key-32bytes-long!!!!")
    # Valid outer structure but payload is not JSON
    bad_payload = base64.urlsafe_b64encode(b"not-json")
    bad_sig = base64.urlsafe_b64encode(b"x" * 32)
    token = (bad_payload + b"." + bad_sig).decode("ascii")
    result = auth.verify_token(token)
    assert result.valid is False
    assert result.reason in ("malformed_token", "bad_signature")


def test_access_auth_rejects_missing_fields():
    auth = AccessAuth(secret_key=b"test-secret-key-32bytes-long!!!!")
    payload = {"sub": "alice"}  # missing exp
    payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
    sig = auth._sign(payload_bytes)
    token = (
        base64.urlsafe_b64encode(payload_bytes)
        + b"."
        + base64.urlsafe_b64encode(sig)
    ).decode("ascii")
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
