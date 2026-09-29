"""Interoperability Mutation & Replay Verification Suite.

Invariant: EVIDENCE_CHANGED → OLD DECISION ≠ AUTOMATICALLY VALID.
Bounded prototype claim only. Universal Gate / production / compliance NOT CLAIMED.
"""
from __future__ import annotations

from copy import deepcopy

from swi_core.interoperability import (
    ResolutionState,
    WorkflowStage,
    evaluate_workflow,
    record_evaluation,
    verify_evidence,
)
from swi_core.interoperability.models import WorkflowTemplate

ALL_STAGES = [s.value for s in WorkflowStage]


def _complete(**kw) -> WorkflowTemplate:
    base = dict(
        workflow_id="wf-mut",
        stages=list(ALL_STAGES),
        context_complete=True,
        evidence_available=True,
        authority_available=True,
        alternative_providers_known=2,
        switching_path_known=True,
        single_provider_declared=False,
        real_world_execution_declared=False,
        market_allocation_requested=False,
        price_setting_requested=False,
        consequence_level="C2",
        execution_mode="SIMULATION",
    )
    base.update(kw)
    return WorkflowTemplate(**base)


def _record_pass():
    tpl = _complete()
    result = evaluate_workflow(tpl)
    assert result.state == ResolutionState.PASS
    ev = record_evaluation(tpl, result)
    assert verify_evidence(ev) == "HASH_OK"
    return tpl, result, ev


def test_mutated_required_stage_cannot_reuse_pass():
    tpl, original, ev = _record_pass()
    mutated = _complete(stages=["IDENTIFY", "BOUNDARY"])  # missing stages
    fresh = evaluate_workflow(mutated)
    assert original.state == ResolutionState.PASS
    assert fresh.state == ResolutionState.QUESTION_REQUIRED
    assert fresh.state != original.state  # old PASS does not survive


def test_provider_change_invalidates_previous_evaluation():
    tpl, original, ev = _record_pass()
    # Change provider count (material input change)
    mutated = _complete(alternative_providers_known=5)
    fresh = evaluate_workflow(mutated)
    fresh_ev = record_evaluation(mutated, fresh)
    # Decision may still be PASS, but evidence identity must differ
    assert fresh_ev.evidence_hash != ev.evidence_hash
    assert fresh_ev.input_material["alternative_providers_known"] == 5


def test_missing_alternative_evidence_requires_question():
    _, original, _ = _record_pass()
    mutated = _complete(alternative_providers_known=None)
    fresh = evaluate_workflow(mutated)
    assert original.state == ResolutionState.PASS
    assert fresh.state == ResolutionState.QUESTION_REQUIRED


def test_switching_path_change_requires_re_evaluation():
    _, original, _ = _record_pass()
    mutated_none = _complete(switching_path_known=None)
    assert evaluate_workflow(mutated_none).state == ResolutionState.QUESTION_REQUIRED
    mutated_false = _complete(switching_path_known=False)
    assert evaluate_workflow(mutated_false).state == ResolutionState.REVIEW_REQUIRED
    assert original.state == ResolutionState.PASS


def test_authority_mutation_invalidates_authority_status():
    _, original, _ = _record_pass()
    mutated = _complete(
        real_world_execution_declared=True,
        authority_available=False,
    )
    fresh = evaluate_workflow(mutated)
    assert original.state == ResolutionState.PASS
    assert fresh.state == ResolutionState.AUTHORITY_REQUIRED
    assert fresh.real_execution is False
    assert fresh.side_effects == 0


def test_consequence_change_requires_re_evaluation():
    tpl, original, ev = _record_pass()
    mutated = _complete(consequence_level="C5")
    fresh = evaluate_workflow(mutated)
    fresh_ev = record_evaluation(mutated, fresh)
    # Prototype evaluator does not auto-BLOCK C5 yet — but evidence must change
    assert fresh_ev.evidence_hash != ev.evidence_hash
    assert fresh_ev.input_material["consequence_level"] == "C5"
    # Old PASS record is not the same evidence identity
    assert original.state == ResolutionState.PASS


def test_runtime_mode_change_invalidates_binding():
    _, original, ev = _record_pass()
    mutated = _complete(execution_mode="ADVISORY_ONLY")
    fresh = evaluate_workflow(mutated)
    fresh_ev = record_evaluation(mutated, fresh)
    assert fresh_ev.evidence_hash != ev.evidence_hash
    assert fresh_ev.input_material["execution_mode"] == "ADVISORY_ONLY"
    # Decision must not silently transfer as same evidence
    assert ev.input_material["execution_mode"] == "SIMULATION"


def test_decision_mutation_detected_on_replay():
    tpl, original, ev = _record_pass()
    # Tamper stored decision after hashing
    ev.decision = ResolutionState.BLOCK.value
    assert verify_evidence(ev) == "HASH_MISMATCH"
    # Re-eval of original input still PASS — DECISION_MISMATCH vs tampered record
    reeval = evaluate_workflow(tpl)
    assert reeval.state == ResolutionState.PASS
    assert reeval.state.value != ev.decision


def test_serialized_evidence_mutation_detected():
    _, _, ev = _record_pass()
    # Mutate serialized input material after hash was sealed
    ev.input_material = dict(ev.input_material)
    ev.input_material["alternative_providers_known"] = 99
    assert verify_evidence(ev) == "HASH_MISMATCH"


def test_input_mutation_cannot_reuse_previous_decision():
    tpl, original, ev = _record_pass()
    # Completely different workflow id / objective
    other = _complete(workflow_id="wf-other", objective="different")
    other_result = evaluate_workflow(other)
    other_ev = record_evaluation(other, other_result)
    assert other_ev.evidence_hash != ev.evidence_hash
    # Cannot treat other_ev as proof of original PASS identity
    assert other_ev.workflow_id != ev.workflow_id
    assert original.state == ResolutionState.PASS
