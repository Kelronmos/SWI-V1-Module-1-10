"""Bounded source-admission replay with layered invalidity and access context.

HASH ≠ AUTHORITY ≠ TRUTH.
A hash match proves byte–digest correspondence for the recorded material.
It does not prove the original decision was true, lawful, or authorized.

Access levels must not magically escalate during replay.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional

from swi_core.source_admission.decision import evaluate_source
from swi_core.source_admission.evidence import evidence_hash_for_record
from swi_core.source_admission.models import (
    DecisionStatus,
    SourceAdmissionRecord,
    SourceDescriptor,
)


class FailureClass(str, Enum):
    SERIALIZATION_INVALID = "SERIALIZATION_INVALID"
    SCHEMA_INVALID = "SCHEMA_INVALID"
    HASH_MISMATCH = "HASH_MISMATCH"
    CRYPTOGRAPHIC_INVALID = "CRYPTOGRAPHIC_INVALID"
    CONTEXT_MISMATCH = "CONTEXT_MISMATCH"
    ACCESS_CONTEXT_INVALID = "ACCESS_CONTEXT_INVALID"
    EVIDENCE_INCOMPLETE = "EVIDENCE_INCOMPLETE"
    DECISION_MISMATCH = "DECISION_MISMATCH"
    SOURCE_MUTATED = "SOURCE_MUTATED"
    AUTHORITY_UNPROVEN = "AUTHORITY_UNPROVEN"


class ReplayStatus(str, Enum):
    REPLAYABLE_BOUNDED = "REPLAYABLE_BOUNDED"
    REPLAY_LIMITED_BY_ACCESS_CONTEXT = "REPLAY_LIMITED_BY_ACCESS_CONTEXT"
    PAUSED = "PAUSED"
    BLOCKED = "BLOCKED"


class Disposition(str, Enum):
    CONTINUE = "CONTINUE"
    BLOCK = "BLOCK"
    ISOLATE = "ISOLATE"
    ESCALATE = "ESCALATE"
    REVALIDATE = "REVALIDATE"


# Knowledge / access levels (conceptual; bounded implementation)
# 0 public · 1 admitted metadata · 2 protected workflow · 3 restricted evidence · 4 execution/authority
KNOWLEDGE_PUBLIC = 0
KNOWLEDGE_ADMITTED_METADATA = 1
KNOWLEDGE_WORKFLOW = 2
KNOWLEDGE_RESTRICTED = 3
KNOWLEDGE_EXECUTION = 4


@dataclass(frozen=True)
class ReplayContext:
    knowledge_level: int = KNOWLEDGE_ADMITTED_METADATA
    access_scope: tuple[str, ...] = ("source_metadata", "admission_evidence")
    restricted_information_used: bool = False


@dataclass
class LayerResult:
    layer: str
    status: str  # PASS | FAIL | LIMITED
    failure_class: Optional[FailureClass] = None
    detail: str = ""


@dataclass
class ViolationReport:
    event: str = "SWI_VIOLATION"
    status: str = "PAUSED"
    failure_class: Optional[FailureClass] = None
    severity: str = "REVIEW_REQUIRED"
    description: str = ""
    cryptographic: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    rules: List[str] = field(default_factory=list)
    questions: dict[str, str] = field(default_factory=dict)
    disposition: Disposition = Disposition.BLOCK
    execution: dict[str, Any] = field(default_factory=lambda: {"continued": False, "side_effects": 0})
    evidence_hash: Optional[str] = None
    layers: List[LayerResult] = field(default_factory=list)


@dataclass
class ReplayResult:
    recorded_decision: str
    recomputed_decision: Optional[str]
    recorded_hash: Optional[str]
    recomputed_hash: Optional[str]
    layers: List[LayerResult]
    replay_status: ReplayStatus
    violation: Optional[ViolationReport] = None
    context: Optional[ReplayContext] = None


def _schema_ok(record: SourceAdmissionRecord) -> LayerResult:
    if record.source is None:
        return LayerResult("schema", "FAIL", FailureClass.SCHEMA_INVALID, "source missing")
    src = record.source
    if not src.source_id or not src.origin or not src.version:
        return LayerResult("schema", "FAIL", FailureClass.SCHEMA_INVALID, "required identity fields missing")
    if not src.content_hash or len(src.content_hash) != 64:
        return LayerResult("schema", "FAIL", FailureClass.SCHEMA_INVALID, "content_hash malformed")
    if record.decision is None:
        return LayerResult("schema", "FAIL", FailureClass.SCHEMA_INVALID, "decision missing")
    return LayerResult("schema", "PASS")


def _serialization_ok(record: SourceAdmissionRecord) -> LayerResult:
    try:
        _ = record.to_evidence_dict()
        return LayerResult("serialization", "PASS")
    except Exception as exc:  # noqa: BLE001 — fail-closed
        return LayerResult(
            "serialization",
            "FAIL",
            FailureClass.SERIALIZATION_INVALID,
            f"canonical reconstruction failed: {type(exc).__name__}",
        )


def _hash_layer(record: SourceAdmissionRecord) -> LayerResult:
    if not record.evidence_hash:
        return LayerResult("hash", "FAIL", FailureClass.EVIDENCE_INCOMPLETE, "recorded evidence_hash missing")
    recomputed = evidence_hash_for_record(record)
    if recomputed != record.evidence_hash:
        return LayerResult(
            "hash",
            "FAIL",
            FailureClass.HASH_MISMATCH,
            "recomputed digest differs from recorded evidence_hash",
        )
    return LayerResult("hash", "PASS")


def _access_layer(ctx: ReplayContext, required_level: int) -> LayerResult:
    if ctx.restricted_information_used and ctx.knowledge_level < KNOWLEDGE_RESTRICTED:
        return LayerResult(
            "access",
            "FAIL",
            FailureClass.ACCESS_CONTEXT_INVALID,
            "restricted information claimed without sufficient knowledge level",
        )
    if ctx.knowledge_level < required_level:
        return LayerResult(
            "access",
            "LIMITED",
            FailureClass.ACCESS_CONTEXT_INVALID,
            f"available knowledge_level={ctx.knowledge_level} < required={required_level}",
        )
    return LayerResult("access", "PASS")


def _build_violation(
    failure: FailureClass,
    description: str,
    *,
    recorded_hash: Optional[str],
    recomputed_hash: Optional[str],
    ctx: ReplayContext,
    layers: List[LayerResult],
    what_failed: str,
    consequence: str,
    continuation_authority: str,
    disposition: Disposition,
) -> ViolationReport:
    return ViolationReport(
        status="PAUSED" if disposition != Disposition.BLOCK else "BLOCKED",
        failure_class=failure,
        severity="REVIEW_REQUIRED",
        description=description,
        cryptographic={
            "recorded_hash": recorded_hash,
            "recomputed_hash": recomputed_hash,
            "match": recorded_hash is not None
            and recomputed_hash is not None
            and recorded_hash == recomputed_hash,
        },
        context={
            "knowledge_level": ctx.knowledge_level,
            "access_scope": list(ctx.access_scope),
            "restricted_information_used": ctx.restricted_information_used,
        },
        rules=[
            "Recorded evidence must remain cryptographically consistent",
            "Missing required evidence must not be treated as approval",
            "Unverified continuation must not execute protected operations",
            "HASH ≠ AUTHORITY ≠ TRUTH",
            "Replay must not escalate knowledge level",
        ],
        questions={
            "what_failed": what_failed,
            "consequence": consequence,
            "continuation_authority": continuation_authority,
        },
        disposition=disposition,
        execution={"continued": False, "side_effects": 0},
        evidence_hash=recorded_hash,
        layers=list(layers),
    )


def three_question_disposition(
    *,
    what_failed: str,
    consequence: str,
    continuation_authority: str,
    failure: FailureClass,
) -> Disposition:
    """CONTINUE only when continuation_authority is demonstrated; else BLOCK/ESCALATE."""
    auth = (continuation_authority or "").strip().upper()
    if auth in {"", "UNPROVEN", "NONE", "NOT_AUTHORIZED", "MISSING"}:
        if failure in {
            FailureClass.ACCESS_CONTEXT_INVALID,
            FailureClass.AUTHORITY_UNPROVEN,
            FailureClass.HASH_MISMATCH,
            FailureClass.SOURCE_MUTATED,
        }:
            return Disposition.BLOCK
        return Disposition.BLOCK
    if auth.startswith("ESCALATE"):
        return Disposition.ESCALATE
    if auth.startswith("ISOLATE"):
        return Disposition.ISOLATE
    if auth.startswith("REVALIDATE"):
        return Disposition.REVALIDATE
    # Explicit scoped authorization string required for CONTINUE
    if auth.startswith("AUTHORIZED:") or auth.startswith("SCOPED:"):
        return Disposition.CONTINUE
    return Disposition.BLOCK


def replay_admission(
    recorded: SourceAdmissionRecord,
    *,
    source_for_reeval: Optional[SourceDescriptor] = None,
    context: Optional[ReplayContext] = None,
    required_knowledge_level: int = KNOWLEDGE_ADMITTED_METADATA,
    continuation_authority: str = "UNPROVEN",
) -> ReplayResult:
    """Replay recorded admission decision under stated access context.

    Does not execute protected operations. On violation: PAUSE/BLOCK report only.
    """
    ctx = context or ReplayContext()
    layers: List[LayerResult] = []

    ser = _serialization_ok(recorded)
    layers.append(ser)
    if ser.status == "FAIL":
        disp = three_question_disposition(
            what_failed=ser.detail,
            consequence="Cannot reconstruct evidence; protected ops must not continue",
            continuation_authority=continuation_authority,
            failure=FailureClass.SERIALIZATION_INVALID,
        )
        report = _build_violation(
            FailureClass.SERIALIZATION_INVALID,
            ser.detail,
            recorded_hash=recorded.evidence_hash,
            recomputed_hash=None,
            ctx=ctx,
            layers=layers,
            what_failed=ser.detail,
            consequence="Cannot reconstruct evidence; protected ops must not continue",
            continuation_authority=continuation_authority,
            disposition=disp,
        )
        return ReplayResult(
            recorded_decision=recorded.decision.value,
            recomputed_decision=None,
            recorded_hash=recorded.evidence_hash,
            recomputed_hash=None,
            layers=layers,
            replay_status=ReplayStatus.BLOCKED if disp == Disposition.BLOCK else ReplayStatus.PAUSED,
            violation=report,
            context=ctx,
        )

    sch = _schema_ok(recorded)
    layers.append(sch)
    if sch.status == "FAIL":
        disp = three_question_disposition(
            what_failed=sch.detail,
            consequence="Malformed evidence must not authorize continuation",
            continuation_authority=continuation_authority,
            failure=FailureClass.SCHEMA_INVALID,
        )
        report = _build_violation(
            FailureClass.SCHEMA_INVALID,
            sch.detail,
            recorded_hash=recorded.evidence_hash,
            recomputed_hash=None,
            ctx=ctx,
            layers=layers,
            what_failed=sch.detail,
            consequence="Malformed evidence must not authorize continuation",
            continuation_authority=continuation_authority,
            disposition=disp,
        )
        return ReplayResult(
            recorded_decision=recorded.decision.value,
            recomputed_decision=None,
            recorded_hash=recorded.evidence_hash,
            recomputed_hash=None,
            layers=layers,
            replay_status=ReplayStatus.BLOCKED if disp == Disposition.BLOCK else ReplayStatus.PAUSED,
            violation=report,
            context=ctx,
        )

    hlayer = _hash_layer(recorded)
    layers.append(hlayer)
    recomputed_hash = evidence_hash_for_record(recorded) if recorded.evidence_hash else None
    if hlayer.status == "FAIL":
        fc = hlayer.failure_class or FailureClass.HASH_MISMATCH
        disp = three_question_disposition(
            what_failed=hlayer.detail,
            consequence="Cryptographic representation differs; do not treat as same evidence",
            continuation_authority=continuation_authority,
            failure=fc,
        )
        report = _build_violation(
            fc,
            hlayer.detail,
            recorded_hash=recorded.evidence_hash,
            recomputed_hash=recomputed_hash,
            ctx=ctx,
            layers=layers,
            what_failed=hlayer.detail,
            consequence="Cryptographic representation differs; do not treat as same evidence",
            continuation_authority=continuation_authority,
            disposition=disp,
        )
        return ReplayResult(
            recorded_decision=recorded.decision.value,
            recomputed_decision=None,
            recorded_hash=recorded.evidence_hash,
            recomputed_hash=recomputed_hash,
            layers=layers,
            replay_status=ReplayStatus.BLOCKED if disp == Disposition.BLOCK else ReplayStatus.PAUSED,
            violation=report,
            context=ctx,
        )

    # Cryptographic binding (bounded: hash integrity only; not signature/CRTG)
    layers.append(LayerResult("cryptographic_binding", "PASS", detail="hash binding only; not CRTG"))

    access = _access_layer(ctx, required_knowledge_level)
    layers.append(access)
    if access.status == "FAIL":
        disp = three_question_disposition(
            what_failed=access.detail,
            consequence="Access boundary exceeded or restricted data used without level",
            continuation_authority=continuation_authority,
            failure=FailureClass.ACCESS_CONTEXT_INVALID,
        )
        report = _build_violation(
            FailureClass.ACCESS_CONTEXT_INVALID,
            access.detail,
            recorded_hash=recorded.evidence_hash,
            recomputed_hash=recomputed_hash,
            ctx=ctx,
            layers=layers,
            what_failed=access.detail,
            consequence="Access boundary exceeded or restricted data used without level",
            continuation_authority=continuation_authority,
            disposition=disp,
        )
        return ReplayResult(
            recorded_decision=recorded.decision.value,
            recomputed_decision=None,
            recorded_hash=recorded.evidence_hash,
            recomputed_hash=recomputed_hash,
            layers=layers,
            replay_status=ReplayStatus.BLOCKED,
            violation=report,
            context=ctx,
        )
    if access.status == "LIMITED":
        # Not automatically a failed original decision — limited by access context
        return ReplayResult(
            recorded_decision=recorded.decision.value,
            recomputed_decision=None,
            recorded_hash=recorded.evidence_hash,
            recomputed_hash=recomputed_hash,
            layers=layers,
            replay_status=ReplayStatus.REPLAY_LIMITED_BY_ACCESS_CONTEXT,
            violation=None,
            context=ctx,
        )

    # Re-evaluation (decision comparison) when source provided
    recomputed_decision: Optional[str] = None
    if source_for_reeval is not None:
        # Detect source mutation vs recorded descriptor
        if recorded.source is not None:
            rs = recorded.source
            if (
                source_for_reeval.source_id != rs.source_id
                or source_for_reeval.content_hash != rs.content_hash
                or source_for_reeval.version != rs.version
            ):
                layers.append(
                    LayerResult(
                        "source",
                        "FAIL",
                        FailureClass.SOURCE_MUTATED,
                        "source identity/hash/version differs from recorded",
                    )
                )
                disp = three_question_disposition(
                    what_failed="SOURCE_MUTATED",
                    consequence="Underlying source changed; prior admission does not transfer",
                    continuation_authority=continuation_authority,
                    failure=FailureClass.SOURCE_MUTATED,
                )
                report = _build_violation(
                    FailureClass.SOURCE_MUTATED,
                    "source identity/hash/version differs from recorded",
                    recorded_hash=recorded.evidence_hash,
                    recomputed_hash=recomputed_hash,
                    ctx=ctx,
                    layers=layers,
                    what_failed="SOURCE_MUTATED",
                    consequence="Underlying source changed; prior admission does not transfer",
                    continuation_authority=continuation_authority,
                    disposition=disp,
                )
                return ReplayResult(
                    recorded_decision=recorded.decision.value,
                    recomputed_decision=None,
                    recorded_hash=recorded.evidence_hash,
                    recomputed_hash=recomputed_hash,
                    layers=layers,
                    replay_status=ReplayStatus.BLOCKED,
                    violation=report,
                    context=ctx,
                )

        fresh = evaluate_source(source_for_reeval)
        recomputed_decision = fresh.decision.value
        if fresh.decision.value != recorded.decision.value:
            layers.append(
                LayerResult(
                    "decision",
                    "FAIL",
                    FailureClass.DECISION_MISMATCH,
                    f"recorded={recorded.decision.value} recomputed={fresh.decision.value}",
                )
            )
            disp = three_question_disposition(
                what_failed="DECISION_MISMATCH",
                consequence="Checks no longer produce the recorded decision",
                continuation_authority=continuation_authority,
                failure=FailureClass.DECISION_MISMATCH,
            )
            report = _build_violation(
                FailureClass.DECISION_MISMATCH,
                f"recorded={recorded.decision.value} recomputed={fresh.decision.value}",
                recorded_hash=recorded.evidence_hash,
                recomputed_hash=recomputed_hash,
                ctx=ctx,
                layers=layers,
                what_failed="DECISION_MISMATCH",
                consequence="Checks no longer produce the recorded decision",
                continuation_authority=continuation_authority,
                disposition=disp,
            )
            return ReplayResult(
                recorded_decision=recorded.decision.value,
                recomputed_decision=recomputed_decision,
                recorded_hash=recorded.evidence_hash,
                recomputed_hash=recomputed_hash,
                layers=layers,
                replay_status=ReplayStatus.BLOCKED,
                violation=report,
                context=ctx,
            )
        layers.append(LayerResult("decision", "PASS"))
    else:
        layers.append(LayerResult("decision", "PASS", detail="reeval skipped; hash+schema only"))

    return ReplayResult(
        recorded_decision=recorded.decision.value,
        recomputed_decision=recomputed_decision or recorded.decision.value,
        recorded_hash=recorded.evidence_hash,
        recomputed_hash=recomputed_hash,
        layers=layers,
        replay_status=ReplayStatus.REPLAYABLE_BOUNDED,
        violation=None,
        context=ctx,
    )
