"""Regression: Module 09 must fail closed on malformed records (no crashes)."""
from __future__ import annotations

from swi_core.module09_audit_logger import AuditLogger


def test_audit_logger_normal_roundtrip(tmp_path):
    path = tmp_path / "audit.log"
    logger = AuditLogger(str(path))
    logger.log_event({"action": "login"})
    result = logger.verify_log()
    assert result.valid is True
    assert result.lines_checked == 1


def test_audit_logger_rejects_malformed_record(tmp_path):
    path = tmp_path / "audit.log"
    logger = AuditLogger(str(path))
    logger.log_event({"action": "login"})

    with open(path, "a") as f:
        f.write("{broken-json\n")

    result = logger.verify_log()
    assert result.valid is False
    assert result.broken_at_line == 2


def test_audit_logger_rejects_missing_hash_field(tmp_path):
    path = tmp_path / "audit.log"
    logger = AuditLogger(str(path))
    logger.log_event({"action": "ok"})

    with open(path, "a") as f:
        f.write('{"prev_hash": "0" * 64, "timestamp": 1.0, "event": {"x": 1}}\n')

    result = logger.verify_log()
    assert result.valid is False
    assert result.broken_at_line == 2


def test_audit_logger_rejects_truncated_line(tmp_path):
    path = tmp_path / "audit.log"
    logger = AuditLogger(str(path))
    logger.log_event({"action": "ok"})

    with open(path, "a") as f:
        f.write('{"prev_hash": "abc"\n')

    result = logger.verify_log()
    assert result.valid is False
