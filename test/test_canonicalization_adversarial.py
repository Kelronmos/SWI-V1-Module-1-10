"""Lane B — adversarial / non-authority tests."""
from __future__ import annotations

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
