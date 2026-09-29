"""Single gateway: all adapters → quarantine → source admission → demo sink.

AI/API declared_authority is never treated as AUTHORIZED.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from swi_core.external_input.models import ExternalInput, InputState
from swi_core.external_input.quarantine import QuarantineRecord, quarantine
from swi_core.external_input.sink import DemoExecutionSink
from swi_core.source_admission.decision import evaluate_source
from swi_core.source_admission.models import DecisionStatus, SourceDescriptor
from swi_core.source_admission.replay import (
    Disposition,
    FailureClass,
    three_question_disposition,
)


@dataclass
class GatewayResult:
    state: InputState
    input_id: str
    payload_hash: str
    admission_decision: Optional[str] = None
    failure_class: Optional[str] = None
    disposition: Optional[str] = None
    questions: Dict[str, str] = field(default_factory=dict)
    execution: Dict[str, Any] = field(default_factory=dict)
    evidence: Dict[str, Any] = field(default_factory=dict)
    quarantine: Optional[QuarantineRecord] = None


class ExternalInputGateway:
    """PROTOTYPE gateway. Production authorization is NOT claimed."""

    def __init__(self, sink: Optional[DemoExecutionSink] = None) -> None:
        self.sink = sink or DemoExecutionSink()

    def _to_descriptor(self, ext: ExternalInput) -> SourceDescriptor:
        # Map external claim to admission descriptor.
        # declared_authority does NOT set architecture_allowed or provenance.
        return SourceDescriptor(
            source_id=ext.source_id or "",
            origin=ext.origin or "",
            version=ext.declared_version or "0",
            content_hash=ext.payload_hash if len(ext.payload_hash) == 64 else ("0" * 64),
            presented_hash=ext.payload_hash if len(ext.payload_hash) == 64 else ("0" * 64),
            license_id=ext.license_id,
            target_boundary="SWI_PRIVILEGED_EXECUTION",
            provenance_verified=ext.provenance_verified,
            privacy_clear=ext.privacy_clear,
            architecture_allowed=ext.architecture_allowed,
            claimed_authorized=bool(ext.declared_authority),
        )

    def process(self, ext: ExternalInput) -> GatewayResult:
        # Missing identity / provenance
        if not ext.source_id or not str(ext.source_id).strip():
            blocked = self.sink.blocked(ext.input_id, "PROVENANCE_MISSING")
            return GatewayResult(
                state=InputState.BLOCKED,
                input_id=ext.input_id,
                payload_hash=ext.payload_hash or "",
                admission_decision="HALT",
                failure_class="EVIDENCE_INCOMPLETE",
                disposition=Disposition.BLOCK.value,
                questions={
                    "what_failed": "source_id missing",
                    "consequence": "Cannot establish provenance; protected op must not run",
                    "continuation_authority": "UNPROVEN",
                },
                execution=blocked,
            )

        # declared_authority is a claim — never grants CONTINUE without scoped string
        if ext.declared_authority:
            auth_claim = str(ext.declared_authority).strip().upper()
            # AI/API saying APPROVED / SYSTEM OVERRIDE is not scoped authority
            if not (
                auth_claim.startswith("AUTHORIZED:") or auth_claim.startswith("SCOPED:")
            ):
                qrec = quarantine(ext)
                blocked = self.sink.blocked(ext.input_id, "AUTHORITY_UNPROVEN")
                disp = three_question_disposition(
                    what_failed="declared_authority is a claim, not scoped authorization",
                    consequence="AI/API assertion must not become execution authority",
                    continuation_authority="UNPROVEN",
                    failure=FailureClass.AUTHORITY_UNPROVEN,
                )
                return GatewayResult(
                    state=InputState.BLOCKED,
                    input_id=ext.input_id,
                    payload_hash=qrec.payload_hash,
                    admission_decision="HALT",
                    failure_class=FailureClass.AUTHORITY_UNPROVEN.value,
                    disposition=disp.value,
                    questions={
                        "what_failed": "declared_authority is a claim, not scoped authorization",
                        "consequence": "AI/API assertion must not become execution authority",
                        "continuation_authority": "UNPROVEN",
                    },
                    execution=blocked,
                    quarantine=qrec,
                    evidence={
                        "declared_authority": ext.declared_authority,
                        "source_type": ext.source_type.value,
                        "label": "DEMO_PROTOTYPE_NOT_PRODUCTION",
                    },
                )

        qrec = quarantine(ext)
        ext.state = InputState.EVALUATING
        desc = self._to_descriptor(ext)
        # Ensure content_hash is real payload hash (64 hex)
        if len(qrec.payload_hash) == 64:
            desc = SourceDescriptor(
                source_id=desc.source_id,
                origin=desc.origin,
                version=desc.version,
                content_hash=qrec.payload_hash,
                presented_hash=qrec.payload_hash,
                license_id=desc.license_id,
                target_boundary=desc.target_boundary,
                provenance_verified=desc.provenance_verified,
                privacy_clear=desc.privacy_clear,
                architecture_allowed=desc.architecture_allowed,
                claimed_authorized=desc.claimed_authorized,
            )

        record = evaluate_source(desc)
        if record.decision != DecisionStatus.PASS:
            blocked = self.sink.blocked(ext.input_id, record.decision.value)
            ext.state = InputState.HALTED
            return GatewayResult(
                state=InputState.HALTED,
                input_id=ext.input_id,
                payload_hash=qrec.payload_hash,
                admission_decision=record.decision.value,
                failure_class=record.violations[0].violation_id if record.violations else "HALT",
                disposition=Disposition.BLOCK.value,
                questions={
                    "what_failed": "; ".join(v.description for v in record.violations) or "admission HALT",
                    "consequence": "Protected operation must not proceed",
                    "continuation_authority": "UNPROVEN",
                },
                execution=blocked,
                quarantine=qrec,
                evidence={
                    "evidence_hash": record.evidence_hash,
                    "decision_basis": list(record.decision_basis),
                    "label": "DEMO_PROTOTYPE_NOT_PRODUCTION",
                },
            )

        # PASS → demo sink only
        executed = self.sink.execute(ext.input_id, ext.requested_action)
        ext.state = InputState.DEMO_EXECUTED
        return GatewayResult(
            state=InputState.DEMO_EXECUTED,
            input_id=ext.input_id,
            payload_hash=qrec.payload_hash,
            admission_decision=DecisionStatus.PASS.value,
            disposition=Disposition.CONTINUE.value,
            execution=executed,
            quarantine=qrec,
            evidence={
                "evidence_hash": record.evidence_hash,
                "label": "DEMO_PROTOTYPE_NOT_PRODUCTION",
                "real_world_side_effects": 0,
            },
        )
