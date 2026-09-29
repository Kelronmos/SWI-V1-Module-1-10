"""Bounded replay for source admission decisions.

Contract:
  Recorded decision → canonical evidence → evidence_hash H
  → re-run identical checks on the same SourceDescriptor
  → new evidence_hash H → decision identical → REPLAYABLE (bounded)

Does not prove Universal Gate closure, legal compliance, or production-wide
replayability. Does not close FM-005–013.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from swi_core.source_admission.decision import evaluate_source
from swi_core.source_admission.evidence import evidence_hash_for_record
from swi_core.source_admission.models import (
    DecisionStatus,
    SourceAdmissionRecord,
    SourceDescriptor,
)


class ReplayResultStatus(str, Enum):
    REPLAY_OK = "REPLAY_OK"
    REPLAY_INVALID = "REPLAY_INVALID"
    NOT_PROVEN = "NOT_PROVEN"


@dataclass(frozen=True)
class ReplayResult:
    status: ReplayResultStatus
    original_decision: Optional[str]
    replayed_decision: Optional[str]
    original_evidence_hash: Optional[str]
    replayed_evidence_hash: Optional[str]
    reason: str
    limitation: str = (
        "REPLAYABLE within the tested source-admission contract and evidence "
        "format; not proof of Universal Gate closure, legal compliance, or "
        "production-wide replayability."
    )


def replay_admission(
    original: SourceAdmissionRecord,
    *,
    source_override: Optional[SourceDescriptor] = None,
) -> ReplayResult:
    """Re-evaluate from the recorded source (or override) and compare hashes/decisions.

    - If original has no source or no evidence_hash → NOT_PROVEN.
    - If source_override is provided, evaluate that material instead (mutation tests).
    - REPLAY_OK only when decision and evidence_hash both match the original.
    """
    if original is None:
        return ReplayResult(
            status=ReplayResultStatus.NOT_PROVEN,
            original_decision=None,
            replayed_decision=None,
            original_evidence_hash=None,
            replayed_evidence_hash=None,
            reason="MISSING_ORIGINAL_RECORD",
        )

    if original.evidence_hash is None or not str(original.evidence_hash).strip():
        return ReplayResult(
            status=ReplayResultStatus.NOT_PROVEN,
            original_decision=original.decision.value if original.decision else None,
            replayed_decision=None,
            original_evidence_hash=None,
            replayed_evidence_hash=None,
            reason="MISSING_EVIDENCE_HASH",
        )

    # Integrity of the stored hash vs material currently on the record
    recomputed_original = evidence_hash_for_record(original)
    if recomputed_original != original.evidence_hash:
        return ReplayResult(
            status=ReplayResultStatus.REPLAY_INVALID,
            original_decision=original.decision.value,
            replayed_decision=None,
            original_evidence_hash=original.evidence_hash,
            replayed_evidence_hash=recomputed_original,
            reason="EVIDENCE_HASH_TAMPERED",
        )

    src = source_override if source_override is not None else original.source
    if src is None:
        return ReplayResult(
            status=ReplayResultStatus.NOT_PROVEN,
            original_decision=original.decision.value,
            replayed_decision=None,
            original_evidence_hash=original.evidence_hash,
            replayed_evidence_hash=None,
            reason="MISSING_SOURCE_DESCRIPTOR",
        )

    replayed = evaluate_source(src)

    if replayed.decision.value != original.decision.value:
        return ReplayResult(
            status=ReplayResultStatus.REPLAY_INVALID,
            original_decision=original.decision.value,
            replayed_decision=replayed.decision.value,
            original_evidence_hash=original.evidence_hash,
            replayed_evidence_hash=replayed.evidence_hash,
            reason="DECISION_MISMATCH",
        )

    if replayed.evidence_hash != original.evidence_hash:
        return ReplayResult(
            status=ReplayResultStatus.REPLAY_INVALID,
            original_decision=original.decision.value,
            replayed_decision=replayed.decision.value,
            original_evidence_hash=original.evidence_hash,
            replayed_evidence_hash=replayed.evidence_hash,
            reason="EVIDENCE_HASH_MISMATCH",
        )

    return ReplayResult(
        status=ReplayResultStatus.REPLAY_OK,
        original_decision=original.decision.value,
        replayed_decision=replayed.decision.value,
        original_evidence_hash=original.evidence_hash,
        replayed_evidence_hash=replayed.evidence_hash,
        reason="SAME_DECISION_SAME_HASH",
    )
