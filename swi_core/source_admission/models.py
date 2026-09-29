"""Source admission data models.

HASH ≠ AUTHORITY. A recorded hash proves correspondence to content,
not legal permission, safety, or authorization.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional


class DecisionStatus(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    HALT = "HALT"
    NOT_PROVEN = "NOT_PROVEN"


@dataclass(frozen=True)
class Violation:
    violation_id: str
    rule_id: str
    severity: str  # HALT | WARNING
    description: str
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SourceDescriptor:
    """Minimal identity of an external source under evaluation."""

    source_id: str
    origin: str
    version: str
    content_hash: str  # expected SHA-256 hex of content under evaluation
    license_id: Optional[str] = None
    target_boundary: str = "SWI_PRIVILEGED_EXECUTION"
    # Optional flags used by checks (fail-closed when missing where required)
    provenance_verified: bool = False
    privacy_clear: bool = False
    architecture_allowed: bool = False
    # Actual hash of material presented (for mismatch detection)
    presented_hash: Optional[str] = None
    # Forged-authority attack surface: must never auto-admit
    claimed_authorized: bool = False


@dataclass
class SourceAdmissionRecord:
    schema_version: str = "swi-source-admission-v1"
    source: Optional[SourceDescriptor] = None
    violations: List[Violation] = field(default_factory=list)
    warnings: List[Violation] = field(default_factory=list)
    decision: DecisionStatus = DecisionStatus.NOT_PROVEN
    decision_basis: List[str] = field(default_factory=list)
    evidence_hash: Optional[str] = None
    status: str = "NOT_PROVEN"  # record-level honesty, not a seal

    def to_evidence_dict(self) -> dict[str, Any]:
        """Canonical material for hashing (no free-form approved:true)."""
        src = self.source
        return {
            "schema_version": self.schema_version,
            "source_id": src.source_id if src else None,
            "origin": src.origin if src else None,
            "version": src.version if src else None,
            "content_hash": src.content_hash if src else None,
            "license_id": src.license_id if src else None,
            "target_boundary": src.target_boundary if src else None,
            "violations": [
                {
                    "violation_id": v.violation_id,
                    "rule_id": v.rule_id,
                    "severity": v.severity,
                    "description": v.description,
                }
                for v in self.violations
            ],
            "warnings": [
                {
                    "violation_id": v.violation_id,
                    "rule_id": v.rule_id,
                    "severity": v.severity,
                    "description": v.description,
                }
                for v in self.warnings
            ],
            "decision": self.decision.value,
            "decision_basis": list(self.decision_basis),
            "status": self.status,
        }
