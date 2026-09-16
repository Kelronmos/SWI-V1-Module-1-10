"""
Module 09: Audit Logger (The Immutable Flight Recorder)

WHAT THIS ACTUALLY DOES:
Writes structured audit events to an append-only log file, where each line
is hash-chained to the previous line (same technique as Module 07, applied
to on-disk logs specifically). `verify_log()` re-reads the file and confirms
the chain is intact, reporting the first broken line if not.

WHAT THIS DOES NOT DO:
"Immutable" here means tamper-evident, not tamper-proof: a party with
filesystem write access and the ability to regenerate hashes can still
rewrite the entire file. True immutability requires write-once storage,
remote mirroring, or a separate service outside the agent's own write
access -- none of which this module provides on its own.

Fail-closed: malformed JSON or missing required fields on a line yield
valid=False with broken_at_line set; JSONDecodeError / KeyError must not
escape verify_log().
"""
from __future__ import annotations
import hashlib
import json
import os
import time
from dataclasses import dataclass
from typing import Any, Optional


GENESIS_HASH = "0" * 64


def _line_hash(prev_hash: str, timestamp: float, event: Any) -> str:
    body = json.dumps({"prev_hash": prev_hash, "timestamp": timestamp, "event": event}, sort_keys=True, default=str)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


@dataclass
class VerifyLogResult:
    valid: bool
    broken_at_line: Optional[int] = None
    lines_checked: int = 0


class AuditLogger:
    """Module 09: append-only, hash-chained audit log on disk."""

    def __init__(self, log_path: str):
        self.log_path = log_path
        if not os.path.exists(log_path):
            open(log_path, "w").close()

    def _last_hash(self) -> str:
        last = GENESIS_HASH
        with open(self.log_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    last = json.loads(line)["hash"]
                except Exception:
                    # Malformed prior line: treat as genesis so a subsequent
                    # write does not crash; verify_log will still report the break.
                    return GENESIS_HASH
        return last

    def log_event(self, event: Any) -> str:
        prev_hash = self._last_hash()
        timestamp = time.time()
        h = _line_hash(prev_hash, timestamp, event)
        record = {"prev_hash": prev_hash, "timestamp": timestamp, "event": event, "hash": h}
        with open(self.log_path, "a") as f:
            f.write(json.dumps(record, default=str) + "\n")
        return h

    def verify_log(self) -> VerifyLogResult:
        prev_hash = GENESIS_HASH
        count = 0
        with open(self.log_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                count += 1
                try:
                    record = json.loads(line)
                    if not isinstance(record, dict):
                        return VerifyLogResult(valid=False, broken_at_line=count, lines_checked=count)
                    required = ("prev_hash", "timestamp", "event", "hash")
                    if any(k not in record for k in required):
                        return VerifyLogResult(valid=False, broken_at_line=count, lines_checked=count)
                    expected = _line_hash(record["prev_hash"], record["timestamp"], record["event"])
                    if record["prev_hash"] != prev_hash or record["hash"] != expected:
                        return VerifyLogResult(valid=False, broken_at_line=count, lines_checked=count)
                    prev_hash = record["hash"]
                except Exception:
                    return VerifyLogResult(valid=False, broken_at_line=count, lines_checked=count)
        return VerifyLogResult(valid=True, lines_checked=count)
