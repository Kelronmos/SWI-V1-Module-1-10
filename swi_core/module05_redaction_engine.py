"""
Module 05: Redaction Engine (PII Neutralization)

WHAT THIS ACTUALLY DOES:
Detects and masks common structured PII patterns in text: email addresses,
phone numbers, credit-card-shaped numbers, and Botswana Omang ID numbers
(9 digits). Returns both the redacted text and a manifest of what was found
and where, for audit purposes.

Public entry point `redact()` is enforced by ModuleKernel:
  pre-checks → _redact_impl → post-checks → release.

WHAT THIS DOES NOT DO:
It cannot detect unstructured/free-text PII (e.g. "my daughter goes to
Westwood Primary") -- that requires NLP entity recognition, which is out of
scope for this module. Treat this as a first-pass structured-data filter,
not a complete PII removal guarantee. Kernel wrapping does not expand
detection coverage.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import List

from .module_kernel import CheckResult, ModuleKernel


@dataclass
class RedactionMatch:
    category: str
    original: str
    start: int
    end: int


@dataclass
class RedactionResult:
    redacted_text: str
    matches: List[RedactionMatch] = field(default_factory=list)


ALLOWED_CATEGORIES = frozenset({"EMAIL", "PHONE", "CREDIT_CARD", "BW_OMANG"})
MAX_INPUT_CHARS = 100_000

_RULES = {
    "EMAIL": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "PHONE": re.compile(r"\b(?:\+?\d{1,3}[ -]?)?(?:\(?\d{2,4}\)?[ -]?)?\d{3}[ -]?\d{4}\b"),
    "CREDIT_CARD": re.compile(r"\b(?:\d[ -]?){13,16}\b"),
    "BW_OMANG": re.compile(r"\b\d{9}\b"),
}

# Order matters: longer/more-specific patterns before shorter substring matches.
_ORDER = ["EMAIL", "CREDIT_CARD", "PHONE", "BW_OMANG"]


class RedactionEngine:
    """Module 05: structured PII detection and masking (kernel-enforced contract)."""

    def __init__(self) -> None:
        self.kernel = ModuleKernel(
            name="module_05_redaction",
            pre_checks=(
                self._input_is_string,
                self._input_size_is_valid,
            ),
            post_checks=(
                self._result_shape_is_valid,
                self._matches_are_valid,
            ),
        )

    def redact(self, text: str) -> RedactionResult:
        return self.kernel.run(text, self._redact_impl)

    # --- pre-checks ---

    def _input_is_string(self, value) -> CheckResult:
        if not isinstance(value, str):
            return CheckResult(
                name="input_is_string",
                passed=False,
                reason=f"expected str, got {type(value).__name__}",
            )
        return CheckResult(name="input_is_string", passed=True)

    def _input_size_is_valid(self, value) -> CheckResult:
        if not isinstance(value, str):
            return CheckResult(
                name="input_size_is_valid",
                passed=False,
                reason="size check requires str",
            )
        if len(value) > MAX_INPUT_CHARS:
            return CheckResult(
                name="input_size_is_valid",
                passed=False,
                reason=f"input length {len(value)} exceeds {MAX_INPUT_CHARS}",
            )
        return CheckResult(name="input_size_is_valid", passed=True)

    # --- post-checks ---

    def _result_shape_is_valid(self, value) -> CheckResult:
        if not isinstance(value, RedactionResult):
            return CheckResult(
                name="result_shape_is_valid",
                passed=False,
                reason=f"expected RedactionResult, got {type(value).__name__}",
            )
        if not isinstance(value.redacted_text, str):
            return CheckResult(
                name="result_shape_is_valid",
                passed=False,
                reason="redacted_text must be str",
            )
        if not isinstance(value.matches, list):
            return CheckResult(
                name="result_shape_is_valid",
                passed=False,
                reason="matches must be list",
            )
        return CheckResult(name="result_shape_is_valid", passed=True)

    def _matches_are_valid(self, value) -> CheckResult:
        if not isinstance(value, RedactionResult):
            return CheckResult(
                name="matches_are_valid",
                passed=False,
                reason="matches check requires RedactionResult",
            )
        prev_end = -1
        for i, m in enumerate(value.matches):
            if not isinstance(m, RedactionMatch):
                return CheckResult(
                    name="matches_are_valid",
                    passed=False,
                    reason=f"match[{i}] is not RedactionMatch",
                )
            if m.category not in ALLOWED_CATEGORIES:
                return CheckResult(
                    name="matches_are_valid",
                    passed=False,
                    reason=f"match[{i}] category {m.category!r} not allowed",
                )
            if m.start < 0 or m.end <= m.start:
                return CheckResult(
                    name="matches_are_valid",
                    passed=False,
                    reason=f"match[{i}] invalid span [{m.start},{m.end})",
                )
            if m.start < prev_end:
                return CheckResult(
                    name="matches_are_valid",
                    passed=False,
                    reason=f"match[{i}] overlaps or is out of order (start={m.start} < prev_end={prev_end})",
                )
            prev_end = m.end
        return CheckResult(name="matches_are_valid", passed=True)

    # --- implementation (unchanged detection meaning) ---

    def _redact_impl(self, text: str) -> RedactionResult:
        matches: List[RedactionMatch] = []
        claimed = [False] * len(text)

        for category in _ORDER:
            pattern = _RULES[category]
            for m in pattern.finditer(text):
                if any(claimed[m.start() : m.end()]):
                    continue
                matches.append(
                    RedactionMatch(
                        category=category,
                        original=m.group(),
                        start=m.start(),
                        end=m.end(),
                    )
                )
                for i in range(m.start(), m.end()):
                    claimed[i] = True

        matches.sort(key=lambda m: m.start)
        out = []
        cursor = 0
        for m in matches:
            out.append(text[cursor : m.start])
            out.append(f"[REDACTED:{m.category}]")
            cursor = m.end
        out.append(text[cursor:])
        return RedactionResult(redacted_text="".join(out), matches=matches)
