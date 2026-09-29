"""Evaluate external source against policy checks. Fail-closed.

Pull ≠ trusted. Scan ≠ approved. Warning ≠ authorization. Hash ≠ authority.
"""
from __future__ import annotations

import re
from typing import Optional

from swi_core.source_admission.evidence import evidence_hash_for_record
from swi_core.source_admission.models import (
    DecisionStatus,
    SourceAdmissionRecord,
    SourceDescriptor,
    Violation,
)

_HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")

# Minimal allow-list for this bounded slice (not a legal opinion).
_KNOWN_COMPATIBLE_LICENSES = frozenset(
    {
        "MIT",
        "Apache-2.0",
        "BSD-2-Clause",
        "BSD-3-Clause",
        "ISC",
        "0BSD",
    }
)


def evaluate_source(source: SourceDescriptor) -> SourceAdmissionRecord:
    """Run policy checks and return a record with PASS, WARNING, or HALT.

    Does not execute any protected operation. Does not grant authority.
    """
    record = SourceAdmissionRecord(source=source)
    basis: list[str] = []

    # --- Provenance ---
    if not source.origin or not str(source.origin).strip():
        record.violations.append(
            Violation(
                violation_id="SWI-SRC-PROVENANCE-001",
                rule_id="OSS-PROVENANCE-001",
                severity="HALT",
                description="Origin missing or empty",
            )
        )
        basis.append("PROVENANCE_FAIL")
    elif not source.provenance_verified:
        record.violations.append(
            Violation(
                violation_id="SWI-SRC-PROVENANCE-002",
                rule_id="OSS-PROVENANCE-002",
                severity="HALT",
                description="Provenance not verified",
            )
        )
        basis.append("PROVENANCE_UNVERIFIED")
    else:
        basis.append("PROVENANCE_OK")

    # --- Integrity ---
    if not source.content_hash or not _HEX64.match(source.content_hash):
        record.violations.append(
            Violation(
                violation_id="SWI-SRC-INTEGRITY-001",
                rule_id="OSS-INTEGRITY-001",
                severity="HALT",
                description="content_hash missing or not 64-hex SHA-256",
            )
        )
        basis.append("INTEGRITY_HASH_INVALID")
    elif source.presented_hash is not None and source.presented_hash != source.content_hash:
        record.violations.append(
            Violation(
                violation_id="SWI-SRC-INTEGRITY-002",
                rule_id="OSS-INTEGRITY-002",
                severity="HALT",
                description="Presented hash does not match recorded content_hash",
                evidence={
                    "content_hash": source.content_hash,
                    "presented_hash": source.presented_hash,
                },
            )
        )
        basis.append("INTEGRITY_MISMATCH")
    else:
        basis.append("INTEGRITY_OK")

    # --- License ---
    if not source.license_id or not str(source.license_id).strip():
        record.violations.append(
            Violation(
                violation_id="SWI-SRC-LICENSE-001",
                rule_id="OSS-LICENSE-001",
                severity="HALT",
                description="License unknown or missing",
            )
        )
        basis.append("LICENSE_UNKNOWN")
    elif source.license_id not in _KNOWN_COMPATIBLE_LICENSES:
        record.violations.append(
            Violation(
                violation_id="SWI-SRC-LICENSE-002",
                rule_id="OSS-LICENSE-002",
                severity="HALT",
                description=f"License not in bounded allow-list: {source.license_id}",
            )
        )
        basis.append("LICENSE_INCOMPATIBLE")
    else:
        basis.append("LICENSE_OK")

    # --- Privacy (bounded design constraint, not compliance claim) ---
    if not source.privacy_clear:
        record.violations.append(
            Violation(
                violation_id="SWI-SRC-PRIVACY-001",
                rule_id="PRIVACY-001",
                severity="HALT",
                description="Privacy obligations not cleared for this source",
            )
        )
        basis.append("PRIVACY_FAIL")
    else:
        basis.append("PRIVACY_OK")

    # --- Architecture boundary ---
    if source.target_boundary == "SWI_PRIVILEGED_EXECUTION" and not source.architecture_allowed:
        record.violations.append(
            Violation(
                violation_id="SWI-SRC-ARCHITECTURE-001",
                rule_id="ARCH-001",
                severity="HALT",
                description="Source not allowed on privileged SWI execution boundary",
            )
        )
        basis.append("ARCHITECTURE_FAIL")
    else:
        basis.append("ARCHITECTURE_OK")

    # --- Forged authority laundering ---
    if source.claimed_authorized and record.violations:
        record.violations.append(
            Violation(
                violation_id="SWI-SRC-AUTHORIZATION-001",
                rule_id="AUTH-001",
                severity="HALT",
                description="claimed_authorized cannot override open violations",
            )
        )
        basis.append("FORGED_AUTHORITY_REJECTED")

    halt_violations = [v for v in record.violations if v.severity == "HALT"]
    if halt_violations:
        record.decision = DecisionStatus.HALT
        record.status = "HALT"
    elif record.warnings:
        record.decision = DecisionStatus.WARNING
        record.status = "WARNING"
    else:
        record.decision = DecisionStatus.PASS
        record.status = "CHECK_PASSED"  # not ADMITTED-as-authority; bounded pass only

    record.decision_basis = basis
    record.evidence_hash = evidence_hash_for_record(record)
    return record
