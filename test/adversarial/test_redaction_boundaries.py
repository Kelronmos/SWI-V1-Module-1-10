"""Boundary tests for Module 05 — structured patterns only; not complete PII."""
import pytest

from swi_core.module05_redaction_engine import RedactionEngine
from swi_core.module_kernel import ModuleKernelError


def test_clean_text_unchanged():
    r = RedactionEngine().redact("Please help with my billing question.")
    assert r.matches == []
    assert "REDACTED" not in r.redacted_text


def test_whitespace():
    r = RedactionEngine().redact("  \n\t ")
    assert r.matches == []


def test_max_size_ok():
    r = RedactionEngine().redact("a" * 100_000)
    assert isinstance(r.redacted_text, str)


def test_over_limit():
    with pytest.raises(ModuleKernelError):
        RedactionEngine().redact("a" * 100_001)


def test_multiple_pii():
    text = "email a@b.co and omang 123456789 and phone 71234567"
    r = RedactionEngine().redact(text)
    cats = {m.category for m in r.matches}
    assert "EMAIL" in cats


def test_free_text_pii_not_claimed():
    """Limitation: free-text identifying info is outside structured patterns."""
    r = RedactionEngine().redact("My daughter attends Westwood Primary.")
    assert r.matches == []  # must not pretend we redacted this


def test_zero_width_does_not_crash():
    r = RedactionEngine().redact("hello\u200bworld")
    assert isinstance(r.redacted_text, str)
