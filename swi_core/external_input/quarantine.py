"""Quarantine: preserve original input; do not rewrite before hash."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict

from swi_core.external_input.models import ExternalInput, InputState
from swi_core.external_input.normalize import payload_sha256


@dataclass
class QuarantineRecord:
    input_id: str
    original_payload: Dict[str, Any]
    payload_hash: str
    serialization_version: str
    source_type: str
    source_id: str
    origin: str


def quarantine(ext: ExternalInput) -> QuarantineRecord:
    original = deepcopy(ext.payload)
    h = payload_sha256(original)
    ext.payload_hash = h
    ext.state = InputState.QUARANTINED
    return QuarantineRecord(
        input_id=ext.input_id,
        original_payload=original,
        payload_hash=h,
        serialization_version=ext.serialization_version,
        source_type=ext.source_type.value,
        source_id=ext.source_id,
        origin=ext.origin,
    )
