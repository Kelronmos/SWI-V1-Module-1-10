"""14-stage interoperable workflow template — stages exist ≠ stages passed."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class WorkflowStage(str, Enum):
    IDENTIFY = "IDENTIFY"
    BOUNDARY = "BOUNDARY"
    CONTRACT = "CONTRACT"
    INPUT = "INPUT"
    ADMISSION = "ADMISSION"
    POLICY = "POLICY"
    CAPACITY = "CAPACITY"
    COMPETITION = "COMPETITION"
    ALTERNATIVES = "ALTERNATIVES"
    SWITCHING = "SWITCHING"
    EXECUTION = "EXECUTION"
    EVIDENCE = "EVIDENCE"
    REVIEW = "REVIEW"
    EXIT = "EXIT"


REQUIRED_STAGES: tuple[WorkflowStage, ...] = tuple(WorkflowStage)


class ResolutionState(str, Enum):
    QUESTION_REQUIRED = "QUESTION_REQUIRED"
    EVIDENCE_REQUIRED = "EVIDENCE_REQUIRED"
    CONTEXT_REQUIRED = "CONTEXT_REQUIRED"
    AUTHORITY_REQUIRED = "AUTHORITY_REQUIRED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    PASS = "PASS"
    HALT = "HALT"
    BLOCK = "BLOCK"


@dataclass
class WorkflowTemplate:
    workflow_id: str
    stages: List[str] = field(default_factory=list)
    objective: str = ""
    organizations: List[Dict[str, Any]] = field(default_factory=list)

    # Explicit None = UNKNOWN — never silently coerce to 0/False for evidence
    alternative_providers_known: Optional[int] = None
    switching_path_known: Optional[bool] = None
    single_provider_declared: bool = False

    context_complete: bool = False
    evidence_available: bool = False
    authority_available: bool = False

    real_world_execution_declared: bool = False
    market_allocation_requested: bool = False
    price_setting_requested: bool = False

    notes: str = ""
