"""
Module 07: Memory Validator (Scar Integrity)

WHAT THIS ACTUALLY DOES:
Maintains an append-only, hash-chained sequence of "memory records" (the
manual's "Semantic Scars" -- here, just records of past decisions/events).
Each record's hash includes the previous record's hash, so altering or
deleting any past record breaks the chain from that point forward, and
`validate_chain()` will detect exactly where it broke. This is the same
core idea as a blockchain's block-linking, minus consensus or distribution
-- it is a local tamper-evidence log, not a distributed ledger.

WHAT THIS DOES NOT DO:
It does not prevent someone with write access to the storage medium from
regenerating the entire chain from scratch (tamper-evidence, not
tamper-proofness). Genuine tamper-*proofness* requires the chain to be
anchored somewhere the operator cannot rewrite (e.g. append-only remote
storage, a separate audit service, or actual distributed consensus) -- that
anchoring is not implemented here and any claim that it is would be false.
"""
from __future__ import annotations
import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class MemoryRecord:
    index: int
    timestamp: float
    payload: Any
    prev_hash: str
    hash: str = field(init=False)

    def __post_init__(self):
        self.hash = self._compute_hash()

    def _compute_hash(self) -> str:
        body = json.dumps(
            {"index": self.index, "timestamp": self.timestamp, "payload": self.payload, "prev_hash": self.prev_hash},
            sort_keys=True,
            default=str,
        )
        return hashlib.sha256(body.encode("utf-8")).hexdigest()


@dataclass
class ValidationResult:
    valid: bool
    broken_at_index: Optional[int] = None


class MemoryValidator:
    """Module 07: hash-chained append-only memory log."""

    GENESIS_HASH = "0" * 64

    def __init__(self):
        self._chain: List[MemoryRecord] = []

    def append(self, payload: Any) -> MemoryRecord:
        prev_hash = self._chain[-1].hash if self._chain else self.GENESIS_HASH
        record = MemoryRecord(
            index=len(self._chain), timestamp=time.time(), payload=payload, prev_hash=prev_hash
        )
        self._chain.append(record)
        return record

    def validate_chain(self) -> ValidationResult:
        prev_hash = self.GENESIS_HASH
        for record in self._chain:
            expected_hash = record._compute_hash()
            if record.prev_hash != prev_hash or record.hash != expected_hash:
                return ValidationResult(valid=False, broken_at_index=record.index)
            prev_hash = record.hash
        return ValidationResult(valid=True)

    def tamper_for_testing(self, index: int, new_payload: Any) -> None:
        """Test-only helper: mutates a past record's payload WITHOUT
        recomputing its hash, simulating an attacker editing stored data
        directly. Used to prove validate_chain() detects the tamper."""
        self._chain[index].payload = new_payload

    @property
    def chain(self) -> List[MemoryRecord]:
        return list(self._chain)
