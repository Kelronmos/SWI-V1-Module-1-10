"""
Module 07: Memory Validator (Scar Integrity)

WHAT THIS ACTUALLY DOES:
Maintains an append-only, hash-chained sequence of "memory records" (the
manual's "Semantic Scars" -- here, just records of past decisions/events).
Each record's hash includes the previous record's hash, so altering or
deleting any past record breaks the chain from that point forward, and
`validate_chain()` will detect exactly where it broke. This is the same
core idea as a blockchain's block-linking, minus consensus or distribution
-- it is a local, in-process tamper-evidence structure, not a distributed
ledger and not a durable log.

WHAT THIS DOES NOT DO:
- It does **not** persist the chain to disk, a database, or any other durable
  store. The entire chain lives only in the MemoryValidator instance's
  memory (`self._chain: List[MemoryRecord]`). A new instance (e.g. after
  process restart or Trainer re-instantiation) starts with an empty chain
  and reports that empty chain as valid.
- It therefore cannot detect tampering or data loss that occurs *between*
  process lifetimes; it only detects in-process mutation of the live list
  (as demonstrated by `tamper_for_testing()` and the test suite).
- It does not provide tamper-proofness. Even if persistence were added,
  genuine tamper-proofness would still require the chain to be anchored
  somewhere the operator cannot rewrite (append-only remote storage, a
  separate audit service, or distributed consensus). That anchoring is not
  implemented here.

Contrast with Module 09 (Audit Logger), which *does* write an append-only
file on disk and verifies against that file. Module 07 does not currently
do the same; any claim that it does would be false.
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
    """Module 07: in-process hash-chained append-only memory log.

    Scope: detects in-process tampering of the live chain only.
    Does not persist; does not survive process restart.
    """

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
        directly. Used to prove validate_chain() detects the tamper.
        Only meaningful while the same process holds the chain.
        """
        self._chain[index].payload = new_payload

    @property
    def chain(self) -> List[MemoryRecord]:
        return list(self._chain)
