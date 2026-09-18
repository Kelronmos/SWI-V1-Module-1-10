"""Cross-repo golden vectors for canonicalization_v0."""
from __future__ import annotations

import json
from pathlib import Path

from swi_core.canonical import canonical_hash

_VECTORS = Path(__file__).resolve().parent / "fixtures" / "canonical_vectors.json"


def test_golden_vectors_match():
    data = json.loads(_VECTORS.read_text(encoding="utf-8"))
    assert len(data) >= 8
    for row in data:
        assert canonical_hash(row["input"]) == row["expected_digest"], row["name"]


def test_simple_and_reordered_same_digest():
    data = {r["name"]: r for r in json.loads(_VECTORS.read_text())}
    assert (
        data["simple_object"]["expected_digest"]
        == data["reordered_equivalent"]["expected_digest"]
    )
