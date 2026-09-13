"""
Module 06: Drift Analyzer (The Tolerance Governor)

WHAT THIS ACTUALLY DOES:
Builds a simple bag-of-words frequency vector for a "baseline" set of
outputs and compares new outputs against it using cosine similarity. When
similarity drops below a threshold, it flags "drift" -- the new output's
vocabulary/topic distribution has shifted meaningfully from the baseline.

WHAT THIS DOES NOT DO:
Bag-of-words cosine similarity is a coarse, syntactic signal. It will not
catch semantic drift phrased with entirely different vocabulary, and it can
false-positive on legitimate topic changes. It is not a semantic or
embedding-based drift detector -- upgrading to one (e.g. with sentence
embeddings) is a natural extension but is not what is implemented here.
"""
from __future__ import annotations
import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Iterable, List


_TOKEN_RE = re.compile(r"[a-zA-Z0-9']+")


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text)]


def _vectorize(tokens: Iterable[str]) -> Counter:
    return Counter(tokens)


def _cosine_similarity(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    dot = sum(a[k] * b.get(k, 0) for k in a)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


@dataclass
class DriftResult:
    similarity: float
    drifted: bool


class DriftAnalyzer:
    """Module 06: bag-of-words drift detector against a baseline corpus."""

    def __init__(self, drift_threshold: float = 0.35):
        self.drift_threshold = drift_threshold
        self._baseline: Counter = Counter()

    def set_baseline(self, texts: Iterable[str]) -> None:
        vec = Counter()
        for text in texts:
            vec.update(_tokenize(text))
        self._baseline = vec

    def check(self, text: str) -> DriftResult:
        current = _vectorize(_tokenize(text))
        similarity = _cosine_similarity(self._baseline, current)
        return DriftResult(similarity=similarity, drifted=similarity < self.drift_threshold)
