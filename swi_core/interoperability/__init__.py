"""SWI Interoperable Organization Workflow Template — PROTOTYPE.

Question-driven resolution: UNKNOWN ≠ FALSE · QUESTION ≠ DENY · PASS ≠ authority.
Does not claim Universal Gate, production trust, or regulatory compliance.
"""

from swi_core.interoperability.evaluate import evaluate_workflow
from swi_core.interoperability.models import (
    ResolutionState,
    WorkflowStage,
    WorkflowTemplate,
)

__all__ = [
    "WorkflowStage",
    "ResolutionState",
    "WorkflowTemplate",
    "evaluate_workflow",
]
