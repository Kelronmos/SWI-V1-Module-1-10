"""Evidence record + hash for interoperability evaluations.

HASH ≠ AUTHORITY ≠ TRUTH. Used so mutation is detectable on replay.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from swi_core.interoperability.evaluate import EvaluationResult
from swi_core.interoperability.models import WorkflowTemplate


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode(
        "utf-8"
    )


def template_material(tpl: WorkflowTemplate) -> Dict[str, Any]:
    return {
        "workflow_id": tpl.workflow_id,
        "stages": list(tpl.stages),
        "objective": tpl.objective,
        "alternative_providers_known": tpl.alternative_providers_known,
        "switching_path_known": tpl.switching_path_known,
        "single_provider_declared": tpl.single_provider_declared,
        "context_complete": tpl.context_complete,
        "evidence_available": tpl.evidence_available,
        "authority_available": tpl.authority_available,
        "real_world_execution_declared": tpl.real_world_execution_declared,
        "market_allocation_requested": tpl.market_allocation_requested,
        "price_setting_requested": tpl.price_setting_requested,
        "consequence_level": getattr(tpl, "consequence_level", None),
        "execution_mode": getattr(tpl, "execution_mode", None),
        "notes": tpl.notes,
    }


@dataclass
class EvaluationEvidence:
    workflow_id: str
    input_material: Dict[str, Any]
    decision: str
    questions: List[str] = field(default_factory=list)
    basis: List[str] = field(default_factory=list)
    evidence_hash: str = ""

    def recompute_hash(self) -> str:
        body = {
            "workflow_id": self.workflow_id,
            "input_material": self.input_material,
            "decision": self.decision,
            "questions": self.questions,
            "basis": self.basis,
        }
        return hashlib.sha256(_canonical(body)).hexdigest()


def record_evaluation(tpl: WorkflowTemplate, result: EvaluationResult) -> EvaluationEvidence:
    ev = EvaluationEvidence(
        workflow_id=tpl.workflow_id,
        input_material=template_material(tpl),
        decision=result.state.value,
        questions=list(result.questions),
        basis=list(result.basis),
    )
    ev.evidence_hash = ev.recompute_hash()
    return ev


def verify_evidence(ev: EvaluationEvidence) -> str:
    """Return PASS, HASH_MISMATCH, or DECISION_MISMATCH relative to recomputed hash only.

    Decision mismatch vs re-eval is checked by caller after re-evaluate.
    """
    recomputed = ev.recompute_hash()
    if recomputed != ev.evidence_hash:
        return "HASH_MISMATCH"
    return "HASH_OK"
