"""
Module 06: Drift Analyzer (The Tolerance Governor)

WHAT THIS ACTUALLY DOES:
Builds a simple bag-of-words frequency vector for a "baseline" set of
outputs and compares new outputs against it using cosine similarity. When
similarity drops below a threshold, it flags "drift" -- the new output's
vocabulary/topic distribution has shifted meaningfully from the baseline.

Module Kernel:
  check() is fail-closed: input must be str; result must be DriftResult with
  finite similarity in [0, 1] and boolean drifted. drifted=True is advisory —
  not ModuleKernelError.

WHAT THIS DOES NOT DO:
Bag-of-words cosine similarity is a coarse, syntactic signal. It will not
catch semantic drift phrased with entirely different vocabulary, and it can
false-positive on legitimate topic changes. It is not a semantic or
embedding-based drift detector. Empty baseline yields similarity 0.0 (often
drifted); that is preserved semantics, not a kernel halt.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, List

from .module_kernel import CheckResult, ModuleKernel

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
    """Module 06: bag-of-words drift detector (kernel-enforced check contract)."""

    def __init__(self, drift_threshold: float = 0.35):
        if isinstance(drift_threshold, bool) or not isinstance(
            drift_threshold, (int, float)
        ):
            raise ValueError(
                f"drift_threshold must be int or float, got {type(drift_threshold).__name__}"
            )
        t = float(drift_threshold)
        if not math.isfinite(t):
            raise ValueError("drift_threshold must be finite")
        if t < 0.0 or t > 1.0:
            raise ValueError("drift_threshold must be in [0.0, 1.0]")
        self.drift_threshold = t
        self._baseline: Counter = Counter()
        self.kernel = ModuleKernel(
            name="module_06_drift",
            pre_checks=(self._input_is_string,),
            post_checks=(
                self._result_is_drift_result,
                self._similarity_is_valid,
                self._drifted_is_bool,
            ),
        )

    def set_baseline(self, texts: Iterable[str]) -> None:
        vec = Counter()
        for text in texts:
            vec.update(_tokenize(text))
        self._baseline = vec

    def check(self, text: str) -> DriftResult:
        return self.kernel.run(text, self._check_impl)

    def _input_is_string(self, value) -> CheckResult:
        if not isinstance(value, str):
            return CheckResult(
                name="input_is_string",
                passed=False,
                reason=f"expected str, got {type(value).__name__}",
            )
        return CheckResult(name="input_is_string", passed=True)

    def _result_is_drift_result(self, value) -> CheckResult:
        if not isinstance(value, DriftResult):
            return CheckResult(
                name="result_is_drift_result",
                passed=False,
                reason=f"expected DriftResult, got {type(value).__name__}",
            )
        return CheckResult(name="result_is_drift_result", passed=True)

    def _similarity_is_valid(self, value) -> CheckResult:
        if not isinstance(value, DriftResult):
            return CheckResult(
                name="similarity_is_valid",
                passed=False,
                reason="not a DriftResult",
            )
        s = value.similarity
        if isinstance(s, bool) or not isinstance(s, (int, float)):
            return CheckResult(
                name="similarity_is_valid",
                passed=False,
                reason=f"similarity must be numeric, got {type(s).__name__}",
            )
        sf = float(s)
        if not math.isfinite(sf):
            return CheckResult(
                name="similarity_is_valid",
                passed=False,
                reason="similarity must be finite",
            )
        if sf < 0.0 or sf > 1.0:
            return CheckResult(
                name="similarity_is_valid",
                passed=False,
                reason=f"similarity {sf} outside [0.0, 1.0]",
            )
        return CheckResult(name="similarity_is_valid", passed=True)

    def _drifted_is_bool(self, value) -> CheckResult:
        if not isinstance(value, DriftResult):
            return CheckResult(
                name="drifted_is_bool",
                passed=False,
                reason="not a DriftResult",
            )
        if type(value.drifted) is not bool:
            return CheckResult(
                name="drifted_is_bool",
                passed=False,
                reason=f"drifted must be bool, got {type(value.drifted).__name__}",
            )
        return CheckResult(name="drifted_is_bool", passed=True)

    def _check_impl(self, text: str) -> DriftResult:
        current = _vectorize(_tokenize(text))
        similarity = _cosine_similarity(self._baseline, current)
        return DriftResult(
            similarity=similarity,
            drifted=similarity < self.drift_threshold,
        )
