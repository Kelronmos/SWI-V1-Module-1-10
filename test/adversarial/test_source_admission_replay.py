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
    RecordedContext,
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
    side_effects = {"count": 0}
    recorded = evaluate_source(_valid_source())
    assert recorded.decision == DecisionStatus.PASS
    h1 = recorded.evidence_hash
    assert h1 is not None and len(h1) == 64

    def protected_continue():
        side_effects["count"] += 1
        return "continued"

    recorded.evidence_hash = "d" * 64
    result = replay_admission(
        recorded,
        context=ReplayContext(knowledge_level=1),
        continuation_authority="UNPROVEN",
    )
    assert result.replay_status in {ReplayStatus.BLOCKED, ReplayStatus.PAUSED}
    assert result.violation is not None
    assert result.violation.failure_class == FailureClass.HASH_MISMATCH
    assert result.violation.cryptographic["match"] is False
    assert result.violation.disposition == Disposition.BLOCK
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
    assert result.violation.disposition == Disposition.BLOCK


def test_schema_invalid_layered():
    recorded = evaluate_source(_valid_source())
    recorded.source = None  # type: ignore[assignment]
    result = replay_admission(recorded)
    assert result.violation is not None
    assert result.violation.failure_class == FailureClass.SCHEMA_INVALID
    assert result.violation.execution["side_effects"] == 0


def test_access_limited_not_false_original_decision():
    """Insufficient knowledge → REPLAY_LIMITED_BY_ACCESS_CONTEXT, not CONTEXT_MISMATCH."""
    recorded = evaluate_source(_valid_source())
    result = replay_admission(
        recorded,
        context=ReplayContext(knowledge_level=1),
        required_knowledge_level=3,
    )
    assert result.replay_status == ReplayStatus.REPLAY_LIMITED_BY_ACCESS_CONTEXT
    assert result.violation is None
    limited = [l for l in result.layers if l.layer == "access" and l.status == "LIMITED"]
    assert limited
    assert limited[0].failure_class is None  # limitation ≠ ACCESS_CONTEXT_INVALID tag


def test_context_mismatch_workflow_contradiction_blocks():
    """Supplied context contradicts recorded context → CONTEXT_MISMATCH → BLOCK.

    Distinct from access limitation: actor has enough knowledge but wrong workflow binding.
    """
    recorded = evaluate_source(_valid_source())
    result = replay_admission(
        recorded,
        context=ReplayContext(
            knowledge_level=2,
            workflow_id="wf-B",
            target_boundary="SWI_PRIVILEGED_EXECUTION",
        ),
        recorded_context=RecordedContext(
            workflow_id="wf-A",
            target_boundary="SWI_PRIVILEGED_EXECUTION",
            knowledge_level=2,
        ),
        required_knowledge_level=1,
    )
    assert result.replay_status == ReplayStatus.BLOCKED
    assert result.violation is not None
    assert result.violation.failure_class == FailureClass.CONTEXT_MISMATCH
    assert result.violation.execution["side_effects"] == 0
    assert result.violation.disposition == Disposition.BLOCK
    assert any(l.layer == "context" and l.status == "FAIL" for l in result.layers)


def test_context_mismatch_boundary_contradiction_blocks():
    recorded = evaluate_source(_valid_source())
    result = replay_admission(
        recorded,
        context=ReplayContext(
            knowledge_level=2,
            workflow_id="wf-A",
            target_boundary="DOCUMENTATION_ONLY",
        ),
        recorded_context=RecordedContext(
            workflow_id="wf-A",
            target_boundary="SWI_PRIVILEGED_EXECUTION",
        ),
        required_knowledge_level=1,
    )
    assert result.replay_status == ReplayStatus.BLOCKED
    assert result.violation is not None
    assert result.violation.failure_class == FailureClass.CONTEXT_MISMATCH
    assert result.violation.execution["side_effects"] == 0


def test_matching_recorded_context_allows_replayable():
    recorded = evaluate_source(_valid_source())
    result = replay_admission(
        recorded,
        source_for_reeval=_valid_source(),
        context=ReplayContext(
            knowledge_level=2,
            workflow_id="wf-A",
            target_boundary="SWI_PRIVILEGED_EXECUTION",
        ),
        recorded_context=RecordedContext(
            workflow_id="wf-A",
            target_boundary="SWI_PRIVILEGED_EXECUTION",
        ),
        required_knowledge_level=1,
    )
    assert result.replay_status == ReplayStatus.REPLAYABLE_BOUNDED
    assert result.violation is None


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
