"""
Module 03: Context Sync (Temporal Alignment)

WHAT THIS ACTUALLY DOES:
Tracks the timestamp of each conversation turn and flags when the gap since
the last turn exceeds a configurable staleness threshold, or when turns
arrive out of chronological order. This is useful for deciding whether
previously-established context (e.g. "as we agreed 20 minutes ago") should
still be treated as current.

Kernel enforces input/output type-shape only. stale / out_of_order remain
data flags — they do not by themselves raise ModuleKernelError.

WHAT THIS DOES NOT DO:
It does not verify the *content* of context is still true -- only that time
has or hasn't passed. It relies on the caller supplying honest timestamps;
it cannot detect a spoofed clock. It does not halt the Trainer pipeline when
stale=True; only contract failures raise ModuleKernelError.
"""
from __future__ import annotations

import datetime as _dt
import math
from dataclasses import dataclass
from typing import List, Optional, Tuple

from .module_kernel import CheckResult, ModuleKernel

# Input payload for kernel: (turn_id, timestamp)
_TurnInput = Tuple[object, Optional[_dt.datetime]]


@dataclass
class Turn:
    turn_id: int
    timestamp: _dt.datetime


@dataclass
class SyncResult:
    stale: bool
    out_of_order: bool
    gap_seconds: float


class ContextSync:
    """Module 03: temporal alignment across conversation turns (kernel-enforced)."""

    def __init__(self, staleness_seconds: float = 1800.0):
        if isinstance(staleness_seconds, bool) or not isinstance(
            staleness_seconds, (int, float)
        ):
            raise ValueError(
                f"staleness_seconds must be int or float, got {type(staleness_seconds).__name__}"
            )
        if not math.isfinite(float(staleness_seconds)):
            raise ValueError("staleness_seconds must be finite")
        if float(staleness_seconds) < 0:
            raise ValueError("staleness_seconds must be >= 0")
        self.staleness_seconds = float(staleness_seconds)
        self._turns: List[Turn] = []
        self.kernel = ModuleKernel(
            name="module_03_context_sync",
            pre_checks=(
                self._input_is_pair,
                self._timestamp_is_valid,
            ),
            post_checks=(
                self._result_is_sync_result,
                self._result_fields_valid,
            ),
        )

    def record_turn(
        self, turn_id: int, timestamp: Optional[_dt.datetime] = None
    ) -> SyncResult:
        return self.kernel.run((turn_id, timestamp), self._record_turn_impl)

    def history(self) -> List[Turn]:
        return list(self._turns)

    def _input_is_pair(self, value: object) -> CheckResult:
        if not isinstance(value, tuple) or len(value) != 2:
            return CheckResult(
                name="input_is_pair",
                passed=False,
                reason=f"expected (turn_id, timestamp), got {type(value).__name__}",
            )
        return CheckResult(name="input_is_pair", passed=True)

    def _timestamp_is_valid(self, value: object) -> CheckResult:
        if not isinstance(value, tuple) or len(value) != 2:
            return CheckResult(
                name="timestamp_is_valid",
                passed=False,
                reason="payload must be a 2-tuple",
            )
        _turn_id, timestamp = value
        if timestamp is not None and not isinstance(timestamp, _dt.datetime):
            return CheckResult(
                name="timestamp_is_valid",
                passed=False,
                reason=(
                    "timestamp must be datetime or None, "
                    f"got {type(timestamp).__name__}"
                ),
            )
        return CheckResult(name="timestamp_is_valid", passed=True)

    def _result_is_sync_result(self, value: object) -> CheckResult:
        if not isinstance(value, SyncResult):
            return CheckResult(
                name="result_is_sync_result",
                passed=False,
                reason=f"expected SyncResult, got {type(value).__name__}",
            )
        return CheckResult(name="result_is_sync_result", passed=True)

    def _result_fields_valid(self, value: object) -> CheckResult:
        if not isinstance(value, SyncResult):
            return CheckResult(
                name="result_fields_valid",
                passed=False,
                reason="not a SyncResult",
            )
        if type(value.stale) is not bool:
            return CheckResult(
                name="result_fields_valid",
                passed=False,
                reason=f"stale must be bool, got {type(value.stale).__name__}",
            )
        if type(value.out_of_order) is not bool:
            return CheckResult(
                name="result_fields_valid",
                passed=False,
                reason=(
                    "out_of_order must be bool, "
                    f"got {type(value.out_of_order).__name__}"
                ),
            )
        if isinstance(value.gap_seconds, bool) or not isinstance(
            value.gap_seconds, (int, float)
        ):
            return CheckResult(
                name="result_fields_valid",
                passed=False,
                reason=(
                    "gap_seconds must be int/float, "
                    f"got {type(value.gap_seconds).__name__}"
                ),
            )
        if not math.isfinite(float(value.gap_seconds)):
            return CheckResult(
                name="result_fields_valid",
                passed=False,
                reason="gap_seconds must be finite",
            )
        return CheckResult(name="result_fields_valid", passed=True)

    def _record_turn_impl(self, value: _TurnInput) -> SyncResult:
        turn_id, timestamp = value
        timestamp = timestamp or _dt.datetime.now(_dt.timezone.utc)
        out_of_order = bool(self._turns) and timestamp < self._turns[-1].timestamp
        gap = (
            (timestamp - self._turns[-1].timestamp).total_seconds()
            if self._turns
            else 0.0
        )
        stale = gap > self.staleness_seconds
        self._turns.append(Turn(turn_id=turn_id, timestamp=timestamp))  # type: ignore[arg-type]
        return SyncResult(
            stale=stale, out_of_order=out_of_order, gap_seconds=gap
        )
