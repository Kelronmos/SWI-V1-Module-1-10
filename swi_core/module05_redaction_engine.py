"""
Module 05: Redaction Engine (PII Neutralization)

WHAT THIS ACTUALLY DOES:
Detects and masks common structured PII patterns in text: email addresses,
phone numbers, credit-card-shaped numbers, and Botswana Omang ID numbers
(9 digits). Returns both the redacted text and a manifest of what was found
and where, for audit purposes.

WHAT THIS DOES NOT DO:
It cannot detect unstructured/free-text PII (e.g. "my daughter goes to
Westwood Primary") -- that requires NLP entity recognition, which is out of
scope for this module. Treat this as a first-pass structured-data filter,
not a complete PII removal guarantee.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import List


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


_RULES = {
    "EMAIL": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "PHONE": re.compile(r"\b(?:\+?\d{1,3}[ -]?)?(?:\(?\d{2,4}\)?[ -]?)?\d{3}[ -]?\d{4}\b"),
    "CREDIT_CARD": re.compile(r"\b(?:\d[ -]?){13,16}\b"),
    "BW_OMANG": re.compile(r"\b\d{9}\b"),
}

# Order matters: longer/more-specific patterns should be tried before
# shorter ones that could be a substring match (credit card before omang).
_ORDER = ["EMAIL", "CREDIT_CARD", "PHONE", "BW_OMANG"]


class RedactionEngine:
    """Module 05: structured PII detection and masking."""

    def redact(self, text: str) -> RedactionResult:
        matches: List[RedactionMatch] = []
        claimed = [False] * len(text)
        working = text

        for category in _ORDER:
            pattern = _RULES[category]
            for m in pattern.finditer(text):
                if any(claimed[m.start():m.end()]):
                    continue
                matches.append(
                    RedactionMatch(category=category, original=m.group(), start=m.start(), end=m.end())
                )
                for i in range(m.start(), m.end()):
                    claimed[i] = True

        matches.sort(key=lambda m: m.start)
        out = []
        cursor = 0
        for m in matches:
            out.append(text[cursor:m.start])
            out.append(f"[REDACTED:{m.category}]")
            cursor = m.end
        out.append(text[cursor:])
        return RedactionResult(redacted_text="".join(out), matches=matches)
