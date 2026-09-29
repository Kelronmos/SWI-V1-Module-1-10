"""External input is a claim/candidate — not an instruction with authority."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class InputSourceType(str, Enum):
    API = "API"
    AI_APP = "AI_APP"
    WEBHOOK = "WEBHOOK"
    SIMULATION = "SIMULATION"


class InputState(str, Enum):
    RECEIVED = "RECEIVED"
    QUARANTINED = "QUARANTINED"
    EVALUATING = "EVALUATING"
    ADMITTED = "ADMITTED"
    HALTED = "HALTED"
    BLOCKED = "BLOCKED"
    DEMO_EXECUTED = "DEMO_EXECUTED"


@dataclass
class ExternalInput:
    input_id: str
    source_type: InputSourceType
    source_id: str
    origin: str
    payload: Dict[str, Any]
    received_at: str = ""
    payload_hash: str = ""
    serialization_version: str = "canonical_json_v1"
    declared_version: str = "1.0"
    # Claim only — must never auto-become AUTHORIZED
    declared_authority: Optional[str] = None
    requested_action: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    state: InputState = InputState.RECEIVED
    # Admission mapping hints (sandbox may supply verified flags for demo PASS cases)
    provenance_verified: bool = False
    privacy_clear: bool = False
    architecture_allowed: bool = False
    license_id: Optional[str] = "MIT"
