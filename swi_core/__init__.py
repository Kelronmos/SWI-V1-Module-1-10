"""SWI Core — Structured Workflow Intelligence reference implementation.

Development status: alpha (see package version 0.1.0a1).
This is not a claim that Universal Gate is proven or Module 00–10 are sealed.

Security primitives are required exports (fail closed — no soft ImportError fallback).
"""

from .admission_boundary import (
    AdmissionDecision,
    evaluate_claim,
    issue_admission_decision,
    is_module_sealed,
)
from .module_kernel import (
    AdmissionRequiredError,
    CheckResult,
    ModuleKernel,
    ModuleKernelError,
)
from .security_maze import (
    AccessState,
    GateId,
    GateOutcome,
    MazeRun,
    SecurityMaze,
    MAZE_VERSION,
)

__version__ = "0.1.0a1"

__all__ = [
    "AccessState",
    "AdmissionDecision",
    "AdmissionRequiredError",
    "CheckResult",
    "GateId",
    "GateOutcome",
    "MAZE_VERSION",
    "MazeRun",
    "ModuleKernel",
    "ModuleKernelError",
    "SecurityMaze",
    "evaluate_claim",
    "issue_admission_decision",
    "is_module_sealed",
    "__version__",
]
