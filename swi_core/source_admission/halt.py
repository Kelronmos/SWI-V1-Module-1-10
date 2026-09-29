"""HALT enforcement: decision must block protected operation (zero side-effect).

Decision layer ≠ execution enforcement. Both are required for a TESTED claim.
"""
from __future__ import annotations

from typing import Any, Callable, Optional, TypeVar

from swi_core.source_admission.decision import evaluate_source
from swi_core.source_admission.models import (
    DecisionStatus,
    SourceAdmissionRecord,
    SourceDescriptor,
)

T = TypeVar("T")


class SourceAdmissionHalt(RuntimeError):
    """Raised when source admission decides HALT. Operation must not proceed."""

    def __init__(self, record: SourceAdmissionRecord) -> None:
        self.record = record
        ids = [v.violation_id for v in record.violations]
        super().__init__(
            f"SOURCE_ADMISSION_HALT decision={record.decision.value} "
            f"violations={ids} evidence_hash={record.evidence_hash}"
        )


def admit_or_halt(source: SourceDescriptor) -> SourceAdmissionRecord:
    """Evaluate source; raise SourceAdmissionHalt on HALT. Return record on PASS.

    WARNING is treated as non-admission for protected operations (fail-closed).
    """
    record = evaluate_source(source)
    if record.decision != DecisionStatus.PASS:
        raise SourceAdmissionHalt(record)
    return record


def guarded_operation(
    source: SourceDescriptor,
    operation: Callable[[], T],
    *,
    side_effect_counter: Optional[dict[str, int]] = None,
) -> tuple[SourceAdmissionRecord, T]:
    """Run operation only after PASS. On HALT, operation is not called.

    If side_effect_counter is provided, tests can assert it was not incremented
    when HALT is raised (zero prohibited side-effects).
    """
    record = evaluate_source(source)
    if record.decision != DecisionStatus.PASS:
        # Do not call operation — this is the enforcement property under test.
        raise SourceAdmissionHalt(record)

    result = operation()
    if side_effect_counter is not None:
        side_effect_counter["execution_successes"] = (
            side_effect_counter.get("execution_successes", 0) + 1
        )
        side_effect_counter["side_effects"] = (
            side_effect_counter.get("side_effects", 0) + 1
        )
    return record, result
