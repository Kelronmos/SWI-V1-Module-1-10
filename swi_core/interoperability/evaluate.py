"""Evaluate workflow template with question-driven resolution.

UNKNOWN remains UNKNOWN. Market/price control → BLOCK.
Real-world execution without authority → AUTHORITY_REQUIRED.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from swi_core.interoperability.models import (
    REQUIRED_STAGES,
    ResolutionState,
    WorkflowStage,
    WorkflowTemplate,
)


@dataclass
class EvaluationResult:
    state: ResolutionState
    questions: List[str] = field(default_factory=list)
    basis: List[str] = field(default_factory=list)
    workflow_id: str = ""
    real_execution: bool = False
    side_effects: int = 0


def evaluate_workflow(tpl: WorkflowTemplate) -> EvaluationResult:
    wid = tpl.workflow_id

    # Market / price control — prototype must not become market engine
    if tpl.market_allocation_requested:
        return EvaluationResult(
            state=ResolutionState.BLOCK,
            basis=["market_allocation_requested — prototype governs transitions, not markets"],
            workflow_id=wid,
            real_execution=False,
            side_effects=0,
        )
    if tpl.price_setting_requested:
        return EvaluationResult(
            state=ResolutionState.BLOCK,
            basis=["price_setting_requested — prototype does not set prices"],
            workflow_id=wid,
            real_execution=False,
            side_effects=0,
        )

    # Stage completeness
    present = {s.upper() for s in tpl.stages}
    missing = [s.value for s in REQUIRED_STAGES if s.value not in present]
    if missing:
        return EvaluationResult(
            state=ResolutionState.QUESTION_REQUIRED,
            questions=[f"Missing stages: {', '.join(missing)}"],
            basis=["STAGE_EXISTS ≠ STAGE_PASSED; incomplete template"],
            workflow_id=wid,
            side_effects=0,
        )

    if not tpl.context_complete:
        return EvaluationResult(
            state=ResolutionState.CONTEXT_REQUIRED,
            questions=["Which organizational boundary and actors complete this workflow context?"],
            workflow_id=wid,
            side_effects=0,
        )

    if not tpl.evidence_available:
        return EvaluationResult(
            state=ResolutionState.EVIDENCE_REQUIRED,
            questions=["What evidence establishes the claims in this workflow?"],
            workflow_id=wid,
            side_effects=0,
        )

    # Real-world execution needs established authority — claim is not enough
    if tpl.real_world_execution_declared and not tpl.authority_available:
        return EvaluationResult(
            state=ResolutionState.AUTHORITY_REQUIRED,
            questions=["What evidence establishes authority for real-world execution?"],
            basis=["DECLARED ≠ ESTABLISHED authority"],
            workflow_id=wid,
            real_execution=False,
            side_effects=0,
        )

    # UNKNOWN alternatives → QUESTION, not zero
    if tpl.alternative_providers_known is None:
        return EvaluationResult(
            state=ResolutionState.QUESTION_REQUIRED,
            questions=["How many alternative providers are established by evidence?"],
            basis=["UNKNOWN ≠ 0; do not manufacture evidence"],
            workflow_id=wid,
            side_effects=0,
        )

    if tpl.switching_path_known is None:
        return EvaluationResult(
            state=ResolutionState.QUESTION_REQUIRED,
            questions=["Is a switching path established by evidence?"],
            basis=["UNKNOWN ≠ impossible"],
            workflow_id=wid,
            side_effects=0,
        )

    if tpl.switching_path_known is False:
        return EvaluationResult(
            state=ResolutionState.REVIEW_REQUIRED,
            questions=["Switching path not established — human/governance review required"],
            basis=["REVIEW ≠ FAILURE; condition detected, not automatic illegality"],
            workflow_id=wid,
            side_effects=0,
        )

    if tpl.single_provider_declared and tpl.alternative_providers_known == 0:
        return EvaluationResult(
            state=ResolutionState.REVIEW_REQUIRED,
            questions=["Single provider with zero known alternatives — review required"],
            basis=["REVIEW_REQUIRED, not automatic BLOCK"],
            workflow_id=wid,
            side_effects=0,
        )

    # Authority still required if real-world declared (already handled) or always for PASS scope
    if not tpl.authority_available and tpl.real_world_execution_declared:
        return EvaluationResult(
            state=ResolutionState.AUTHORITY_REQUIRED,
            workflow_id=wid,
            side_effects=0,
        )

    return EvaluationResult(
        state=ResolutionState.PASS,
        basis=["PASS_WITHIN_PROTOTYPE_SCOPE — not universal authority"],
        workflow_id=wid,
        real_execution=False,
        side_effects=0,
    )
