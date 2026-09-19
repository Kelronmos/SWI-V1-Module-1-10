"""Security Maze V1 — controlled admission / containment around SWI transitions.

Uses the existing micro-kernel (ModuleKernel) and admission_boundary.
This is an *internal* SWI workflow layer, not a separate security product.

Status: CONSTRUCTION / PARTIALLY IMPLEMENTED — NOT SEALED.
Universal Gate remains NOT PROVEN while residual ModuleKernel(False)
and direct module APIs can form state outside this maze.

Governing principle:
  No validated path → no privileged access.
  approved / seal / signature / hash / module / prior admission are INPUTS,
  never bypasses around the maze.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional, Sequence

from .admission_boundary import evaluate_claim, issue_admission_decision
from .module_kernel import AdmissionRequiredError, CheckResult, ModuleKernel

MAZE_VERSION = "security-maze-v1"


class GateId(str, Enum):
    G0_ENTRY = "G0_ENTRY"
    G1_IDENTITY = "G1_IDENTITY"
    G2_STRUCTURE = "G2_STRUCTURE"
    G3_PROVENANCE = "G3_PROVENANCE"
    G4_INTEGRITY = "G4_INTEGRITY"
    G5_AUTHORITY = "G5_AUTHORITY"
    G6_BOUNDARY = "G6_BOUNDARY"
    G7_REPLAY = "G7_REPLAY"
    G8_EVIDENCE = "G8_EVIDENCE"


class GateOutcome(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_RUN = "NOT_RUN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class AccessState(str, Enum):
    UNVALIDATED = "UNVALIDATED"
    VALIDATING = "VALIDATING"
    SANDBOXED = "SANDBOXED"
    ADMITTED = "ADMITTED"
    EXECUTING = "EXECUTING"
    HALTED = "HALTED"


ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    AccessState.UNVALIDATED.value: {AccessState.VALIDATING.value},
    AccessState.VALIDATING.value: {
        AccessState.ADMITTED.value,
        AccessState.SANDBOXED.value,
        AccessState.HALTED.value,
    },
    AccessState.SANDBOXED.value: {
        AccessState.VALIDATING.value,
        AccessState.HALTED.value,
    },
    AccessState.ADMITTED.value: {AccessState.EXECUTING.value},
    AccessState.EXECUTING.value: {AccessState.HALTED.value},
    AccessState.HALTED.value: set(),
}

# SM-V1-001 .. SM-V1-010 (executable names; enforcement is partial)
INVARIANTS = (
    "SM-V1-001",  # unvalidated → no privileged access
    "SM-V1-002",  # sandboxed → no privileged access
    "SM-V1-003",  # retry does not create authority
    "SM-V1-004",  # imported admission revalidated
    "SM-V1-005",  # modified admitted input cannot reuse admission
    "SM-V1-006",  # evidence corruption → contain/halt
    "SM-V1-007",  # privileged paths maze-protected or explicit CONSTRUCTION
    "SM-V1-008",  # temporary bridges cannot bypass maze
    "SM-V1-009",  # failed gate cannot become PASS; NOT_RUN ≠ PASS
    "SM-V1-010",  # decision reproducible under documented env
)


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


@dataclass(frozen=True)
class GateEvidence:
    gate: str
    result: str
    reason: str
    input_hash: str
    previous_evidence_hash: Optional[str]
    state_before: str
    state_after: str
    evidence_hash: str


@dataclass
class MazeRun:
    """One deterministic maze traversal. Does not grant execution by itself."""

    maze_run_id: str
    maze_version: str
    implementation_commit: Optional[str]
    input_hash: str
    state: str = AccessState.UNVALIDATED.value
    gates: list[GateEvidence] = field(default_factory=list)
    decision: str = "PENDING"
    privileged_access: bool = False
    execution_allowed: bool = False
    retry_count: int = 0
    claim_result: Optional[dict[str, Any]] = None

    def record_gate(
        self,
        gate: GateId,
        result: GateOutcome,
        reason: str,
        state_before: str,
        state_after: str,
        input_hash: str,
    ) -> GateEvidence:
        prev = self.gates[-1].evidence_hash if self.gates else None
        payload = {
            "gate": gate.value,
            "result": result.value,
            "reason": reason,
            "input_hash": input_hash,
            "previous_evidence_hash": prev,
            "state_before": state_before,
            "state_after": state_after,
        }
        ev = GateEvidence(
            gate=gate.value,
            result=result.value,
            reason=reason,
            input_hash=input_hash,
            previous_evidence_hash=prev,
            state_before=state_before,
            state_after=state_after,
            evidence_hash=_sha256(payload),
        )
        self.gates.append(ev)
        return ev


def transition(state: str, new_state: str) -> None:
    allowed = ALLOWED_TRANSITIONS.get(state, set())
    if new_state not in allowed:
        raise AdmissionRequiredError(
            f"INVALID_STATE_TRANSITION:{state}->{new_state}"
        )


class SecurityMaze:
    """Security Maze V1 runner.

    Claim path: evaluate_claim (existing anti-overclaim checks).
    Formation path: ModuleKernel(require_admission=True) — micro-kernel choke.

    Default ModuleKernel in production modules remains require_admission=False;
    this class does not rewrite those callers. Universal Gate stays NOT PROVEN.
    """

    def __init__(
        self,
        *,
        implementation_commit: Optional[str] = None,
        seal_records: Optional[Mapping[str, Any]] = None,
        module_id: str = "00",
    ) -> None:
        self.implementation_commit = implementation_commit
        self.seal_records = dict(seal_records or {})
        self.module_id = module_id
        # Micro-kernel: strict admission for maze-controlled formation only
        self._formation_kernel = ModuleKernel(
            name="security-maze-formation",
            require_admission=True,
            module_id=module_id,
            expected_commit=implementation_commit,
        )

    def start_run(self, request: Mapping[str, Any], maze_run_id: str = "MR-local") -> MazeRun:
        ih = _sha256(dict(request))
        return MazeRun(
            maze_run_id=maze_run_id,
            maze_version=MAZE_VERSION,
            implementation_commit=self.implementation_commit,
            input_hash=ih,
            state=AccessState.UNVALIDATED.value,
        )

    def evaluate_request(
        self,
        request: Mapping[str, Any],
        *,
        maze_run_id: str = "MR-local",
        admission: Any = None,
        operation: Optional[Any] = None,
    ) -> MazeRun:
        """Run G0–G8 against a claim-like request; optional strict formation.

        If operation is provided, formation is attempted only after claim PASS
        and only via ModuleKernel(require_admission=True).
        """
        run = self.start_run(request, maze_run_id=maze_run_id)
        transition(run.state, AccessState.VALIDATING.value)
        run.state = AccessState.VALIDATING.value

        ih = run.input_hash

        # G0 — entry (observation only)
        run.record_gate(
            GateId.G0_ENTRY,
            GateOutcome.PASS,
            "MAZE_ENTRY_ESTABLISHED",
            AccessState.UNVALIDATED.value,
            AccessState.VALIDATING.value,
            ih,
        )

        # G1 — identity
        module = request.get("module") or request.get("module_id")
        if module is None and not request.get("request_id"):
            run.record_gate(
                GateId.G1_IDENTITY,
                GateOutcome.FAIL,
                "IDENTITY_MISSING",
                run.state,
                AccessState.SANDBOXED.value,
                ih,
            )
            return self._sandbox(run, "IDENTITY_MISSING")
        run.record_gate(
            GateId.G1_IDENTITY,
            GateOutcome.PASS,
            "IDENTITY_PRESENT",
            run.state,
            run.state,
            ih,
        )

        # G2–G5 / provenance / integrity / authority via evaluate_claim
        claim_result = evaluate_claim(
            request,
            seal_records=self.seal_records,
            current_commit=self.implementation_commit,
        )
        run.claim_result = claim_result

        if not claim_result.get("ok"):
            reason = str(claim_result.get("reason") or "CLAIM_REJECTED")
            # Map reason class to gate for evidence (best-effort)
            gate = GateId.G5_AUTHORITY
            if reason.startswith("UPSTREAM") or "PROVENANCE" in reason or "SYNTHETIC" in reason:
                gate = GateId.G3_PROVENANCE
            elif "HASH" in reason or "COMMIT" in reason or "SEAL" in reason:
                gate = GateId.G4_INTEGRITY
            elif reason in (
                "CLAIM_NOT_A_MAPPING",
                "MODULE_ID_NOT_A_STRING",
                "MODULE_ID_EMPTY",
                "STATUS_NOT_A_STRING",
                "UNKNOWN_STATUS_TOKEN",
            ):
                gate = GateId.G2_STRUCTURE
            run.record_gate(
                gate,
                GateOutcome.FAIL,
                reason,
                run.state,
                AccessState.SANDBOXED.value,
                ih,
            )
            # Mark later gates NOT_RUN (SM-V1-009)
            for g in (
                GateId.G6_BOUNDARY,
                GateId.G7_REPLAY,
                GateId.G8_EVIDENCE,
            ):
                if g.value not in {x.gate for x in run.gates}:
                    run.record_gate(
                        g,
                        GateOutcome.NOT_RUN,
                        "SKIPPED_AFTER_FAILURE",
                        run.state,
                        AccessState.SANDBOXED.value,
                        ih,
                    )
            return self._sandbox(run, reason)

        # Claim ok → structure/provenance/integrity/authority section passed
        for g, note in (
            (GateId.G2_STRUCTURE, "STRUCTURE_OK"),
            (GateId.G3_PROVENANCE, "PROVENANCE_OK_OR_ABSENT"),
            (GateId.G4_INTEGRITY, "INTEGRITY_CHECKS_OK"),
            (GateId.G5_AUTHORITY, "AUTHORITY_CLAIM_ONLY_OR_ADMISSIBLE"),
        ):
            run.record_gate(g, GateOutcome.PASS, note, run.state, run.state, ih)

        # G6 — boundary: claim-only never grants privileged formation without admission
        action = claim_result.get("action")
        if action == "ACCEPT_CLAIM_ONLY" and operation is not None and admission is None:
            run.record_gate(
                GateId.G6_BOUNDARY,
                GateOutcome.FAIL,
                "CLAIM_ONLY_NO_FORMATION_WITHOUT_ADMISSION",
                run.state,
                AccessState.SANDBOXED.value,
                ih,
            )
            return self._sandbox(run, "CLAIM_ONLY_NO_FORMATION_WITHOUT_ADMISSION")

        run.record_gate(
            GateId.G6_BOUNDARY,
            GateOutcome.PASS,
            "BOUNDARY_OK",
            run.state,
            run.state,
            ih,
        )

        # G7 — replay placeholder: commit binding already in evaluate_claim when provided
        run.record_gate(
            GateId.G7_REPLAY,
            GateOutcome.PASS,
            "REPLAY_CHECKS_DEFERRED_OR_OK",
            run.state,
            run.state,
            ih,
        )

        # G8 — evidence: require claim ok + gate trail
        if not run.gates:
            run.record_gate(
                GateId.G8_EVIDENCE,
                GateOutcome.FAIL,
                "NO_GATE_EVIDENCE",
                run.state,
                AccessState.SANDBOXED.value,
                ih,
            )
            return self._sandbox(run, "NO_GATE_EVIDENCE")

        run.record_gate(
            GateId.G8_EVIDENCE,
            GateOutcome.PASS,
            "EVIDENCE_TRAIL_PRESENT",
            run.state,
            run.state,
            ih,
        )

        # Optional privileged formation only via strict micro-kernel
        if operation is not None:
            try:
                self._formation_kernel.run(
                    request,
                    operation,
                    admission=admission,
                )
            except AdmissionRequiredError as exc:
                run.record_gate(
                    GateId.G6_BOUNDARY,
                    GateOutcome.FAIL,
                    str(exc),
                    run.state,
                    AccessState.SANDBOXED.value,
                    ih,
                )
                return self._sandbox(run, str(exc))

        transition(run.state, AccessState.ADMITTED.value)
        run.state = AccessState.ADMITTED.value
        run.decision = "ADMITTED"
        # Claim-only still has no execution authority unless admission was valid
        if admission is not None and getattr(admission, "execution_authority", False):
            run.privileged_access = True
            run.execution_allowed = True
        else:
            run.privileged_access = False
            run.execution_allowed = False
            run.decision = "ADMITTED_CLAIM_ONLY"
        return run

    def _sandbox(self, run: MazeRun, reason: str) -> MazeRun:
        transition(run.state, AccessState.SANDBOXED.value)
        run.state = AccessState.SANDBOXED.value
        run.decision = "SANDBOXED"
        run.privileged_access = False
        run.execution_allowed = False
        run.claim_result = run.claim_result or {"ok": False, "reason": reason}
        return run

    def retry_does_not_grant_authority(self, run: MazeRun) -> MazeRun:
        """SM-V1-003: increment retry without raising privilege."""
        run.retry_count += 1
        run.privileged_access = False
        run.execution_allowed = False
        if run.state != AccessState.SANDBOXED.value:
            # stay sandboxed / halted only
            if run.state not in (
                AccessState.HALTED.value,
                AccessState.SANDBOXED.value,
            ):
                run.state = AccessState.SANDBOXED.value
                run.decision = "SANDBOXED"
        return run


def issue_maze_admission(
    claim: Mapping[str, Any],
    *,
    seal_records: Optional[Mapping[str, Any]] = None,
    current_commit: Optional[str] = None,
    grant_execution: bool = False,
):
    """Thin wrapper: maze uses the same admission issuer as the core boundary."""
    return issue_admission_decision(
        claim,
        seal_records=seal_records,
        current_commit=current_commit,
        grant_execution=grant_execution,
    )
