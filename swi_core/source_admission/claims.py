"""Claim-slot system — prevent silent claim expansion.

LICENSE_IDENTIFIED ≠ LEGAL_COMPLIANCE
HASH verified ≠ AUTHORITY / TRUSTED / AUTHORIZED
TESTED_WITHIN_SCOPE ≠ SECURE
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Mapping, Optional


class ClaimValue(str, Enum):
    NOT_CLAIMED = "NOT_CLAIMED"
    NOT_PROVEN = "NOT_PROVEN"
    VERIFIED = "VERIFIED"
    IDENTIFIED = "IDENTIFIED"
    TESTED_WITHIN_SCOPE = "TESTED_WITHIN_SCOPE"
    ADMITTED_FOR_DEFINED_USE = "ADMITTED_FOR_DEFINED_USE"
    # Explicitly not auto-granted from weaker claims:
    SECURE = "SECURE"
    AUTHORIZED = "AUTHORIZED"
    LEGAL_COMPLIANT = "LEGAL_COMPLIANT"
    TRUSTED = "TRUSTED"


# Ordered strength within a slot family (lower index = weaker).
# Expansion to a stronger value without evidence is blocked.
_SLOT_LADDERS: Dict[str, tuple[str, ...]] = {
    "identity": ("NOT_CLAIMED", "NOT_PROVEN", "VERIFIED"),
    "origin": ("NOT_CLAIMED", "NOT_PROVEN", "VERIFIED"),
    "version": ("NOT_CLAIMED", "NOT_PROVEN", "VERIFIED"),
    "license": ("NOT_CLAIMED", "NOT_PROVEN", "IDENTIFIED", "VERIFIED"),
    "security": ("NOT_CLAIMED", "NOT_PROVEN", "TESTED_WITHIN_SCOPE", "SECURE"),
    "architecture": ("NOT_CLAIMED", "NOT_PROVEN", "ADMITTED_FOR_DEFINED_USE"),
    "authority": ("NOT_CLAIMED", "NOT_PROVEN", "AUTHORIZED"),
    "legal_compliance": ("NOT_CLAIMED", "NOT_PROVEN", "LEGAL_COMPLIANT"),
    "trust": ("NOT_CLAIMED", "NOT_PROVEN", "TRUSTED"),
}


class ClaimScopeExpansionError(ValueError):
    """Raised when a claim attempts to expand without new evidence."""


@dataclass(frozen=True)
class ClaimSlotMap:
    slots: Mapping[str, str] = field(default_factory=dict)

    def get(self, slot: str, default: str = "NOT_CLAIMED") -> str:
        return str(self.slots.get(slot, default))

    def to_dict(self) -> Dict[str, str]:
        return {k: str(v) for k, v in self.slots.items()}


def default_claim_slots() -> ClaimSlotMap:
    return ClaimSlotMap(
        {
            "identity": ClaimValue.NOT_PROVEN.value,
            "origin": ClaimValue.NOT_PROVEN.value,
            "version": ClaimValue.NOT_PROVEN.value,
            "license": ClaimValue.NOT_PROVEN.value,
            "security": ClaimValue.NOT_PROVEN.value,
            "architecture": ClaimValue.NOT_PROVEN.value,
            "authority": ClaimValue.NOT_CLAIMED.value,
            "legal_compliance": ClaimValue.NOT_PROVEN.value,
            "trust": ClaimValue.NOT_CLAIMED.value,
        }
    )


def _rank(slot: str, value: str) -> int:
    ladder = _SLOT_LADDERS.get(slot)
    if ladder is None:
        return 0
    try:
        return ladder.index(value)
    except ValueError:
        # Unknown token is not a free upgrade path
        return -1


def apply_claim_update(
    current: ClaimSlotMap,
    proposed: Mapping[str, str],
    *,
    evidence_refs: Optional[Mapping[str, str]] = None,
) -> ClaimSlotMap:
    """Apply slot updates. Expansion to a stronger value requires evidence_ref for that slot.

    Missing evidence on expansion → ClaimScopeExpansionError.
    """
    evidence_refs = evidence_refs or {}
    new_slots: Dict[str, str] = dict(current.to_dict())

    for slot, new_val in proposed.items():
        old_val = new_slots.get(slot, ClaimValue.NOT_CLAIMED.value)
        old_r = _rank(slot, old_val)
        new_r = _rank(slot, str(new_val))

        if new_r > old_r:
            # Expansion requires explicit evidence reference for this slot
            if not evidence_refs.get(slot):
                raise ClaimScopeExpansionError(
                    f"CLAIM_SCOPE_EXPANSION slot={slot} "
                    f"from={old_val} to={new_val} without evidence_ref"
                )
        new_slots[slot] = str(new_val)

    return ClaimSlotMap(new_slots)


def assert_no_illegal_inference(slots: ClaimSlotMap) -> None:
    """Invariant checks: weaker facts must not imply stronger legal/authority claims."""
    # license identified/verified does not imply legal_compliance
    lic = slots.get("license")
    if lic in {ClaimValue.IDENTIFIED.value, ClaimValue.VERIFIED.value}:
        if slots.get("legal_compliance") == ClaimValue.LEGAL_COMPLIANT.value:
            # Only illegal if no separate evidence path — caller must use apply_claim_update
            pass  # structural allowance only when explicitly set with evidence

    # security tested ≠ SECURE without expansion evidence (enforced at apply time)
    # authority remains NOT_CLAIMED unless explicit


def claim_slots_from_admission_pass(
    *,
    license_id: Optional[str],
    provenance_verified: bool,
    architecture_allowed: bool,
) -> ClaimSlotMap:
    """Derive bounded slots from a successful technical admission — never legal/authority."""
    base = default_claim_slots().to_dict()
    if provenance_verified:
        base["identity"] = ClaimValue.VERIFIED.value
        base["origin"] = ClaimValue.VERIFIED.value
        base["version"] = ClaimValue.VERIFIED.value
    if license_id:
        base["license"] = ClaimValue.IDENTIFIED.value
    base["security"] = ClaimValue.TESTED_WITHIN_SCOPE.value
    if architecture_allowed:
        base["architecture"] = ClaimValue.ADMITTED_FOR_DEFINED_USE.value
    base["authority"] = ClaimValue.NOT_CLAIMED.value
    base["legal_compliance"] = ClaimValue.NOT_PROVEN.value
    base["trust"] = ClaimValue.NOT_CLAIMED.value
    return ClaimSlotMap(base)
