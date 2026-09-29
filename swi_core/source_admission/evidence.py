"""Evidence hash for source admission records.

The hash establishes integrity of the recorded evidence material.
It does not prove authority, truth, path closure, or regulatory compliance.
"""
from __future__ import annotations

import hashlib
import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from swi_core.source_admission.models import SourceAdmissionRecord


def _canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode(
        "utf-8"
    )


def evidence_hash_for_record(record: "SourceAdmissionRecord") -> str:
    material = record.to_evidence_dict()
    # Exclude evidence_hash field itself (not present in to_evidence_dict).
    digest = hashlib.sha256(_canonical_json(material)).hexdigest()
    return digest
