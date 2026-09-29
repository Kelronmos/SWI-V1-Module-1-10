"""Adversarial tests: claim slots, material change, no silent inheritance, attribution.

Bounded open-source protection slice. Does not close FM-005–013 or claim compliance.
"""
from __future__ import annotations

import pytest

from swi_core.source_admission.claims import (
    ClaimScopeExpansionError,
    ClaimSlotMap,
    ClaimValue,
    apply_claim_update,
    claim_slots_from_admission_pass,
    default_claim_slots,
)
from swi_core.source_admission.change_control import (
    ComponentState,
    admit_with_history,
    detect_material_change,
)
from swi_core.source_admission.models import SourceDescriptor
from swi_core.source_admission.open_source import OpenSourceComponent, admit_component

_H1 = "1" * 64
_H2 = "2" * 64


def _desc(**kw) -> SourceDescriptor:
    base = dict(
        source_id="oss-1",
        origin="https://example.com/lib",
        version="1.0.0",
        content_hash=_H1,
        presented_hash=_H1,
        license_id="Apache-2.0",
        provenance_verified=True,
        privacy_clear=True,
        architecture_allowed=True,
    )
    base.update(kw)
    return SourceDescriptor(**base)


def _state(desc: SourceDescriptor | None = None, **kw) -> ComponentState:
    return ComponentState(descriptor=desc or _desc(), **kw)


def test_claim_expansion_security_to_secure_blocked():
    current = ClaimSlotMap({"security": ClaimValue.TESTED_WITHIN_SCOPE.value})
    with pytest.raises(ClaimScopeExpansionError, match="CLAIM_SCOPE_EXPANSION"):
        apply_claim_update(current, {"security": ClaimValue.SECURE.value})


def test_claim_expansion_legal_compliance_blocked():
    current = ClaimSlotMap({"legal_compliance": ClaimValue.NOT_PROVEN.value})
    with pytest.raises(ClaimScopeExpansionError):
        apply_claim_update(current, {"legal_compliance": ClaimValue.LEGAL_COMPLIANT.value})


def test_claim_expansion_with_evidence_allowed():
    current = ClaimSlotMap({"security": ClaimValue.TESTED_WITHIN_SCOPE.value})
    updated = apply_claim_update(
        current,
        {"security": ClaimValue.SECURE.value},
        evidence_refs={"security": "ev-sec-001"},
    )
    assert updated.get("security") == ClaimValue.SECURE.value


def test_admission_pass_does_not_claim_legal_or_authority():
    slots = claim_slots_from_admission_pass(
        license_id="MIT",
        provenance_verified=True,
        architecture_allowed=True,
    )
    assert slots.get("license") == ClaimValue.IDENTIFIED.value
    assert slots.get("legal_compliance") == ClaimValue.NOT_PROVEN.value
    assert slots.get("authority") == ClaimValue.NOT_CLAIMED.value
    assert slots.get("trust") == ClaimValue.NOT_CLAIMED.value


def test_material_change_version_and_hash():
    s1 = _state(_desc(version="1.0.0", content_hash=_H1))
    s2 = _state(_desc(version="1.1.0", content_hash=_H2, presented_hash=_H2))
    diff = detect_material_change(s1, s2)
    assert diff.material
    assert "version" in diff.changed_fields
    assert "content_hash" in diff.changed_fields


def test_no_silent_inheritance_on_version_bump():
    c1 = OpenSourceComponent(
        component_id="lib",
        origin="https://example.com/lib",
        exact_version="1.0.0",
        content_hash=_H1,
        license_id="MIT",
        provenance_verified=True,
        privacy_clear=True,
        architecture_allowed=True,
    )
    r1 = admit_component(c1)
    assert r1.admitted and r1.record is not None
    a1 = r1.record.admission_id

    c2 = OpenSourceComponent(
        component_id="lib",
        origin="https://example.com/lib",
        exact_version="1.1.0",
        content_hash=_H2,
        license_id="MIT",
        provenance_verified=True,
        privacy_clear=True,
        architecture_allowed=True,
    )
    r2 = admit_component(c2, prior=r1.record, prior_component=c1)
    assert r2.admitted and r2.record is not None
    assert r2.record.admission_id != a1
    assert r2.record.supersedes == a1
    assert r2.record.evidence_hash != r1.record.evidence_hash
    assert "version" in r2.record.changed_fields or "content_hash" in r2.record.changed_fields
    # A1 preserved as prior object
    assert r2.prior is not None and r2.prior.admission_id == a1


def test_notice_missing_blocks_not_legal_verdict():
    c = OpenSourceComponent(
        component_id="lib",
        origin="https://example.com/lib",
        exact_version="1.0.0",
        content_hash=_H1,
        license_id="Apache-2.0",
        notice_present=False,
        provenance_verified=True,
        privacy_clear=True,
        architecture_allowed=True,
    )
    r = admit_component(c)
    assert not r.admitted
    assert "NOTICE_REQUIREMENT_MISSING" in r.obligation_issues
    assert r.blocked_reason == "LICENSE_OBLIGATION_UNVERIFIED"
    assert r.side_effects == 0


def test_terms_hash_change_is_material():
    s1 = _state(terms_hash="t1")
    s2 = _state(terms_hash="t2")
    diff = detect_material_change(s1, s2)
    assert diff.material
    assert "terms_hash" in diff.changed_fields


def test_dependency_fingerprint_change_is_material():
    s1 = _state(dependency_fingerprint="dep-a")
    s2 = _state(dependency_fingerprint="dep-b")
    diff = detect_material_change(s1, s2)
    assert diff.material
    assert "dependency_fingerprint" in diff.changed_fields


def test_blocked_admission_zero_side_effects():
    counter = {"execution_successes": 0}
    bad = _state(_desc(license_id=None))
    r = admit_with_history(bad, side_effect_counter=counter)
    assert not r.admitted
    assert counter["execution_successes"] == 0
    assert r.side_effects == 0
