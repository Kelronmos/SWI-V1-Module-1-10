"""SWI External Source Admission — bounded enforcement + replay slice.

SPECIFIED → IMPLEMENTED → TESTED (halt slice + replay slice).
REPLAYABLE_BOUNDED claimed only where adversarial tests demonstrate it.
PROVEN beyond slice / SEALED / regulatory compliance: NOT CLAIMED.
Does not close FM-005–013 or the Universal Gate.
"""

from swi_core.source_admission.decision import evaluate_source
from swi_core.source_admission.evidence import evidence_hash_for_record
from swi_core.source_admission.halt import (
    SourceAdmissionHalt,
    admit_or_halt,
    guarded_operation,
)
from swi_core.source_admission.models import (
    DecisionStatus,
    SourceAdmissionRecord,
    SourceDescriptor,
    Violation,
)
from swi_core.source_admission.replay import (
    Disposition,
    FailureClass,
    ReplayContext,
    ReplayResult,
    ReplayStatus,
    ViolationReport,
    replay_admission,
    three_question_disposition,
)

__all__ = [
    "DecisionStatus",
    "SourceAdmissionRecord",
    "SourceDescriptor",
    "Violation",
    "SourceAdmissionHalt",
    "evaluate_source",
    "admit_or_halt",
    "guarded_operation",
    "evidence_hash_for_record",
    "FailureClass",
    "ReplayStatus",
    "Disposition",
    "ReplayContext",
    "ReplayResult",
    "ViolationReport",
    "replay_admission",
    "three_question_disposition",
]
