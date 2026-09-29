"""Adversarial tests: source-policy violation → HALT → zero prohibited side-effects.

Bounded claim only:
  IMPLEMENTED + TESTED for this vertical slice.
  Does not close FM-005–013, Universal Gate, or Foundation Seal 5.
  Does not claim regulatory compliance or REPLAYABLE yet.
"""
from __future__ import annotations

import pytest

from swi_core.source_admission import (
    DecisionStatus,
    SourceAdmissionHalt,
    SourceDescriptor,
    admit_or_halt,
    evaluate_source,
    guarded_operation,
)

_VALID_HASH = "a" * 64
_OTHER_HASH = "b" * 64


def _valid_source(**overrides) -> SourceDescriptor:
    base = dict(
        source_id="src-valid-001",
        origin="https://example.com/org/repo",
        version="1.0.0",
        content_hash=_VALID_HASH,
        presented_hash=_VALID_HASH,
        license_id="Apache-2.0",
        target_boundary="SWI_PRIVILEGED_EXECUTION",
        provenance_verified=True,
        privacy_clear=True,
        architecture_allowed=True,
        claimed_authorized=False,
    )
    base.update(overrides)
    return SourceDescriptor(**base)


def test_valid_source_passes():
    record = evaluate_source(_valid_source())
    assert record.decision == DecisionStatus.PASS
    assert record.evidence_hash is not None
    assert len(record.evidence_hash) == 64
    assert not record.violations


def test_valid_source_guarded_operation_runs_once():
    counter = {"execution_successes": 0, "side_effects": 0}

    def op():
        return "ok"

    record, result = guarded_operation(_valid_source(), op, side_effect_counter=counter)
    assert result == "ok"
    assert record.decision == DecisionStatus.PASS
    assert counter["execution_successes"] == 1
    assert counter["side_effects"] == 1


def test_unknown_provenance_halts_zero_side_effects():
    counter = {"execution_successes": 0, "side_effects": 0}
    src = _valid_source(provenance_verified=False)

    with pytest.raises(SourceAdmissionHalt) as ei:
        guarded_operation(src, lambda: "should-not-run", side_effect_counter=counter)

    assert ei.value.record.decision == DecisionStatus.HALT
    assert any(v.rule_id.startswith("OSS-PROVENANCE") for v in ei.value.record.violations)
    assert counter["execution_successes"] == 0
    assert counter["side_effects"] == 0


def test_hash_mismatch_halts_zero_side_effects():
    counter = {"execution_successes": 0, "side_effects": 0}
    src = _valid_source(presented_hash=_OTHER_HASH)

    with pytest.raises(SourceAdmissionHalt) as ei:
        guarded_operation(src, lambda: "should-not-run", side_effect_counter=counter)

    assert ei.value.record.decision == DecisionStatus.HALT
    assert any(v.violation_id == "SWI-SRC-INTEGRITY-002" for v in ei.value.record.violations)
    assert counter["execution_successes"] == 0
    assert counter["side_effects"] == 0


def test_license_unknown_halts_zero_side_effects():
    counter = {"execution_successes": 0, "side_effects": 0}
    src = _valid_source(license_id=None)

    with pytest.raises(SourceAdmissionHalt) as ei:
        guarded_operation(src, lambda: "should-not-run", side_effect_counter=counter)

    assert ei.value.record.decision == DecisionStatus.HALT
    assert any(v.rule_id == "OSS-LICENSE-001" for v in ei.value.record.violations)
    assert counter["execution_successes"] == 0
    assert counter["side_effects"] == 0


def test_license_incompatible_halts_zero_side_effects():
    counter = {"execution_successes": 0, "side_effects": 0}
    src = _valid_source(license_id="UNKNOWN-COPYLEFT-X")

    with pytest.raises(SourceAdmissionHalt) as ei:
        guarded_operation(src, lambda: "should-not-run", side_effect_counter=counter)

    assert ei.value.record.decision == DecisionStatus.HALT
    assert any(v.rule_id == "OSS-LICENSE-002" for v in ei.value.record.violations)
    assert counter["execution_successes"] == 0
    assert counter["side_effects"] == 0


def test_architecture_fail_halts_zero_side_effects():
    counter = {"execution_successes": 0, "side_effects": 0}
    src = _valid_source(architecture_allowed=False)

    with pytest.raises(SourceAdmissionHalt) as ei:
        guarded_operation(src, lambda: "should-not-run", side_effect_counter=counter)

    assert ei.value.record.decision == DecisionStatus.HALT
    assert any(v.rule_id == "ARCH-001" for v in ei.value.record.violations)
    assert counter["execution_successes"] == 0
    assert counter["side_effects"] == 0


def test_privacy_fail_halts_zero_side_effects():
    counter = {"execution_successes": 0, "side_effects": 0}
    src = _valid_source(privacy_clear=False)

    with pytest.raises(SourceAdmissionHalt) as ei:
        guarded_operation(src, lambda: "should-not-run", side_effect_counter=counter)

    assert ei.value.record.decision == DecisionStatus.HALT
    assert any(v.rule_id == "PRIVACY-001" for v in ei.value.record.violations)
    assert counter["execution_successes"] == 0
    assert counter["side_effects"] == 0


def test_forged_authority_cannot_bypass_violations():
    counter = {"execution_successes": 0, "side_effects": 0}
    src = _valid_source(
        provenance_verified=False,
        claimed_authorized=True,
    )

    with pytest.raises(SourceAdmissionHalt) as ei:
        guarded_operation(src, lambda: "should-not-run", side_effect_counter=counter)

    assert ei.value.record.decision == DecisionStatus.HALT
    assert any(v.rule_id == "AUTH-001" for v in ei.value.record.violations)
    assert counter["execution_successes"] == 0
    assert counter["side_effects"] == 0


def test_admit_or_halt_raises_on_halt():
    with pytest.raises(SourceAdmissionHalt):
        admit_or_halt(_valid_source(license_id=None))


def test_admit_or_halt_returns_record_on_pass():
    record = admit_or_halt(_valid_source())
    assert record.decision == DecisionStatus.PASS


def test_evidence_hash_stable_for_same_material():
    a = evaluate_source(_valid_source())
    b = evaluate_source(_valid_source())
    assert a.evidence_hash == b.evidence_hash
