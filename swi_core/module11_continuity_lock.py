"""
Module 11: Continuity Lock (State Preservation)

WHAT THIS ACTUALLY DOES:
Maintains a bounded list of state tags (max 10 by default) so an agent can
preserve short-term context across turns. Provides update_state() and
get_pinned_context(). Older tags are dropped in FIFO order when the limit
is exceeded.

This is a working, deterministic implementation of the Continuity Lock
concept described in Volume 2. It is not claimed as SEALED; it is
IMPLEMENTED and TESTED.

WHAT THIS DOES NOT DO:
- Does not persist across process restarts (unless a path is given).
- Does not perform semantic understanding of the tags.
- Does not replace Vector Memory / Scars (different concern).
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class StateTag:
    key: str
    value: str
    pinned_at: float = field(default_factory=time.time)


@dataclass
class ContinuitySnapshot:
    tags: List[StateTag]
    max_tags: int
    updated_at: float


class ContinuityLock:
    """Module 11: bounded state-tag preservation."""

    def __init__(self, max_tags: int = 10, persist_path: Optional[str] = None) -> None:
        if max_tags < 1:
            raise ValueError("max_tags must be >= 1")
        self.max_tags = max_tags
        self._tags: List[StateTag] = []
        self._persist_path = persist_path
        if persist_path:
            self._load()

    def update_state(self, key: str, value: str) -> ContinuitySnapshot:
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError("key must be non-empty")

        # Update existing key in place, then move to end (most recent)
        self._tags = [t for t in self._tags if t.key != key]
        self._tags.append(StateTag(key=key, value=value))

        while len(self._tags) > self.max_tags:
            self._tags.pop(0)

        self._save()
        return self.snapshot()

    def get_pinned_context(self) -> str:
        if not self._tags:
            return ""
        lines = [f"{t.key}={t.value}" for t in self._tags]
        return " | ".join(lines)

    def snapshot(self) -> ContinuitySnapshot:
        return ContinuitySnapshot(
            tags=list(self._tags),
            max_tags=self.max_tags,
            updated_at=time.time(),
        )

    def clear(self) -> None:
        self._tags.clear()
        self._save()

    def _save(self) -> None:
        if not self._persist_path:
            return
        path = Path(self._persist_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = [{"key": t.key, "value": t.value, "pinned_at": t.pinned_at} for t in self._tags]
        path.write_text(json.dumps(data), encoding="utf-8")

    def _load(self) -> None:
        if not self._persist_path:
            return
        path = Path(self._persist_path)
        if not path.exists():
            return
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            self._tags = [
                StateTag(key=d["key"], value=d["value"], pinned_at=d.get("pinned_at", time.time()))
                for d in data
            ][-self.max_tags :]
        except (json.JSONDecodeError, KeyError, TypeError):
            self._tags = []
