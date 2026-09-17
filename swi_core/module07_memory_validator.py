"""
Module 07: Memory Validator (Scar Integrity)

v1.1: Integrates with ScarStore when provided. Still supports the original
in-process hash-chained MemoryRecord log for backward compatibility.

WHAT THIS ACTUALLY DOES:
- Maintains an append-only, hash-chained sequence of memory records (legacy).
- When a ScarStore is attached, also validates Scar content hashes and the
  ScarStore integrity root.
- Detects in-process tampering of the live chain.

WHAT THIS DOES NOT DO:
- Does not claim durable Vector Memory or Foundation Seal status.
- Legacy chain remains in-process unless the caller supplies a persistent
  ScarStore (SQLite path).
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, List, Optional

from .scar import ScarStore


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
            {
                "index": self.index,
                "timestamp": self.timestamp,
                "payload": self.payload,
                "prev_hash": self.prev_hash,
            },
            sort_keys=True,
            default=str,
        )
        return hashlib.sha256(body.encode("utf-8")).hexdigest()


@dataclass
class ValidationResult:
    valid: bool
    broken_at_index: Optional[int] = None
    scar_integrity: Optional[dict] = None


class MemoryValidator:
    """Module 07: hash-chained memory log + optional ScarStore integrity."""

    GENESIS_HASH = "0" * 64

    def __init__(self, scar_store: Optional[ScarStore] = None):
        self._chain: List[MemoryRecord] = []
        self.scar_store = scar_store

    def append(self, payload: Any) -> MemoryRecord:
        prev_hash = self._chain[-1].hash if self._chain else self.GENESIS_HASH
        record = MemoryRecord(
            index=len(self._chain),
            timestamp=time.time(),
            payload=payload,
            prev_hash=prev_hash,
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

        scar_result = None
        if self.scar_store is not None:
            scar_result = self.scar_store.validate_integrity()
            if not scar_result["valid"]:
                return ValidationResult(
                    valid=False,
                    broken_at_index=None,
                    scar_integrity=scar_result,
                )

        return ValidationResult(valid=True, scar_integrity=scar_result)

    def tamper_for_testing(self, index: int, new_payload: Any) -> None:
        """Test-only: mutate past payload without recomputing hash."""
        self._chain[index].payload = new_payload

    @property
    def chain(self) -> List[MemoryRecord]:
        return list(self._chain)
