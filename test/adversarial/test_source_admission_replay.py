"""Adversarial replay tests — layered invalidity, access context, 3-question disposition.

Bounded REPLAYABLE claim only. HASH ≠ AUTHORITY ≠ TRUTH.
FM-005–013 / Universal Gate / Seal 5 / compliance: NOT touched / NOT CLAIMED.
"""
from __future__ import annotations

import pytest

from swi_core.source_admission import (
    DecisionStatus,
    Disposition,
    FailureClass,
    ReplayContext,
    ReplayStatus,
    SourceDescriptor,
    evaluate_source,
    replay_admission,
    three_question_disposition,
)

_VALID_HASH = "c" * 64


def _valid_source(**overrides) -> SourceDescriptor:
    base = dict(
        source_id="src-replay-001",
        origin="https://example.com/org/repo",
        version="1.0.0",
        content_hash=_VALID_HASH,
        presented_hash=_VALID_HASH,
        license_id="MIT",
        target_boundary="SWI_PRIVILEGED_EXECUTION",
        provenance_verified=True,
        privacy_clear=True,
        architecture_allowed=True,
        claimed_authorized=False,
    )
    base.update(overrides)
    return SourceDescriptor(**base)


def test_headline_pass_record_mutate_hash_mismatch_pause_zero_side_effects():
    """Headline adversarial path:

    PASS → record H1 → modify evidence → replay → HASH_MISMATCH
    → PAUSE/BLOCK → violation report → side_effects == 0

    Proves a previously accepted workflow cannot silently continue when
    the cryptographic binding of the recorded evidence has changed.
    """
    side_effects = {"count": 0}

    # 1. PASS and record H1
    recorded = evaluate_source(_valid_source())
    assert recorded.decision == DecisionStatus.PASS
    h1 = recorded.evidence_hash
    assert h1 is not None and len(h1) == 64

    # Optional: would-be continue path only if replay matches (not taken after mutate)
    def protected_continue():
        side_effects["count"] += 1
        return "continued"

    # 2. Modify evidence binding (representation drift / tamper)
    recorded.evidence_hash = "d" * 64

    # 3. Replay under normal access context
    result = replay_admission(
        recorded,
        context=ReplayContext(knowledge_level=1),
        continuation_authority="UNPROVEN",
    )

    # 4. HASH_MISMATCH — not a generic INVALID
    assert result.replay_status in {ReplayStatus.BLOCKED, ReplayStatus.PAUSED}
    assert result.violation is not None
    assert result.violation.failure_class == FailureClass.HASH_MISMATCH
    assert result.violation.cryptographic["recorded_hash"] == "d" * 64
    assert result.violation.cryptographic["recomputed_hash"] == h1
    assert result.violation.cryptographic["match"] is False

    # 5. PAUSE / report / 3 questions / disposition
    assert result.violation.status in {"PAUSED", "BLOCKED"}
    assert result.violation.questions["what_failed"]
    assert result.violation.questions["consequence"]
    assert result.violation.questions["continuation_authority"] == "UNPROVEN"
    assert result.violation.disposition == Disposition.BLOCK

    # 6. Must not continue protected work
    if result.violation.disposition != Disposition.CONTINUE:
        # protected_continue deliberately not invoked
        pass
    else:
        protected_continue()

    assert result.violation.execution["continued"] is False
    assert result.violation.execution["side_effects"] == 0
    assert side_effects["count"] == 0


def test_replay_same_evidence_same_decision():
    recorded = evaluate_source(_valid_source())
    assert recorded.decision == DecisionStatus.PASS
    result = replay_admission(
        recorded,
        source_for_reeval=_valid_source(),
        context=ReplayContext(knowledge_level=1),
    )
    assert result.replay_status == ReplayStatus.REPLAYABLE_BOUNDED
    assert result.recorded_hash == result.recomputed_hash
    assert result.recomputed_decision == recorded.decision.value
    assert result.violation is None


def test_hash_mismatch_is_not_generic_invalid():
    recorded = evaluate_source(_valid_source())
    recorded.evidence_hash = "d" * 64
    result = replay_admission(recorded, context=ReplayContext(knowledge_level=1))
    assert result.replay_status in {ReplayStatus.BLOCKED, ReplayStatus.PAUSED}
    assert result.violation is not None
    assert result.violation.failure_class == FailureClass.HASH_MISMATCH
    assert result.violation.execution["side_effects"] == 0
    assert result.violation.execution["continued"] is False
    assert result.violation.questions["continuation_authority"] == "UNPROVEN"
    assert result.violation.disposition == Disposition.BLOCK


def test_schema_invalid_layered():
    recorded = evaluate_source(_valid_source())
    recorded.source = None  # type: ignore[assignment]
    result = replay_admission(recorded)
    assert result.violation is not None
    assert result.violation.failure_class == FailureClass.SCHEMA_INVALID
    assert result.violation.execution["side_effects"] == 0


def test_access_limited_not_false_original_decision():
    recorded = evaluate_source(_valid_source())
    result = replay_admission(
        recorded,
        context=ReplayContext(knowledge_level=1),
        required_knowledge_level=3,
    )
    assert result.replay_status == ReplayStatus.REPLAY_LIMITED_BY_ACCESS_CONTEXT
    assert result.violation is None
    assert any(l.layer == "access" and l.status == "LIMITED" for l in result.layers)


def test_restricted_info_without_level_blocks():
    recorded = evaluate_source(_valid_source())
    result = replay_admission(
        recorded,
        context=ReplayContext(knowledge_level=1, restricted_information_used=True),
        required_knowledge_level=1,
    )
    assert result.replay_status == ReplayStatus.BLOCKED
    assert result.violation is not None
    assert result.violation.failure_class == FailureClass.ACCESS_CONTEXT_INVALID
    assert result.violation.execution["side_effects"] == 0


def test_source_mutated_blocks():
    recorded = evaluate_source(_valid_source())
    mutated = _valid_source(version="2.0.0", content_hash="e" * 64, presented_hash="e" * 64)
    result = replay_admission(
        recorded,
        source_for_reeval=mutated,
        context=ReplayContext(knowledge_level=1),
    )
    assert result.replay_status == ReplayStatus.BLOCKED
    assert result.violation is not None
    assert result.violation.failure_class == FailureClass.SOURCE_MUTATED
    assert result.violation.execution["side_effects"] == 0


def test_decision_mismatch_blocks():
    recorded = evaluate_source(_valid_source())
    changed = _valid_source(
        privacy_clear=False,
        source_id=recorded.source.source_id,  # type: ignore[union-attr]
        content_hash=recorded.source.content_hash,  # type: ignore[union-attr]
        presented_hash=recorded.source.content_hash,  # type: ignore[union-attr]
        version=recorded.source.version,  # type: ignore[union-attr]
    )
    result = replay_admission(
        recorded,
        source_for_reeval=changed,
        context=ReplayContext(knowledge_level=1),
    )
    assert result.replay_status == ReplayStatus.BLOCKED
    assert result.violation is not None
    assert result.violation.failure_class == FailureClass.DECISION_MISMATCH
    assert result.recomputed_decision == DecisionStatus.HALT.value


def test_three_question_continue_requires_explicit_authority():
    assert (
        three_question_disposition(
            what_failed="x",
            consequence="y",
            continuation_authority="UNPROVEN",
            failure=FailureClass.HASH_MISMATCH,
        )
        == Disposition.BLOCK
    )
    assert (
        three_question_disposition(
            what_failed="x",
            consequence="y",
            continuation_authority="AUTHORIZED:scope=dev-only",
            failure=FailureClass.HASH_MISMATCH,
        )
        == Disposition.CONTINUE
    )


def test_violation_report_answers_three_questions():
    recorded = evaluate_source(_valid_source())
    recorded.evidence_hash = "f" * 64
    result = replay_admission(recorded)
    q = result.violation.questions  # type: ignore[union-attr]
    assert "what_failed" in q and q["what_failed"]
    assert "consequence" in q and q["consequence"]
    assert q["continuation_authority"] == "UNPROVEN"
