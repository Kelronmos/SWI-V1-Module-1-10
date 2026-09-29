"""Adversarial tests for 14-stage interoperability template.

UNKNOWN ≠ FALSE · QUESTION ≠ DENY · REVIEW ≠ FAILURE · PASS ≠ authority.
"""
from __future__ import annotations

from swi_core.interoperability import ResolutionState, WorkflowStage, evaluate_workflow
from swi_core.interoperability.models import WorkflowTemplate

ALL_STAGES = [s.value for s in WorkflowStage]


def _complete(**kw) -> WorkflowTemplate:
    base = dict(
        workflow_id="wf-demo",
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
    )
    base.update(kw)
    return WorkflowTemplate(**base)


def test_complete_workflow_pass_scoped():
    r = evaluate_workflow(_complete())
    assert r.state == ResolutionState.PASS
    assert r.real_execution is False
    assert r.side_effects == 0
    assert "PROTOTYPE" in ";".join(r.basis).upper() or "SCOPE" in ";".join(r.basis).upper()


def test_missing_stage_question_required():
    r = evaluate_workflow(_complete(stages=["IDENTIFY", "BOUNDARY"]))
    assert r.state == ResolutionState.QUESTION_REQUIRED
    assert r.side_effects == 0


def test_unknown_alternatives_not_zero():
    r = evaluate_workflow(_complete(alternative_providers_known=None))
    assert r.state == ResolutionState.QUESTION_REQUIRED
    assert any("alternative" in q.lower() for q in r.questions)


def test_unknown_switching_question():
    r = evaluate_workflow(_complete(switching_path_known=None))
    assert r.state == ResolutionState.QUESTION_REQUIRED


def test_no_switching_review_not_block():
    r = evaluate_workflow(_complete(switching_path_known=False))
    assert r.state == ResolutionState.REVIEW_REQUIRED
    assert r.state != ResolutionState.BLOCK


def test_single_provider_review():
    r = evaluate_workflow(
        _complete(single_provider_declared=True, alternative_providers_known=0)
    )
    assert r.state == ResolutionState.REVIEW_REQUIRED


def test_real_world_without_authority():
    r = evaluate_workflow(
        _complete(real_world_execution_declared=True, authority_available=False)
    )
    assert r.state == ResolutionState.AUTHORITY_REQUIRED
    assert r.real_execution is False
    assert r.side_effects == 0


def test_market_allocation_block():
    r = evaluate_workflow(_complete(market_allocation_requested=True))
    assert r.state == ResolutionState.BLOCK
    assert r.side_effects == 0


def test_price_setting_block():
    r = evaluate_workflow(_complete(price_setting_requested=True))
    assert r.state == ResolutionState.BLOCK


def test_context_required():
    r = evaluate_workflow(_complete(context_complete=False))
    assert r.state == ResolutionState.CONTEXT_REQUIRED


def test_evidence_required():
    r = evaluate_workflow(_complete(evidence_available=False))
    assert r.state == ResolutionState.EVIDENCE_REQUIRED
