"""
SWI Scar model and ScarStore (Phase 2 Vector Memory foundation).

WHAT THIS ACTUALLY DOES:
Defines a concrete, content-addressable Scar object and a store that can
hold Scars with priority rules (Sovereign > Functional), content hashing,
and an integrity root over active content hashes.

Supports in-process storage by default. Optional SQLite persistence can be
enabled so the store survives process restart within a single deployment.

WHAT THIS DOES NOT DO:
- Not a full vector database or embedding service.
- Embeddings are optional; when not supplied the store still works on
  metadata + content_hash only.
- Does not claim Vector Memory, SAD-DFU, or Foundation Seal status.
- Does not perform semantic similarity search unless an external embedder
  is provided by the caller.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class ScarClass(str, Enum):
    SOVEREIGN = "sovereign"
    FUNCTIONAL = "functional"


class ScarStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    PRUNED = "pruned"
    SUSPECT = "suspect"


@dataclass
class Scar:
    scar_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    version: int = 1
    scar_class: ScarClass = ScarClass.FUNCTIONAL
    status: ScarStatus = ScarStatus.ACTIVE

    title: str = ""
    description: str = ""
    trigger_context: str = ""
    failure_signature: str = ""
    recommended_response: str = ""

    embedding: Optional[List[float]] = None
    embedding_model: str = ""
    embedding_dim: int = 0

    content_hash: str = ""
    previous_scar_hash: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    created_by: str = "system"
    source_event_id: Optional[str] = None

    priority_score: float = 1.0
    protection_level: int = 1
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if isinstance(self.scar_class, str):
            self.scar_class = ScarClass(self.scar_class)
        if isinstance(self.status, str):
            self.status = ScarStatus(self.status)
        if not self.content_hash:
            self.content_hash = self.compute_content_hash()
        if self.scar_class == ScarClass.SOVEREIGN and self.priority_score < 2.0:
            self.priority_score = 2.0

    def compute_content_hash(self) -> str:
        canonical = (
            f"{self.scar_class.value}|{self.title}|{self.description}|"
            f"{self.trigger_context}|{self.failure_signature}|"
            f"{self.recommended_response}|{self.embedding_model}"
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def is_sovereign(self) -> bool:
        return self.scar_class == ScarClass.SOVEREIGN

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["scar_class"] = self.scar_class.value
        d["status"] = self.status.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Scar":
        data = dict(data)
        data["scar_class"] = ScarClass(data.get("scar_class", "functional"))
        data["status"] = ScarStatus(data.get("status", "active"))
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class ScarStoreError(RuntimeError):
    pass


class ScarStore:
    """Working Scar store with priority rules and integrity root.

    Default: in-process dict.
    Optional: SQLite file for persistence across process restarts.
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        self._scars: Dict[str, Scar] = {}
        self._db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
        if db_path:
            self._init_db(db_path)
            self._load_from_db()

    def _init_db(self, path: str) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(path)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scars (
                scar_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def _load_from_db(self) -> None:
        if not self._conn:
            return
        cur = self._conn.execute("SELECT scar_id, payload FROM scars")
        for scar_id, payload in cur.fetchall():
            self._scars[scar_id] = Scar.from_dict(json.loads(payload))

    def _persist(self, scar: Scar) -> None:
        if not self._conn:
            return
        self._conn.execute(
            "INSERT OR REPLACE INTO scars (scar_id, payload) VALUES (?, ?)",
            (scar.scar_id, json.dumps(scar.to_dict())),
        )
        self._conn.commit()

    def create(
        self,
        *,
        title: str,
        description: str,
        scar_class: ScarClass = ScarClass.FUNCTIONAL,
        trigger_context: str = "",
        failure_signature: str = "",
        recommended_response: str = "",
        created_by: str = "system",
        source_event_id: Optional[str] = None,
        protection_level: int = 1,
        tags: Optional[List[str]] = None,
        embedding: Optional[List[float]] = None,
        embedding_model: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Scar:
        scar = Scar(
            title=title,
            description=description,
            scar_class=scar_class,
            trigger_context=trigger_context,
            failure_signature=failure_signature,
            recommended_response=recommended_response,
            created_by=created_by,
            source_event_id=source_event_id,
            protection_level=protection_level,
            tags=tags or [],
            embedding=embedding,
            embedding_model=embedding_model,
            embedding_dim=len(embedding) if embedding else 0,
            metadata=metadata or {},
        )
        self._scars[scar.scar_id] = scar
        self._persist(scar)
        return scar

    def get(self, scar_id: str) -> Optional[Scar]:
        return self._scars.get(scar_id)

    def list_active(self, class_filter: Optional[ScarClass] = None) -> List[Scar]:
        out = []
        for s in self._scars.values():
            if s.status != ScarStatus.ACTIVE:
                continue
            if class_filter and s.scar_class != class_filter:
                continue
            out.append(s)
        out.sort(key=lambda s: (-s.priority_score, s.created_at))
        return out

    def prune(self, scar_id: str, reason: str, authorized_by: str) -> Scar:
        scar = self._scars.get(scar_id)
        if not scar:
            raise ScarStoreError(f"scar not found: {scar_id}")
        if scar.protection_level >= 3 and authorized_by not in ("architect", "module_00"):
            raise ScarStoreError(
                f"protection_level {scar.protection_level} requires architect/module_00"
            )
        scar.status = ScarStatus.PRUNED
        scar.metadata["prune_reason"] = reason
        scar.metadata["pruned_by"] = authorized_by
        scar.metadata["pruned_at"] = time.time()
        self._persist(scar)
        return scar

    def integrity_root(self) -> str:
        """SHA-256 over sorted active content_hashes. Detects silent mutation."""
        hashes = sorted(
            s.content_hash for s in self._scars.values() if s.status == ScarStatus.ACTIVE
        )
        body = "|".join(hashes)
        return hashlib.sha256(body.encode("utf-8")).hexdigest()

    def validate_integrity(self) -> Dict[str, Any]:
        broken = []
        for s in self._scars.values():
            expected = s.compute_content_hash()
            if s.content_hash != expected:
                broken.append(s.scar_id)
                s.status = ScarStatus.SUSPECT
        return {
            "valid": len(broken) == 0,
            "broken_scar_ids": broken,
            "integrity_root": self.integrity_root(),
            "active_count": len(self.list_active()),
        }

    def count(self) -> int:
        return len(self._scars)
