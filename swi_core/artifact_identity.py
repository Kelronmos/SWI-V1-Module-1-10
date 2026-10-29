"""SWI Artifact Identity — reference implementation (Python).

Assigns IDs, serials, SHA-256 digests. Does NOT authorize or prove SWI.

PROVEN=NO SEALED=NO AUTHORIZED=NO PRODUCTION_AUTHORIZED=NO
"""
from __future__ import annotations

import hashlib
import json
import secrets
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, BinaryIO, Iterable, Optional

SCHEMA = "swi.artifact-identity.v1"
HASH_ALG = "SHA-256"


def utc_now_rfc3339() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_artifact_id() -> str:
    return str(uuid.uuid4())


def new_serial(kind: str = "ART") -> str:
    """Human-readable serial; CSPRNG suffix — not an authorization token."""
    kind = kind.upper().replace(" ", "")
    day = datetime.now(timezone.utc).strftime("%Y%m%d")
    suffix = secrets.token_hex(6)
    return f"SWI-{kind}-{day}-{suffix}"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_stream(fp: BinaryIO, chunk_size: int = 1024 * 1024) -> tuple[str, int]:
    h = hashlib.sha256()
    total = 0
    while True:
        chunk = fp.read(chunk_size)
        if not chunk:
            break
        h.update(chunk)
        total += len(chunk)
    return h.hexdigest(), total


def sha256_file(path: Path | str, chunk_size: int = 1024 * 1024) -> tuple[str, int]:
    path = Path(path)
    with path.open("rb") as f:
        return sha256_stream(f, chunk_size=chunk_size)


def canonical_json_bytes(obj: Any) -> bytes:
    """Canonical JSON: UTF-8, sorted keys, no insignificant whitespace."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_canonical_json(obj: Any) -> str:
    return sha256_bytes(canonical_json_bytes(obj))


def register_bytes(
    data: bytes,
    *,
    artifact_type: str = "binary",
    media_type: str = "application/octet-stream",
    task_id: Optional[str] = None,
    execution_id: Optional[str] = None,
    origin_type: str = "SWI_GENERATED",
    origin_reference: Optional[str] = None,
    external_id: Optional[str] = None,
    parent_artifacts: Optional[list[str]] = None,
    transformations: Optional[list[str]] = None,
) -> dict[str, Any]:
    digest = sha256_bytes(data)
    record = {
        "schema": SCHEMA,
        "artifact_id": new_artifact_id(),
        "serial": new_serial("ART"),
        "artifact_type": artifact_type,
        "task_id": task_id,
        "execution_id": execution_id,
        "created_at": utc_now_rfc3339(),
        "timestamp_source": "system-clock",
        "timestamp_trust": "UNVERIFIED",
        "origin_type": origin_type,
        "origin_reference": origin_reference,
        "external_id": external_id,
        "content": {
            "media_type": media_type,
            "size_bytes": len(data),
            "hash_algorithm": HASH_ALG,
            "digest": digest,
        },
        "parent_artifacts": list(parent_artifacts or []),
        "transformations": list(transformations or []),
        "integrity_status": "UNVERIFIED",
        "signature_status": "UNSIGNED",
        "proof_status": "NOT_PROVEN",
        "authorization_status": "NOT_AUTHORIZED",
        "replay_status": "NOT_REPLAYED",
        "record_version": 1,
    }
    return record


def register_file(path: Path | str, **kwargs: Any) -> dict[str, Any]:
    path = Path(path)
    with path.open("rb") as f:
        data = f.read()
    media = kwargs.get("media_type") or "application/octet-stream"
    return register_bytes(data, media_type=media, **{k: v for k, v in kwargs.items() if k != "media_type"})


def verify_bytes(data: bytes, record: dict[str, Any]) -> dict[str, Any]:
    """Recalculate digest; never promotes authorization/proof."""
    out = dict(record)
    expected = (record.get("content") or {}).get("digest")
    actual = sha256_bytes(data)
    size = len(data)
    if expected is None:
        out["integrity_status"] = "UNAVAILABLE"
    elif actual == expected and size == (record.get("content") or {}).get("size_bytes", size):
        out["integrity_status"] = "MATCH"
    else:
        out["integrity_status"] = "MISMATCH"
    # Ceilings fixed
    out["proof_status"] = record.get("proof_status") or "NOT_PROVEN"
    if out["proof_status"] not in (
        "NOT_PROVEN",
        "PROOF_PENDING",
        "PROOF_PASSED_WITHIN_SCOPE",
        "PROOF_FAILED",
        "PROOF_INCOMPLETE",
    ):
        out["proof_status"] = "NOT_PROVEN"
    out["authorization_status"] = "NOT_AUTHORIZED"
    out["authorized"] = False
    out["proven"] = False
    out["sealed"] = False
    out["production_authorized"] = False
    out["observed_digest"] = actual
    return out


def verify_file(path: Path | str, record: dict[str, Any]) -> dict[str, Any]:
    path = Path(path)
    try:
        with path.open("rb") as f:
            data = f.read()
    except OSError:
        out = dict(record)
        out["integrity_status"] = "UNAVAILABLE"
        out["authorization_status"] = "NOT_AUTHORIZED"
        out["proven"] = False
        out["authorized"] = False
        out["production_authorized"] = False
        return out
    return verify_bytes(data, record)


def new_version_from_bytes(
    data: bytes,
    parent: dict[str, Any],
    *,
    transformation: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """Content change → new identity + digest; link parent."""
    parents = list(parent.get("parent_artifacts") or [])
    parents.append(parent["artifact_id"])
    transforms = list(parent.get("transformations") or [])
    transforms.append(transformation)
    return register_bytes(
        data,
        artifact_type=kwargs.get("artifact_type") or parent.get("artifact_type") or "binary",
        media_type=kwargs.get("media_type") or (parent.get("content") or {}).get("media_type") or "application/octet-stream",
        task_id=kwargs.get("task_id") or parent.get("task_id"),
        execution_id=kwargs.get("execution_id"),
        origin_type="REGENERATED",
        origin_reference=parent.get("artifact_id"),
        parent_artifacts=parents,
        transformations=transforms,
    )
