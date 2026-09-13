"""Module 05 kernel integration — contract enforcement, not detection rewrite."""
import pytest

from swi_core.module05_redaction_engine import (
    RedactionEngine,
    RedactionMatch,
    RedactionResult,
)
from swi_core.module_kernel import ModuleKernelError


def test_normal_email_phone_still_redacted():
    engine = RedactionEngine()
    r = engine.redact("Contact me at ronie@example.com or 267 71234567.")
    assert isinstance(r, RedactionResult)
    assert "[REDACTED:EMAIL]" in r.redacted_text
    assert "ronie@example.com" not in r.redacted_text
    cats = {m.category for m in r.matches}
    assert "EMAIL" in cats


def test_precheck_non_string_impl_never_runs(monkeypatch):
    engine = RedactionEngine()
    called = {"n": 0}
    original = engine._redact_impl

    def wrapped(text):
        called["n"] += 1
        return original(text)

    monkeypatch.setattr(engine, "_redact_impl", wrapped)
    with pytest.raises(ModuleKernelError):
        engine.redact(12345)  # type: ignore[arg-type]
    assert called["n"] == 0


def test_precheck_oversized_input_rejected():
    engine = RedactionEngine()
    with pytest.raises(ModuleKernelError):
        engine.redact("x" * 100_001)


def test_postcheck_rejects_non_result(monkeypatch):
    engine = RedactionEngine()
    monkeypatch.setattr(engine, "_redact_impl", lambda text: "not-a-result")
    with pytest.raises(ModuleKernelError):
        engine.redact("hello")


def test_postcheck_rejects_unknown_category(monkeypatch):
    engine = RedactionEngine()

    def bad(text):
        return RedactionResult(
            redacted_text="x",
            matches=[
                RedactionMatch(category="SECRET", original="x", start=0, end=1)
            ],
        )

    monkeypatch.setattr(engine, "_redact_impl", bad)
    with pytest.raises(ModuleKernelError):
        engine.redact("hello")


def test_postcheck_rejects_overlapping_matches(monkeypatch):
    engine = RedactionEngine()

    def bad(text):
        return RedactionResult(
            redacted_text="abcdefghijklmn",
            matches=[
                RedactionMatch(category="EMAIL", original="abcdefghijklm", start=0, end=13),
                RedactionMatch(category="PHONE", original="jklmnop", start=10, end=17),
            ],
        )

    monkeypatch.setattr(engine, "_redact_impl", bad)
    with pytest.raises(ModuleKernelError):
        engine.redact("abcdefghijklmnop")


def test_empty_string_ok():
    r = RedactionEngine().redact("")
    assert r.redacted_text == ""
    assert r.matches == []


def test_exact_max_input_accepted():
    r = RedactionEngine().redact("z" * 100_000)
    assert isinstance(r.redacted_text, str)
    assert r.matches == [] or isinstance(r.matches, list)


def test_postcheck_rejects_invalid_span_start_gt_end(monkeypatch):
    engine = RedactionEngine()

    def bad(text):
        return RedactionResult(
            redacted_text="ab",
            matches=[
                RedactionMatch(category="EMAIL", original="ba", start=1, end=0),
            ],
        )

    monkeypatch.setattr(engine, "_redact_impl", bad)
    with pytest.raises(ModuleKernelError):
        engine.redact("ab")


def test_postcheck_rejects_zero_length_span(monkeypatch):
    engine = RedactionEngine()

    def bad(text):
        return RedactionResult(
            redacted_text="ab",
            matches=[
                RedactionMatch(category="EMAIL", original="", start=1, end=1),
            ],
        )

    monkeypatch.setattr(engine, "_redact_impl", bad)
    with pytest.raises(ModuleKernelError):
        engine.redact("ab")


def test_postcheck_rejects_negative_start(monkeypatch):
    engine = RedactionEngine()

    def bad(text):
        return RedactionResult(
            redacted_text="ab",
            matches=[
                RedactionMatch(category="EMAIL", original="a", start=-1, end=1),
            ],
        )

    monkeypatch.setattr(engine, "_redact_impl", bad)
    with pytest.raises(ModuleKernelError):
        engine.redact("ab")
