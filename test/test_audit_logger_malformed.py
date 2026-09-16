"""Regression: Module 09 must fail closed on malformed records (no crashes)."""
from __future__ import annotations

import json

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


def test_audit_logger_rejects_truncated_line(tmp_path):
    path = tmp_path / "audit.log"
    logger = AuditLogger(str(path))
    logger.log_event({"action": "ok"})

    with open(path, "a") as f:
        f.write('{"prev_hash": "abc"\n')

    result = logger.verify_log()
    assert result.valid is False
    assert result.broken_at_line == 2


def test_audit_logger_rejects_missing_hash_field(tmp_path):
    path = tmp_path / "audit.log"
    logger = AuditLogger(str(path))
    logger.log_event({"action": "ok"})

    with open(path, "a") as f:
        f.write(
            '{"prev_hash": "'
            + ("0" * 64)
            + '", "timestamp": 1.0, "event": {"x": 1}}\n'
        )

    result = logger.verify_log()
    assert result.valid is False
    assert result.broken_at_line == 2


def test_audit_logger_rejects_missing_event_field(tmp_path):
    path = tmp_path / "audit.log"
    logger = AuditLogger(str(path))
    logger.log_event({"action": "ok"})

    with open(path, "a") as f:
        f.write(
            '{"prev_hash": "'
            + ("0" * 64)
            + '", "timestamp": 1.0, "hash": "'
            + ("a" * 64)
            + '"}\n'
        )

    result = logger.verify_log()
    assert result.valid is False
    assert result.broken_at_line == 2


def test_audit_logger_rejects_non_object_line(tmp_path):
    path = tmp_path / "audit.log"
    logger = AuditLogger(str(path))
    logger.log_event({"action": "ok"})

    with open(path, "a") as f:
        f.write('"just-a-string"\n')

    result = logger.verify_log()
    assert result.valid is False
    assert result.broken_at_line == 2


def test_audit_logger_rejects_tampered_hash(tmp_path):
    path = tmp_path / "audit.log"
    logger = AuditLogger(str(path))
    logger.log_event({"action": "ok"})
    lines = path.read_text().strip().splitlines()
    rec = json.loads(lines[0])
    rec["hash"] = "0" * 64
    path.write_text(json.dumps(rec) + "\n")
    result = logger.verify_log()
    assert result.valid is False
    assert result.broken_at_line == 1
