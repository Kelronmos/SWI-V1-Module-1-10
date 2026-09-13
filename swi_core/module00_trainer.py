"""
Module 00: The Trainer (The Master Orchestrator)

WHAT THIS ACTUALLY DOES:
Wires Modules 01-09 into a single request pipeline: an incoming message is
security-scanned (02), checked for context staleness (03), redacted for PII
(05), checked for output drift against a baseline (06), and every step is
written to the hash-chained audit log (09) and memory chain (07). It returns
a structured `PipelineResult` reporting what happened at each stage.

If Module 02's kernel contract fails (pre/post-check), the pipeline STOPS:
it does not continue to redaction/drift. The failure is recorded on the
audit/memory path when those writers remain usable, then re-raised as
ModuleKernelError so callers cannot treat a contract failure as success.

If `config_path` is given, `security_probe.block_threshold` and
`context_sync.staleness_seconds` are read from it via `config_loader`. Any
other setting in `swi_config.yaml` is still not read by this or any other
module -- only these two are wired. `process()` also accepts an optional
`timestamp` to pass through to `ContextSync`.

WHAT THIS DOES NOT DO:
It does not call out to Modules 11-46. It does not make autonomous decisions
beyond block/allow logic defined by the modules it calls. It does not claim
CEK, SAD-DFU, Vector Memory, or Sovereign Mesh. It does not validate that
config values are in sensible ranges beyond what individual modules enforce
at construction (e.g. SecurityProbe threshold).
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
        self.drift = DriftAnalyzer()
        self.memory = MemoryValidator()
        self.audit = AuditLogger(audit_log_path)
        self._turn_counter = 0

    def _record_halt(self, reason: str) -> None:
        """Best-effort evidence of a controlled stop. Must not hide the halt."""
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
        sync_result = self.sync.record_turn(self._turn_counter, timestamp=timestamp)

        # --- Module 02: kernel-wrapped; contract failure => STOP ---
        try:
            security_result = self.security.scan(text)
        except ModuleKernelError as exc:
            reason = f"halted_by_module_02_kernel:{exc}"
            self._record_halt(reason)
            raise ModuleKernelError(reason) from exc

        redaction_result = self.redaction.redact(text)

        drift_result = None
        allowed = True
        reason = None

        if security_result.blocked:
            allowed = False
            reason = f"blocked_by_security_probe:{security_result.triggered}"
        else:
            drift_result = self.drift.check(redaction_result.redacted_text)

        self.memory.append(
            {
                "turn": self._turn_counter,
                "allowed": allowed,
                "reason": reason,
                "risk_score": security_result.risk_score,
            }
        )
        self.audit.log_event(
            {
                "turn": self._turn_counter,
                "allowed": allowed,
                "reason": reason,
                "security_triggered": security_result.triggered,
                "redaction_categories": [m.category for m in redaction_result.matches],
            }
        )

        return PipelineResult(
            allowed=allowed,
            reason=reason,
            security=security_result,
            sync=sync_result,
            redaction=redaction_result,
            drift=drift_result,
        )
