"""
Module 03: Context Sync (Temporal Alignment)

WHAT THIS ACTUALLY DOES:
Tracks the timestamp of each conversation turn and flags when the gap since
the last turn exceeds a configurable staleness threshold, or when turns
arrive out of chronological order. This is useful for deciding whether
previously-established context (e.g. "as we agreed 20 minutes ago") should
still be treated as current.

WHAT THIS DOES NOT DO:
It does not verify the *content* of context is still true -- only that time
has or hasn't passed. It relies on the caller supplying honest timestamps;
it cannot detect a spoofed clock.
"""
from __future__ import annotations
import datetime as _dt
from dataclasses import dataclass
from typing import List, Optional


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
    """Module 03: temporal alignment across conversation turns."""

    def __init__(self, staleness_seconds: float = 1800.0):
        self.staleness_seconds = staleness_seconds
        self._turns: List[Turn] = []

    def record_turn(self, turn_id: int, timestamp: Optional[_dt.datetime] = None) -> SyncResult:
        timestamp = timestamp or _dt.datetime.now(_dt.timezone.utc)
        out_of_order = bool(self._turns) and timestamp < self._turns[-1].timestamp
        gap = (
            (timestamp - self._turns[-1].timestamp).total_seconds()
            if self._turns
            else 0.0
        )
        stale = gap > self.staleness_seconds
        self._turns.append(Turn(turn_id=turn_id, timestamp=timestamp))
        return SyncResult(stale=stale, out_of_order=out_of_order, gap_seconds=gap)

    def history(self) -> List[Turn]:
        return list(self._turns)
