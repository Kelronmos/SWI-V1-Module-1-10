"""Material-change detection and admission history — no silent inheritance.

Component v1 / H1 / A1 → v1.1 / H2 requires A2; A1 is preserved, not rewritten.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence

from swi_core.source_admission.claims import ClaimSlotMap, claim_slots_from_admission_pass
from swi_core.source_admission.decision import evaluate_source
from swi_core.source_admission.models import DecisionStatus, SourceDescriptor


MATERIAL_FIELDS = (
    "source_id",
    "version",
    "content_hash",
    "license_id",
    "origin",
    "provenance_verified",
    "privacy_clear",
    "architecture_allowed",
    "target_boundary",
    "notice_present",
    "copyright_present",
    "attribution_present",
    "dependency_fingerprint",
)


@dataclass(frozen=True)
class ComponentState:
    """Snapshot used for change detection (extends SourceDescriptor dimensions)."""

    descriptor: SourceDescriptor
    notice_present: bool = True
    copyright_present: bool = True
    attribution_present: bool = True
    dependency_fingerprint: str = ""  # opaque hash of resolved deps
    terms_hash: str = ""

    def material_dict(self) -> Dict[str, Any]:
        d = self.descriptor
        return {
            "source_id": d.source_id,
            "version": d.version,
            "content_hash": d.content_hash,
            "license_id": d.license_id,
            "origin": d.origin,
            "provenance_verified": d.provenance_verified,
            "privacy_clear": d.privacy_clear,
            "architecture_allowed": d.architecture_allowed,
            "target_boundary": d.target_boundary,
            "notice_present": self.notice_present,
            "copyright_present": self.copyright_present,
            "attribution_present": self.attribution_present,
            "dependency_fingerprint": self.dependency_fingerprint,
            "terms_hash": self.terms_hash,
        }


@dataclass
class ChangeDiff:
    changed_fields: List[str]
    material: bool

    @property
    def empty(self) -> bool:
        return not self.changed_fields


def detect_material_change(before: ComponentState, after: ComponentState) -> ChangeDiff:
    b, a = before.material_dict(), after.material_dict()
    changed = [k for k in MATERIAL_FIELDS if b.get(k) != a.get(k)]
    # terms_hash also material
    if b.get("terms_hash") != a.get("terms_hash") and "terms_hash" not in changed:
        if b.get("terms_hash") or a.get("terms_hash"):
            changed.append("terms_hash")
    return ChangeDiff(changed_fields=changed, material=bool(changed))


@dataclass
class AdmissionRecord:
    admission_id: str
    source_version: str
    source_hash: str
    evidence_hash: str
    decision: str
    claim_slots: Dict[str, str]
    supersedes: Optional[str] = None
    changed_fields: List[str] = field(default_factory=list)
    attribution: Dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "admission_id": self.admission_id,
            "source_version": self.source_version,
            "source_hash": self.source_hash,
            "evidence_hash": self.evidence_hash,
            "decision": self.decision,
            "claim_slots": dict(self.claim_slots),
            "supersedes": self.supersedes,
            "changed_fields": list(self.changed_fields),
            "attribution": dict(self.attribution),
        }


def _admission_id(prefix: str, payload: Dict[str, Any]) -> str:
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode(
        "utf-8"
    )
    return f"{prefix}-{hashlib.sha256(blob).hexdigest()[:16]}"


def check_attribution(state: ComponentState) -> List[str]:
    """Return obligation issue codes — not legal adjudications."""
    issues: List[str] = []
    if not state.notice_present:
        issues.append("NOTICE_REQUIREMENT_MISSING")
    if not state.copyright_present:
        issues.append("ATTRIBUTION_REQUIREMENT_UNVERIFIED")  # copyright notice missing
    if not state.attribution_present:
        issues.append("ATTRIBUTION_REQUIREMENT_MISSING")
    return issues


@dataclass
class ChangeControlResult:
    admitted: bool
    record: Optional[AdmissionRecord]
    prior: Optional[AdmissionRecord]
    diff: Optional[ChangeDiff]
    obligation_issues: List[str] = field(default_factory=list)
    blocked_reason: Optional[str] = None
    side_effects: int = 0


def admit_with_history(
    state: ComponentState,
    *,
    prior: Optional[AdmissionRecord] = None,
    prior_state: Optional[ComponentState] = None,
    side_effect_counter: Optional[Dict[str, int]] = None,
) -> ChangeControlResult:
    """Evaluate component; never silently inherit prior admission after material change.

    If prior exists and material change detected, prior is kept as history via supersedes.
    Attribution obligation gaps → BLOCK (engineering state, not legal verdict).
    """
    # Attribution obligations
    obligations = check_attribution(state)
    if obligations:
        return ChangeControlResult(
            admitted=False,
            record=None,
            prior=prior,
            diff=None,
            obligation_issues=obligations,
            blocked_reason="LICENSE_OBLIGATION_UNVERIFIED",
            side_effects=0,
        )

    # Policy evaluation (existing engine)
    eval_record = evaluate_source(state.descriptor)
    if eval_record.decision != DecisionStatus.PASS:
        return ChangeControlResult(
            admitted=False,
            record=None,
            prior=prior,
            diff=None,
            obligation_issues=[],
            blocked_reason=f"ADMISSION_{eval_record.decision.value}",
            side_effects=0,
        )

    diff: Optional[ChangeDiff] = None
    supersedes: Optional[str] = None
    changed: List[str] = []

    if prior is not None and prior_state is not None:
        diff = detect_material_change(prior_state, state)
        if diff.material:
            # Cannot inherit prior admission id / evidence
            supersedes = prior.admission_id
            changed = list(diff.changed_fields)
            # If someone tried to keep prior evidence_hash, that would be silent inherit — we always mint new
        else:
            # Non-material: still mint new record but may note no change
            supersedes = prior.admission_id

    slots = claim_slots_from_admission_pass(
        license_id=state.descriptor.license_id,
        provenance_verified=state.descriptor.provenance_verified,
        architecture_allowed=state.descriptor.architecture_allowed,
    )

    payload = {
        "version": state.descriptor.version,
        "content_hash": state.descriptor.content_hash,
        "license_id": state.descriptor.license_id,
        "evidence_hash": eval_record.evidence_hash,
        "decision": eval_record.decision.value,
        "slots": slots.to_dict(),
        "changed": changed,
        "supersedes": supersedes,
    }
    aid = _admission_id("A", payload)

    new_rec = AdmissionRecord(
        admission_id=aid,
        source_version=state.descriptor.version,
        source_hash=state.descriptor.content_hash,
        evidence_hash=eval_record.evidence_hash or "",
        decision=eval_record.decision.value,
        claim_slots=slots.to_dict(),
        supersedes=supersedes,
        changed_fields=changed,
        attribution={
            "notice_present": state.notice_present,
            "copyright_present": state.copyright_present,
            "attribution_present": state.attribution_present,
        },
    )

    # Invariant: new admission must not equal prior admission_id after material change
    if prior is not None and diff is not None and diff.material:
        if new_rec.admission_id == prior.admission_id:
            return ChangeControlResult(
                admitted=False,
                record=None,
                prior=prior,
                diff=diff,
                blocked_reason="SILENT_INHERITANCE_REJECTED",
                side_effects=0,
            )
        if new_rec.evidence_hash == prior.evidence_hash and "content_hash" in changed:
            return ChangeControlResult(
                admitted=False,
                record=None,
                prior=prior,
                diff=diff,
                blocked_reason="EVIDENCE_HASH_NOT_REFRESHED",
                side_effects=0,
            )

    if side_effect_counter is not None:
        side_effect_counter["execution_successes"] = side_effect_counter.get("execution_successes", 0) + 1

    return ChangeControlResult(
        admitted=True,
        record=new_rec,
        prior=prior,
        diff=diff,
        obligation_issues=[],
        blocked_reason=None,
        side_effects=0,
    )
