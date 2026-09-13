"""
Module 02: The Security Probe (Shadow Prompt Detection)

WHAT THIS ACTUALLY DOES:
Scans text against a set of regex heuristics associated with prompt-injection
and instruction-override attempts ("ignore previous instructions", role-play
jailbreak framing, base64-encoded payloads, zero-width character smuggling)
and returns a risk score plus which patterns fired.

Module Kernel (pilot):
  scan() is wrapped with fail-closed pre/post checks (input type/size,
  threshold range, ProbeResult contract). Detection logic is unchanged.

WHAT THIS DOES NOT DO:
This is pattern-matching, not semantic understanding. It will miss novel or
paraphrased injection attempts and will false-positive on legitimate text
that happens to match a pattern (e.g. a security researcher discussing these
exact phrases). It is one signal to feed into a larger review process, not a
standalone guarantee of safety. No heuristic-based filter can claim to be
"non-bypassable" -- that claim is not made here.
"""
from __future__ import annotations
import base64
import re
import unicodedata
from dataclasses import dataclass, field
from typing import List

from .module_kernel import CheckResult, ModuleKernel


_PATTERNS = {
    "instruction_override": re.compile(
        r"\b(ignore|disregard|forget)\b.{0,20}\b(previous|prior|above|earlier)\b.{0,20}\b(instructions?|prompt|rules?)\b",
        re.IGNORECASE,
    ),
    "role_override": re.compile(
        r"\byou are now\b|\bact as (?:an?|the)\b.{0,40}\bwith no (?:restrictions|filters|limits)\b",
        re.IGNORECASE,
    ),
    "system_prompt_exfil": re.compile(
        r"\b(reveal|print|repeat|show)\b.{0,20}\b(system prompt|instructions|hidden prompt)\b",
        re.IGNORECASE,
    ),
    "zero_width_smuggling": re.compile(r"[\u200b\u200c\u200d\ufeff]"),
}

_RISK_WEIGHTS = {
    "instruction_override": 0.5,
    "role_override": 0.4,
    "system_prompt_exfil": 0.4,
    "zero_width_smuggling": 0.3,
    "base64_payload": 0.2,
}

_MAX_INPUT_CHARS = 100_000


@dataclass
class ProbeResult:
    risk_score: float
    triggered: List[str] = field(default_factory=list)
    block_threshold: float = 0.5

    @property
    def blocked(self) -> bool:
        return self.risk_score >= self.block_threshold


def _input_is_string(value) -> CheckResult:
    return CheckResult(
        name="input_is_string",
        passed=isinstance(value, str),
        reason="input must be a string",
    )


def _input_has_reasonable_size(value) -> CheckResult:
    if not isinstance(value, str):
        return CheckResult(
            name="input_size",
            passed=False,
            reason="input is not a string",
        )
    return CheckResult(
        name="input_size",
        passed=len(value) <= _MAX_INPUT_CHARS,
        reason=f"input exceeds {_MAX_INPUT_CHARS} characters",
    )


def _result_is_probe_result(result) -> CheckResult:
    return CheckResult(
        name="probe_result_type",
        passed=isinstance(result, ProbeResult),
        reason="unexpected result type",
    )


def _risk_score_is_valid(result) -> CheckResult:
    if not isinstance(result, ProbeResult):
        return CheckResult(
            name="risk_score",
            passed=False,
            reason="unexpected result type",
        )
    score = result.risk_score
    ok = isinstance(score, (int, float)) and 0.0 <= float(score) <= 1.0
    return CheckResult(
        name="risk_score",
        passed=ok,
        reason="risk_score must be between 0 and 1",
    )


def _triggered_is_valid(result) -> CheckResult:
    if not isinstance(result, ProbeResult):
        return CheckResult(
            name="triggered",
            passed=False,
            reason="unexpected result type",
        )
    ok = isinstance(result.triggered, list) and all(
        isinstance(item, str) for item in result.triggered
    )
    return CheckResult(
        name="triggered",
        passed=ok,
        reason="triggered must be a list of strings",
    )


def _blocked_consistency(result) -> CheckResult:
    """If blocked, at least one pattern should have fired (score path consistency)."""
    if not isinstance(result, ProbeResult):
        return CheckResult(
            name="blocked_consistency",
            passed=False,
            reason="unexpected result type",
        )
    if result.blocked and not result.triggered and result.risk_score > 0:
        return CheckResult(
            name="blocked_consistency",
            passed=False,
            reason="blocked with positive score but empty triggered list",
        )
    return CheckResult(name="blocked_consistency", passed=True)


class SecurityProbe:
    """Module 02: heuristic shadow-prompt / injection detector."""

    def __init__(self, block_threshold: float = 0.5):
        if not isinstance(block_threshold, (int, float)):
            raise ValueError("block_threshold must be numeric")
        if not 0.0 <= float(block_threshold) <= 1.0:
            raise ValueError("block_threshold must be between 0 and 1")
        self.block_threshold = float(block_threshold)
        self.kernel = ModuleKernel(
            name="module_02_security_probe",
            pre_checks=[_input_is_string, _input_has_reasonable_size],
            post_checks=[
                _result_is_probe_result,
                _risk_score_is_valid,
                _triggered_is_valid,
                _blocked_consistency,
            ],
        )

    @staticmethod
    def _looks_like_base64_payload(text: str) -> bool:
        candidates = re.findall(r"[A-Za-z0-9+/]{24,}={0,2}", text)
        for c in candidates:
            try:
                base64.b64decode(c, validate=True)
                return True
            except Exception:
                continue
        return False

    def _scan_impl(self, text: str) -> ProbeResult:
        normalized = unicodedata.normalize("NFKC", text)
        triggered = []
        score = 0.0
        for name, pattern in _PATTERNS.items():
            if pattern.search(normalized):
                triggered.append(name)
                score += _RISK_WEIGHTS[name]
        if self._looks_like_base64_payload(normalized):
            triggered.append("base64_payload")
            score += _RISK_WEIGHTS["base64_payload"]
        score = min(score, 1.0)
        return ProbeResult(
            risk_score=score,
            triggered=triggered,
            block_threshold=self.block_threshold,
        )

    def scan(self, text: str) -> ProbeResult:
        return self.kernel.run(text, self._scan_impl)
