"""
Module 00: The Trainer (The Master Orchestrator)

Kernel contract failures on Module 03, 02, 05, or 06 STOP the pipeline.
M07/M09 normal-path integrity/persistence failures also STOP (ModuleKernelError).
Halt recording remains best-effort and never converts failure into success.

stale / out_of_order / drifted remain advisory flags.

Runtime config: security_probe.block_threshold, context_sync.staleness_seconds,
drift_analyzer.drift_threshold.
"""
from __future__ import annotations
import datetime as _dt
from dataclasses import dataclass
from typing import Optional

from .config_loader import load_config
from .module02_security_probe import SecurityProbe, ProbeResult
from .module03_context_sync import ContextSync, SyncResult
from .module05_redaction_engine import RedactionEngine, RedactionResult
from .module06_drift_analyzer import DriftAnalyzer, DriftResult
from .module07_memory_validator import MemoryValidator
from .module09_audit_logger import AuditLogger
from .module_kernel import ModuleKernelError


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

    def __init__(self, audit_log_path: str, config_path: Optional[str] = None):
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

    def _record_halt(self, reason: str) -> None:
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
        self, text: str, timestamp: Optional[_dt.datetime] = None
    ) -> PipelineResult:
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
            reason = f"halted_by_module_07_persistence:{exc}"
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
