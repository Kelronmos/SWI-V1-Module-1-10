"""
Module 00: The Trainer (The Master Orchestrator)

WHAT THIS ACTUALLY DOES:
Wires Modules 01-09 into a single request pipeline: an incoming message is
security-scanned (02), checked for context staleness (03), redacted for PII
(05), checked for output drift against a baseline (06), and every step is
written to the hash-chained audit log (09) and memory chain (07). It returns
a structured `PipelineResult` reporting what happened at each stage.

If `config_path` is given, `security_probe.block_threshold` and
`context_sync.staleness_seconds` are read from it via `config_loader`. Any
other setting in `swi_config.yaml` is still not read by this or any other
module -- only these two are wired. `process()` also accepts an optional
`timestamp` to pass through to `ContextSync`; the caller supplies it, this
does not read a system clock on your behalf beyond what ContextSync already
defaults to when omitted.

WHAT THIS DOES NOT DO:
It does not call out to Modules 11-46 -- those are outside Volume 1's scope
and are not implemented in this package. It does not make any autonomous
decisions beyond the block/allow logic defined by the modules it calls; the
"Master Orchestrator" framing in the original manual should not be read as
implying capabilities beyond this sequential pipeline. It does not validate
that config values are in sensible ranges -- see config_loader's docstring.
"""
from __future__ import annotations
import datetime as _dt
from dataclasses import dataclass, field
from typing import List, Optional

from .config_loader import load_config
from .module02_security_probe import SecurityProbe, ProbeResult
from .module03_context_sync import ContextSync, SyncResult
from .module05_redaction_engine import RedactionEngine, RedactionResult
from .module06_drift_analyzer import DriftAnalyzer, DriftResult
from .module07_memory_validator import MemoryValidator
from .module09_audit_logger import AuditLogger


@dataclass
class PipelineResult:
    allowed: bool
    reason: Optional[str]
    security: ProbeResult
    sync: SyncResult
    redaction: RedactionResult
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

    def process(
        self, text: str, timestamp: Optional[_dt.datetime] = None
    ) -> PipelineResult:
        self._turn_counter += 1
        sync_result = self.sync.record_turn(self._turn_counter, timestamp=timestamp)
        security_result = self.security.scan(text)
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
