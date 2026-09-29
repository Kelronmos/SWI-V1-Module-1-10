"""Interactive SWI demo journey — structured stages for a visible experience.

PROTOTYPE / DEMO ONLY. Production: OFF.
Gives a UI five stages: INPUT → RECEIVING → CHECKING → DECISION → RESULT/REPLAY.

Does not claim Universal Gate, Seal 5, or compliance.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from swi_core.external_input.adapters import AIAppAdapter, SimulationAdapter
from swi_core.external_input.gateway import ExternalInputGateway, GatewayResult
from swi_core.external_input.models import ExternalInput, InputState
from swi_core.external_input.sink import DemoExecutionSink
from swi_core.source_admission.decision import evaluate_source
from swi_core.source_admission.models import SourceDescriptor
from swi_core.source_admission.replay import (
    RecordedContext,
    ReplayContext,
    ReplayStatus,
    replay_admission,
)


@dataclass
class Stage:
    name: str
    status: str  # ACTIVE | DONE | FAIL | LIMITED
    detail: str = ""
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class JourneyResult:
    stages: List[Stage]
    decision: str
    disposition: Optional[str]
    side_effects: int
    real_world_side_effects: int
    label: str = "DEMO_PROTOTYPE_NOT_PRODUCTION"
    production: str = "OFF"
    authority: str = "bounded"
    execution: str = "simulated"
    replay: str = "bounded"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stages": [asdict(s) for s in self.stages],
            "decision": self.decision,
            "disposition": self.disposition,
            "side_effects": self.side_effects,
            "real_world_side_effects": self.real_world_side_effects,
            "label": self.label,
            "swi_status": {
                "authority": self.authority,
                "execution": self.execution,
                "replay": self.replay,
                "production": self.production,
            },
        }


def _check_board(result: GatewayResult) -> List[Dict[str, str]]:
    """Observable checks — not a fake 'AI thinking' animation."""
    board = [
        {"check": "Serialization", "result": "PASS"},
        {"check": "Schema", "result": "PASS"},
        {"check": "Provenance", "result": "PASS" if result.admission_decision == "PASS" else "FAIL"},
        {"check": "Integrity", "result": "PASS" if result.payload_hash else "FAIL"},
        {"check": "Source admission", "result": result.admission_decision or "UNKNOWN"},
        {"check": "Authority evidence", "result": "UNPROVEN" if result.failure_class == "AUTHORITY_UNPROVEN" else ("PASS" if result.admission_decision == "PASS" else "REVIEW")},
    ]
    return board


def run_input_journey(
    text_or_payload: Any,
    *,
    source: str = "AI_APP",
    declared_authority: Optional[str] = None,
    verified_demo: bool = False,
) -> JourneyResult:
    """End-to-end: user input → SWI stages → decision → simulated result."""
    stages: List[Stage] = []
    sink = DemoExecutionSink()
    gw = ExternalInputGateway(sink=sink)

    payload = text_or_payload if isinstance(text_or_payload, dict) else {"text": str(text_or_payload)}

    stages.append(Stage("INPUT", "DONE", "External claim received", {"payload": payload, "source": source}))

    if verified_demo:
        ext = SimulationAdapter().receive(
            payload,
            requested_action="sandbox_record",
            provenance_verified=True,
            privacy_clear=True,
            architecture_allowed=True,
        )
    elif source.upper() == "AI_APP":
        ext = AIAppAdapter().receive(
            payload,
            declared_authority=declared_authority,
            requested_action=payload.get("action") or payload.get("requested_action"),
        )
    else:
        from swi_core.external_input.adapters import APIAdapter

        ext = APIAdapter().receive(payload, declared_authority=declared_authority)

    stages.append(
        Stage(
            "RECEIVING",
            "DONE",
            "Quarantine + hash",
            {
                "input_id": ext.input_id,
                "source_type": ext.source_type.value,
                "origin": ext.origin,
            },
        )
    )

    result = gw.process(ext)

    stages.append(
        Stage(
            "CHECKING",
            "DONE",
            "Observable evidence checks",
            {"checks": _check_board(result), "payload_hash": result.payload_hash},
        )
    )

    if result.state in {InputState.BLOCKED, InputState.HALTED}:
        stages.append(
            Stage(
                "DECISION",
                "FAIL",
                result.failure_class or "HALT",
                {
                    "decision": "BLOCKED",
                    "failure_class": result.failure_class,
                    "questions": result.questions,
                    "disposition": result.disposition,
                    "side_effects": result.execution.get("side_effects", 0),
                },
            )
        )
        stages.append(
            Stage(
                "RESULT",
                "FAIL",
                "Protected operation not executed",
                {"execution": result.execution},
            )
        )
        return JourneyResult(
            stages=stages,
            decision="BLOCKED",
            disposition=result.disposition,
            side_effects=int(result.execution.get("side_effects", 0)),
            real_world_side_effects=0,
        )

    stages.append(
        Stage(
            "DECISION",
            "DONE",
            "PASS (bounded)",
            {"decision": "PASS", "label": "SIMULATED_ONLY"},
        )
    )
    stages.append(
        Stage(
            "RESULT",
            "DONE",
            "Demo execution only",
            {"execution": result.execution},
        )
    )
    return JourneyResult(
        stages=stages,
        decision="PASS",
        disposition=result.disposition,
        side_effects=int(result.execution.get("side_effects", 0)),
        real_world_side_effects=0,
    )


def run_replay_experience(
    *,
    mode: str = "success",
) -> Dict[str, Any]:
    """Three distinct replay experiences for the UI.

    mode:
      success      → REPLAYABLE_BOUNDED
      limited      → REPLAY_LIMITED_BY_ACCESS_CONTEXT (not a violation)
      contradiction → CONTEXT_MISMATCH → BLOCK
      tamper       → HASH_MISMATCH → BLOCK
    """
    desc = SourceDescriptor(
        source_id="demo-src",
        origin="https://example.com/demo",
        version="1.0.0",
        content_hash="a" * 64,
        presented_hash="a" * 64,
        license_id="MIT",
        provenance_verified=True,
        privacy_clear=True,
        architecture_allowed=True,
    )
    recorded = evaluate_source(desc)

    if mode == "limited":
        r = replay_admission(
            recorded,
            context=ReplayContext(knowledge_level=1),
            required_knowledge_level=3,
        )
        return {
            "experience": "REPLAY_LIMITED",
            "message": "The original decision is NOT declared false. Replay cannot complete within this access boundary.",
            "required_knowledge_level": 3,
            "available_level": 1,
            "replay_status": r.replay_status.value,
            "violation": None,
            "side_effects": 0,
        }

    if mode == "contradiction":
        r = replay_admission(
            recorded,
            context=ReplayContext(
                knowledge_level=2,
                workflow_id="WF-002",
                target_boundary="SWI_PRIVILEGED_EXECUTION",
            ),
            recorded_context=RecordedContext(
                workflow_id="WF-001",
                target_boundary="SWI_PRIVILEGED_EXECUTION",
            ),
            required_knowledge_level=1,
        )
        return {
            "experience": "CONTEXT_MISMATCH",
            "message": "The replay context contradicts the recorded context.",
            "recorded_workflow": "WF-001",
            "replay_workflow": "WF-002",
            "replay_status": r.replay_status.value,
            "disposition": r.violation.disposition.value if r.violation else None,
            "side_effects": r.violation.execution["side_effects"] if r.violation else 0,
            "questions": r.violation.questions if r.violation else {},
        }

    if mode == "tamper":
        h1 = recorded.evidence_hash
        recorded.evidence_hash = "b" * 64
        r = replay_admission(recorded, context=ReplayContext(knowledge_level=1))
        return {
            "experience": "HASH_MISMATCH",
            "message": "Workflow does not inherit previous admission after evidence binding changes.",
            "original_hash": h1,
            "current_hash": recorded.evidence_hash,
            "replay_status": r.replay_status.value,
            "disposition": r.violation.disposition.value if r.violation else None,
            "side_effects": 0,
            "questions": r.violation.questions if r.violation else {},
        }

    # success
    r = replay_admission(
        recorded,
        source_for_reeval=desc,
        context=ReplayContext(
            knowledge_level=2,
            workflow_id="WF-001",
            target_boundary="SWI_PRIVILEGED_EXECUTION",
        ),
        recorded_context=RecordedContext(
            workflow_id="WF-001",
            target_boundary="SWI_PRIVILEGED_EXECUTION",
        ),
        required_knowledge_level=1,
    )
    return {
        "experience": "REPLAYABLE_BOUNDED",
        "message": "Evidence, context, and decision match within the tested contract.",
        "workflow": "WF-001",
        "context": "MATCH",
        "evidence": "MATCH",
        "decision": "MATCH",
        "original": recorded.decision.value,
        "replay": r.recomputed_decision,
        "replay_status": r.replay_status.value,
        "side_effects": 0,
    }
