"""
Module 02: The Security Probe (Shadow Prompt Detection)

WHAT THIS ACTUALLY DOES:
Scans text against a set of regex heuristics associated with prompt-injection
and instruction-override attempts ("ignore previous instructions", role-play
jailbreak framing, base64-encoded payloads, zero-width character smuggling)
and returns a risk score plus which patterns fired.

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


@dataclass
class ProbeResult:
    risk_score: float
    triggered: List[str] = field(default_factory=list)
    block_threshold: float = 0.5

    @property
    def blocked(self) -> bool:
        return self.risk_score >= self.block_threshold


class SecurityProbe:
    """Module 02: heuristic shadow-prompt / injection detector."""

    def __init__(self, block_threshold: float = 0.5):
        self.block_threshold = block_threshold

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

    def scan(self, text: str) -> ProbeResult:
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
        return ProbeResult(risk_score=score, triggered=triggered, block_threshold=self.block_threshold)
