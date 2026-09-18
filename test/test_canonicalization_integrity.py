"""Lane B — integrity binding and created_at exclusion."""
from __future__ import annotations

import json

from swi_core.canonical import (
    canonical_hash,
    compute_integrity_reference,
    foundation_integrity_material,
)
from swi_core.foundation_evidence import compute_integrity_reference as fe_compute


def test_created_at_not_in_material():
    material = foundation_integrity_material(
        {"allowed": True}, "1.0-proposed", "1.0-proposed", "id-1", "src"
    )
    assert "created_at" not in material


def test_payload_change_changes_digest():
    base = dict(
        payload={"allowed": True},
        foundation_version="1.0-proposed",
        evidence_schema_version="1.0-proposed",
        evidence_id="e1",
        source_reference="t",
    )
    h1 = compute_integrity_reference(**base)
    h2 = compute_integrity_reference(**{**base, "payload": {"allowed": False}})
    assert h1 != h2


def test_evidence_id_change_changes_digest():
    h1 = compute_integrity_reference({"a": 1}, "1.0-proposed", "1.0-proposed", "e1", "s")
    h2 = compute_integrity_reference({"a": 1}, "1.0-proposed", "1.0-proposed", "e2", "s")
    assert h1 != h2


def test_matches_foundation_evidence_delegate():
    args = ({"x": 1}, "1.0-proposed", "1.0-proposed", "fixed", "trainer")
    assert compute_integrity_reference(*args) == fe_compute(*args)


def test_pretty_json_after_parse_same_hash():
    logical = {"b": 2, "a": 1}
    loaded = json.loads(json.dumps(logical, indent=2))
    assert canonical_hash(logical) == canonical_hash(loaded)
