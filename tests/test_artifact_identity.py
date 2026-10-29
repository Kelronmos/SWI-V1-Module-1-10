"""Tests for SWI artifact identity reference implementation.

PROVEN=NO AUTHORIZED=NO PRODUCTION_AUTHORIZED=NO
"""
from __future__ import annotations

from pathlib import Path

from swi_core.artifact_identity import (
    SCHEMA,
    canonical_json_bytes,
    new_serial,
    new_version_from_bytes,
    register_bytes,
    sha256_bytes,
    sha256_canonical_json,
    sha256_file,
    verify_bytes,
    verify_file,
)

# FIPS 180-2 / common empty and "abc" vectors
SHA256_EMPTY = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
SHA256_ABC = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_sha256_empty_vector():
    assert sha256_bytes(b"") == SHA256_EMPTY


def test_sha256_abc_vector():
    assert sha256_bytes(b"abc") == SHA256_ABC


def test_register_and_verify_match():
    data = b"SWI artifact payload"
    rec = register_bytes(data, artifact_type="binary", media_type="application/octet-stream")
    assert rec["schema"] == SCHEMA
    assert rec["content"]["digest"] == sha256_bytes(data)
    assert rec["authorization_status"] == "NOT_AUTHORIZED"
    assert rec["proof_status"] == "NOT_PROVEN"
    verified = verify_bytes(data, rec)
    assert verified["integrity_status"] == "MATCH"
    assert verified["authorization_status"] == "NOT_AUTHORIZED"
    assert verified["proven"] is False
    assert verified["production_authorized"] is False


def test_verify_mismatch():
    rec = register_bytes(b"original")
    verified = verify_bytes(b"tampered", rec)
    assert verified["integrity_status"] == "MISMATCH"
    assert verified["authorized"] is False


def test_serial_unique():
    s = {new_serial("ART") for _ in range(50)}
    assert len(s) == 50


def test_content_change_new_identity():
    parent = register_bytes(b"v1")
    child = new_version_from_bytes(b"v2", parent, transformation="reprint-layout")
    assert child["artifact_id"] != parent["artifact_id"]
    assert child["content"]["digest"] != parent["content"]["digest"]
    assert parent["artifact_id"] in child["parent_artifacts"]
    assert child["origin_type"] == "REGENERATED"


def test_canonical_json_stable():
    a = {"b": 1, "a": 2}
    b = {"a": 2, "b": 1}
    assert canonical_json_bytes(a) == canonical_json_bytes(b)
    assert sha256_canonical_json(a) == sha256_canonical_json(b)


def test_file_roundtrip(tmp_path: Path):
    p = tmp_path / "x.bin"
    p.write_bytes(b"file-bytes")
    dig, size = sha256_file(p)
    assert size == 10
    rec = register_bytes(p.read_bytes(), artifact_type="binary")
    assert rec["content"]["digest"] == dig
    v = verify_file(p, rec)
    assert v["integrity_status"] == "MATCH"


def test_missing_file_unavailable(tmp_path: Path):
    rec = register_bytes(b"x")
    v = verify_file(tmp_path / "missing.bin", rec)
    assert v["integrity_status"] == "UNAVAILABLE"
    assert v["authorization_status"] == "NOT_AUTHORIZED"
