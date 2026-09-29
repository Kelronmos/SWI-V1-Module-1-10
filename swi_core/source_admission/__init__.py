"""SWI External Source Admission — bounded enforcement + replay slice.

Progression for this package:
  SPECIFIED → IMPLEMENTED → TESTED → REPLAYABLE (bounded).
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
    ReplayResult,
    ReplayResultStatus,
    replay_admission,
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
    "ReplayResult",
    "ReplayResultStatus",
    "replay_admission",
]
