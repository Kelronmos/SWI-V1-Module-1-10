"""SWI External Source Admission — halt + replay + claim slots + change control.

SPECIFIED → IMPLEMENTED → TESTED (bounded slices).
REPLAYABLE_BOUNDED where adversarial tests demonstrate it.
PROVEN beyond slice / SEALED / regulatory compliance: NOT CLAIMED.
Does not close FM-005–013 or the Universal Gate.
"""

from swi_core.source_admission.change_control import (
    AdmissionRecord,
    ChangeControlResult,
    ComponentState,
    admit_with_history,
    detect_material_change,
)
from swi_core.source_admission.claims import (
    ClaimScopeExpansionError,
    ClaimSlotMap,
    ClaimValue,
    apply_claim_update,
    claim_slots_from_admission_pass,
    default_claim_slots,
)
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
from swi_core.source_admission.open_source import OpenSourceComponent, admit_component
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
    "ClaimValue",
    "ClaimSlotMap",
    "ClaimScopeExpansionError",
    "default_claim_slots",
    "apply_claim_update",
    "claim_slots_from_admission_pass",
    "ComponentState",
    "AdmissionRecord",
    "ChangeControlResult",
    "detect_material_change",
    "admit_with_history",
    "OpenSourceComponent",
    "admit_component",
]
