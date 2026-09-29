"""Bounded replay tests for source admission.

REPLAYABLE within the tested source-admission contract and evidence format only.
Does not close FM-005–013, Universal Gate, or claim legal compliance.
"""
from __future__ import annotations

from dataclasses import replace

import pytest

from swi_core.source_admission import (
    DecisionStatus,
    ReplayResultStatus,
    SourceAdmissionRecord,
    SourceDescriptor,
    evaluate_source,
    replay_admission,
)

_VALID_HASH = "a" * 64
_OTHER_HASH = "b" * 64


def _valid_source(**overrides) -> SourceDescriptor:
    base = dict(
        source_id="src-replay-001",
        origin="https://example.com/org/repo",
        version="1.0.0",
        content_hash=_VALID_HASH,
        presented_hash=_VALID_HASH,
        license_id="Apache-2.0",
        target_boundary="SWI_PRIVILEGED_EXECUTION",
        provenance_verified=True,
        privacy_clear=True,
        architecture_allowed=True,
        claimed_authorized=False,
    )
    base.update(overrides)
    return SourceDescriptor(**base)


def test_replay_same_pass_evidence_ok():
    original = evaluate_source(_valid_source())
    assert original.decision == DecisionStatus.PASS
    result = replay_admission(original)
    assert result.status == ReplayResultStatus.REPLAY_OK
    assert result.original_decision == "PASS"
    assert result.replayed_decision == "PASS"
    assert result.original_evidence_hash == result.replayed_evidence_hash
    assert result.reason == "SAME_DECISION_SAME_HASH"


def test_replay_same_halt_evidence_ok():
    original = evaluate_source(_valid_source(license_id=None))
    assert original.decision == DecisionStatus.HALT
    result = replay_admission(original)
    assert result.status == ReplayResultStatus.REPLAY_OK
    assert result.original_decision == "HALT"
    assert result.replayed_decision == "HALT"
    assert result.original_evidence_hash == result.replayed_evidence_hash


def test_replay_source_bytes_modified_invalid():
    """Mutate source after original PASS — old decision must not survive."""
    original = evaluate_source(_valid_source())
    assert original.decision == DecisionStatus.PASS
    mutated = _valid_source(presented_hash=_OTHER_HASH)
    result = replay_admission(original, source_override=mutated)
    assert result.status == ReplayResultStatus.REPLAY_INVALID
    assert result.reason in {"DECISION_MISMATCH", "EVIDENCE_HASH_MISMATCH"}
    # Must not remain a free PASS under mutation
    assert not (
        result.replayed_decision == "PASS"
        and result.original_evidence_hash == result.replayed_evidence_hash
    )


def test_replay_evidence_hash_tampered_invalid():
    original = evaluate_source(_valid_source())
    # Tamper stored hash without changing material
    original.evidence_hash = _OTHER_HASH
    result = replay_admission(original)
    assert result.status == ReplayResultStatus.REPLAY_INVALID
    assert result.reason == "EVIDENCE_HASH_TAMPERED"


def test_replay_license_result_modified_invalid():
    original = evaluate_source(_valid_source())
    mutated = _valid_source(license_id=None)
    result = replay_admission(original, source_override=mutated)
    assert result.status == ReplayResultStatus.REPLAY_INVALID
    assert result.replayed_decision == "HALT"


def test_replay_privacy_result_modified_invalid():
    original = evaluate_source(_valid_source())
    mutated = _valid_source(privacy_clear=False)
    result = replay_admission(original, source_override=mutated)
    assert result.status == ReplayResultStatus.REPLAY_INVALID
    assert result.replayed_decision == "HALT"


def test_replay_architecture_result_modified_invalid():
    original = evaluate_source(_valid_source())
    mutated = _valid_source(architecture_allowed=False)
    result = replay_admission(original, source_override=mutated)
    assert result.status == ReplayResultStatus.REPLAY_INVALID
    assert result.replayed_decision == "HALT"


def test_replay_claimed_authorization_cannot_turn_violation_into_pass():
    original = evaluate_source(_valid_source(provenance_verified=False))
    assert original.decision == DecisionStatus.HALT
    # Inject claimed_authorized on replay material — must not become PASS
    mutated = _valid_source(provenance_verified=False, claimed_authorized=True)
    result = replay_admission(original, source_override=mutated)
    # Either still HALT with matching hash path, or INVALID if material diverges
    assert result.replayed_decision != "PASS"
    if result.status == ReplayResultStatus.REPLAY_OK:
        assert result.replayed_decision == "HALT"
    else:
        assert result.status == ReplayResultStatus.REPLAY_INVALID


def test_replay_missing_evidence_hash_not_proven():
    original = evaluate_source(_valid_source())
    original.evidence_hash = None
    result = replay_admission(original)
    assert result.status == ReplayResultStatus.NOT_PROVEN
    assert result.reason == "MISSING_EVIDENCE_HASH"


def test_replay_missing_source_not_proven():
    original = evaluate_source(_valid_source())
    original.source = None
    result = replay_admission(original)
    assert result.status == ReplayResultStatus.NOT_PROVEN
    assert result.reason == "MISSING_SOURCE_DESCRIPTOR"


def test_replay_result_carries_limitation_text():
    original = evaluate_source(_valid_source())
    result = replay_admission(original)
    assert "Universal Gate" in result.limitation
    assert "legal compliance" in result.limitation
