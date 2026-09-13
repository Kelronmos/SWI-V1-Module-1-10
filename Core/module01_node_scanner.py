"""
Module 01: The Node Scanner (The Integrity Probe)

WHAT THIS ACTUALLY DOES:
Computes a SHA-256 hash of a set of files (or arbitrary byte content) and
compares it against a previously recorded baseline. This detects whether
tracked content has changed between two points in time.

WHAT THIS DOES NOT DO:
It does not detect *why* something changed, does not run on a schedule by
itself, and provides no protection if the baseline file itself is tampered
with by someone who also has write access to it. Baseline integrity is the
caller's responsibility (e.g. store it somewhere the agent process cannot
write to).
"""
from __future__ import annotations
import hashlib
import json
import os
from dataclasses import dataclass, field
from typing import Dict, Iterable


@dataclass
class ScanResult:
    baseline_hash: str
    current_hash: str

    @property
    def match(self) -> bool:
        return self.baseline_hash == self.current_hash


class NodeScanner:
    """Module 01: computes and verifies content-integrity hashes."""

    def __init__(self):
        self._baselines: Dict[str, str] = {}

    @staticmethod
    def _hash_bytes(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def _hash_files(paths: Iterable[str]) -> str:
        h = hashlib.sha256()
        for path in sorted(paths):
            with open(path, "rb") as f:
                h.update(f.read())
        return h.hexdigest()

    def register_baseline(self, node_id: str, paths: Iterable[str] = None, data: bytes = None) -> str:
        """Record the current state as the trusted baseline for `node_id`."""
        if paths is not None:
            digest = self._hash_files(paths)
        elif data is not None:
            digest = self._hash_bytes(data)
        else:
            raise ValueError("Provide either paths or data")
        self._baselines[node_id] = digest
        return digest

    def verify(self, node_id: str, paths: Iterable[str] = None, data: bytes = None) -> ScanResult:
        """Compare current state against the registered baseline."""
        if node_id not in self._baselines:
            raise KeyError(f"No baseline registered for node '{node_id}'")
        if paths is not None:
            current = self._hash_files(paths)
        elif data is not None:
            current = self._hash_bytes(data)
        else:
            raise ValueError("Provide either paths or data")
        return ScanResult(baseline_hash=self._baselines[node_id], current_hash=current)

    def export_baselines(self) -> str:
        return json.dumps(self._baselines, indent=2)
