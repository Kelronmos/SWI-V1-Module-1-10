"""Fixtures for V1 M00-M10 contract/schema tests.
Schema layer only — does not invent production validators.
Behavioural coverage remains in existing test harness.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.fixture
def valid_zero_base_payload():
    return {
        "module_id": "M01",
        "timestamp_utc": "2026-09-17T20:14:55Z",
        "payload_version": "1.0.0",
        "data": {
            "execution_mode": "DETERMINISTIC",
            "strict_validation": True,
            "parameters": {},
        },
    }


@pytest.fixture(scope="session")
def m00_m10_schema():
    schema_path = Path(__file__).resolve().parent.parent / "schemas" / "m00_m10_schema.json"
    if not schema_path.exists():
        pytest.fail(f"Schema missing: {schema_path}")
    with schema_path.open(encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def schema_validator(m00_m10_schema):
    jsonschema = pytest.importorskip("jsonschema")
    validator_cls = jsonschema.validators.validator_for(m00_m10_schema)
    validator_cls.check_schema(m00_m10_schema)
    return validator_cls(m00_m10_schema)
