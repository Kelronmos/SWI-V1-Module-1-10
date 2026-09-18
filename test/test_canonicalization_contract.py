"""Lane B — canonicalization contract tests (no mocks)."""
from __future__ import annotations

from swi_core.canonical import (
    CANONICALIZATION_VERSION,
    canonical_dumps,
    canonical_hash,
)


def test_key_order_independent():
    assert canonical_dumps({"b": 1, "a": 2}) == canonical_dumps({"a": 2, "b": 1})
    assert canonical_hash({"b": 1, "a": 2}) == canonical_hash({"a": 2, "b": 1})


def test_nested_key_order_independent():
    a = {"z": {"b": 1, "a": 2}, "y": 0}
    b = {"y": 0, "z": {"a": 2, "b": 1}}
    assert canonical_hash(a) == canonical_hash(b)


def test_list_order_preserved():
    assert canonical_dumps([1, 2, 3]) != canonical_dumps([3, 2, 1])


def test_compact_separators():
    s = canonical_dumps({"a": 1, "b": 2})
    assert ": " not in s and ", " not in s
    assert s == '{"a":1,"b":2}'


def test_determinism_repeated():
    obj = {"k": [1, {"x": True}], "n": None}
    h0 = canonical_hash(obj)
    assert all(canonical_hash(obj) == h0 for _ in range(50))


def test_empty_object_and_array():
    assert canonical_dumps({}) == "{}"
    assert canonical_dumps([]) == "[]"


def test_version_constant():
    assert CANONICALIZATION_VERSION == "canonicalization_v0"
