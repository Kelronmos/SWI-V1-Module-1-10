"""
Module 00: The Trainer (The Master Orchestrator)

Kernel contract failures on Module 03, 02, 05, or 06 STOP the pipeline.
M07 normal-path integrity failures and M09 integrity/persistence failures
also STOP (ModuleKernelError).
Halt recording remains best-effort and never converts failure into success.

Admission: Trainer.process requires keyword-only admission (AdmissionDecision
shape: object with is_valid_for(module, commit)) before any state formation
(turn counter, module calls, M07/M09 writes).
There is no admission=None production fallback.

_record_halt is only reachable after admission has succeeded (post-admission
kernel/integrity failures). Pre-admission rejection performs no M07/M09 writes.

This does not gate direct module APIs (scan/redact/…); Universal Gate is
not proven for those residual surfaces.
"""
from __future__ import annotations
import datetime as _dt
from dataclasses import dataclass
from typing import Any, Optional

from .config_loader import load_config
from .module02_security_probe import SecurityProbe, ProbeResult
from .module03_context_sync import ContextSync, SyncResult
from .module05_redaction_engine import RedactionEngine, RedactionResult
from .module06_drift_analyzer import DriftAnalyzer, DriftResult
from .module07_memory_validator import MemoryValidator
from .module09_audit_logger import AuditLogger
from .module_kernel import AdmissionRequiredError, ModuleKernelError

# Pipeline module identity for admission binding
TRAINER_MODULE_ID = "00"


@dataclass
class PipelineResult:
    allowed: bool
    reason: Optional[str]
    security: Optional[ProbeResult]
    sync: SyncResult
    redaction: Optional[RedactionResult]
    drift: Optional[DriftResult]


class Trainer:
    """Module 00: orchestrates Modules 02, 03, 05, 06, 07, 09 into one pipeline."""

    def __init__(
        self,
        audit_log_path: str,
        config_path: Optional[str] = None,
        *,
        expected_commit: Optional[str] = None,
    ):
        self.config = load_config(config_path)
        self.security = SecurityProbe(
            block_threshold=self.config.get("security_probe", "block_threshold")
        )
        self.sync = ContextSync(
            staleness_seconds=self.config.get("context_sync", "staleness_seconds")
        )
        self.redaction = RedactionEngine()
        self.drift = DriftAnalyzer(
            drift_threshold=self.config.get("drift_analyzer", "drift_threshold")
        )
        self.memory = MemoryValidator()
        self.audit = AuditLogger(audit_log_path)
        self._turn_counter = 0
        self.expected_commit = expected_commit

    def _require_admission(self, admission: Any) -> None:
        """Fail closed before any pipeline formation."""
        if admission is None:
            raise AdmissionRequiredError(
                "Trainer.process: STATE_FORMATION_WITHOUT_ADMISSION"
            )
        is_valid = getattr(admission, "is_valid_for", None)
        if not callable(is_valid):
            raise AdmissionRequiredError(
                "Trainer.process: ADMISSION_OBJECT_INVALID"
            )
        if not admission.is_valid_for(
            module=TRAINER_MODULE_ID,
            commit=self.expected_commit,
        ):
            raise AdmissionRequiredError(
                "Trainer.process: ADMISSION_NOT_VALID_FOR_CONTEXT"
            )

    def _record_halt(self, reason: str) -> None:
        """Post-admission best-effort halt evidence only.

        Must never be invoked on the pre-admission rejection path.
        """
        payload = {
            "turn": self._turn_counter,
            "allowed": False,
            "reason": reason,
            "halt": True,
        }
        try:
            self.memory.append(payload)
        except Exception:
            pass
        try:
            self.audit.log_event(payload)
        except Exception:
            pass

    def process(
        self,
        text: str,
        timestamp: Optional[_dt.datetime] = None,
        *,
        admission: Any,
    ) -> PipelineResult:
        """Run the pipeline only after a valid admission object.

        ``admission`` is required (keyword-only). Omitting it is a TypeError.
        Passing an invalid decision is AdmissionRequiredError before turn++.

        Expected shape: object with is_valid_for(module, commit) -> bool
        (typically AdmissionDecision from admission_boundary). No runtime
        import of AdmissionDecision here — duck-typed to keep production
        import surface minimal.
        """
        # First executable boundary — before turn counter and all side effects.
        self._require_admission(admission)

        self._turn_counter += 1

        try:
            sync_result = self.sync.record_turn(
                self._turn_counter, timestamp=timestamp
            )
        except ModuleKernelError as exc:
            reason = f"halted_by_module_03_kernel:{exc}"
            self._record_halt(reason)
            raise ModuleKernelError(reason) from exc

        try:
            security_result = self.security.scan(text)
        except ModuleKernelError as exc:
            reason = f"halted_by_module_02_kernel:{exc}"
            self._record_halt(reason)
            raise ModuleKernelError(reason) from exc

        try:
            redaction_result = self.redaction.redact(text)
        except ModuleKernelError as exc:
            reason = f"halted_by_module_05_kernel:{exc}"
            self._record_halt(reason)
            raise ModuleKernelError(reason) from exc

        drift_result = None
        allowed = True
        reason = None

        if security_result.blocked:
            allowed = False
            reason = f"blocked_by_security_probe:{security_result.triggered}"
        else:
            try:
                drift_result = self.drift.check(redaction_result.redacted_text)
            except ModuleKernelError as exc:
                reason = f"halted_by_module_06_kernel:{exc}"
                self._record_halt(reason)
                raise ModuleKernelError(reason) from exc

        mem_check = self.memory.validate_chain()
        if not mem_check.valid:
            reason = f"halted_by_module_07_integrity:broken_at_{mem_check.broken_at_index}"
            self._record_halt(reason)
            raise ModuleKernelError(reason)

        memory_payload = {
            "turn": self._turn_counter,
            "allowed": allowed,
            "reason": reason,
            "risk_score": security_result.risk_score,
        }
        try:
            self.memory.append(memory_payload)
        except Exception as exc:
            reason = f"halted_by_module_07_integrity:{exc}"
            self._record_halt(reason)
            raise ModuleKernelError(reason) from exc

        mem_after = self.memory.validate_chain()
        if not mem_after.valid:
            reason = (
                f"halted_by_module_07_integrity:post_write_broken_at_{mem_after.broken_at_index}"
            )
            self._record_halt(reason)
            raise ModuleKernelError(reason)

        audit_check = self.audit.verify_log()
        if not audit_check.valid:
            reason = (
                f"halted_by_module_09_integrity:broken_at_line_{audit_check.broken_at_line}"
            )
            self._record_halt(reason)
            raise ModuleKernelError(reason)

        audit_event = {
            "turn": self._turn_counter,
            "allowed": allowed,
            "reason": reason,
            "security_triggered": security_result.triggered,
            "redaction_categories": [m.category for m in redaction_result.matches],
        }
        try:
            self.audit.log_event(audit_event)
        except Exception as exc:
            reason = f"halted_by_module_09_persistence:{exc}"
            self._record_halt(reason)
            raise ModuleKernelError(reason) from exc

        audit_after = self.audit.verify_log()
        if not audit_after.valid:
            reason = (
                f"halted_by_module_09_integrity:post_write_broken_at_line_{audit_after.broken_at_line}"
            )
            self._record_halt(reason)
            raise ModuleKernelError(reason)

        return PipelineResult(
            allowed=allowed,
            reason=reason,
            security=security_result,
            sync=sync_result,
            redaction=redaction_result,
            drift=drift_result,
        )
