"""Lane B — adversarial / non-authority tests."""
from __future__ import annotations

import pytest

from swi_core.canonical import canonical_dumps, canonical_hash, compute_integrity_reference


def test_bool_distinct_from_string():
    assert canonical_hash({"v": True}) != canonical_hash({"v": "true"})


def test_null_vs_missing_key():
    assert canonical_hash({"a": None}) != canonical_hash({})


def test_default_str_for_non_json_type():
    class X:
        def __str__(self) -> str:
            return "X-instance"

    assert "X-instance" in canonical_dumps({"o": X()})


def test_canonical_does_not_inject_authority_fields():
    h = compute_integrity_reference(
        {"allowed": True}, "1.0-proposed", "1.0-proposed", "e", "s"
    )
    assert isinstance(h, str) and len(h) == 64


def test_nan_rejected():
    with pytest.raises(ValueError, match="non-finite"):
        canonical_dumps({"x": float("nan")})


def test_infinity_rejected():
    with pytest.raises(ValueError, match="non-finite"):
        canonical_dumps({"x": float("inf")})


def test_nested_nan_rejected():
    with pytest.raises(ValueError, match="non-finite"):
        compute_integrity_reference(
            {"nested": {"v": float("nan")}},
            "1.0-proposed",
            "1.0-proposed",
            "e",
            "s",
        )
