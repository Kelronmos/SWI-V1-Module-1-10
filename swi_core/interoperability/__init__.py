"""SWI Interoperable Organization Workflow Template — PROTOTYPE.

Question-driven resolution: UNKNOWN ≠ FALSE · QUESTION ≠ DENY · PASS ≠ authority.
Does not claim Universal Gate, production trust, or regulatory compliance.
"""

from swi_core.interoperability.evaluate import EvaluationResult, evaluate_workflow
from swi_core.interoperability.evidence import (
    EvaluationEvidence,
    record_evaluation,
    verify_evidence,
)
from swi_core.interoperability.models import (
    ResolutionState,
    WorkflowStage,
    WorkflowTemplate,
)

__all__ = [
    "WorkflowStage",
    "ResolutionState",
    "WorkflowTemplate",
    "EvaluationResult",
    "evaluate_workflow",
    "EvaluationEvidence",
    "record_evaluation",
    "verify_evidence",
]
