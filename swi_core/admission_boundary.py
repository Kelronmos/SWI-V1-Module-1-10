"""Admission / claim boundary — executable anti-overclaim controls.

Governing rules (must remain true):

  DOCUMENTATION ≠ ADMISSION ≠ SEAL
  MODULE NUMBER = CONSTRUCTION REFERENCE (not authority)
  HASH ≠ AUTHORITY
  verified=true ≠ authorized ≠ executable
  OLD CI / OLD SEAL ≠ CURRENT TIP
  SYNTHETIC RECEIPT ≠ REAL UPSTREAM PRODUCTION

This module is a pure checker plus an AdmissionDecision object.
It does not grant execution authority by itself.
Universal gate is NOT proven until every formation path requires a valid decision.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping, Optional


SEALED_REQUIRES_EVIDENCE = frozenset({"SEALED", "ADMITTED", "SYSTEM_VERIFIED", "RELEASED"})

BLOCKED_STATES = frozenset({"BLOCKED", "PROPOSED", "NOT ADMITTED", "NOT READY", "REJECTED"})

KNOWN_STATES = SEALED_REQUIRES_EVIDENCE | BLOCKED_STATES | frozenset(
    {
        "IMPLEMENTED",
        "UNIT_TESTED",
        "TESTED",
        "INTEGRATED",
        "VERIFIED",
        "CI_VERIFIED",
        "REVIEWED",
        "PLANNED",
        "DEFER",
        "HARDEN",
        "ADOPT",
        "BUILD",
        "ADAPTER",
        "CONTRACT_FROZEN",
        "UNKNOWN",
        "",
    }
)

_HEX_COMMIT_RE = re.compile(r"^[0-9a-fA-F]{7,64}$")
_MODULE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._\-]{0,63}$")


@dataclass(frozen=True)
class AdmissionDecision:
    """Non-boolean admission proof.

    A plain True is never sufficient. Callers must hold this object and
    pass is_valid_for(module, commit) before state formation when the
    formation path is under the universal-gate construction regime.
    """

    ok: bool
    module: Optional[str]
    commit: Optional[str]
    decision: str
    reason: str
    request_identity: Optional[str] = None
    evidence_identity: Optional[str] = None
    execution_authority: bool = False
    architectural_admission: bool = False
    seal: bool = False

    def is_valid_for(
        self,
        module: Optional[str] = None,
        commit: Optional[str] = None,
    ) -> bool:
        if not self.ok or not self.execution_authority:
            return False
        if module is not None and self.module is not None and str(module) != str(self.module):
            return False
        if commit is not None and self.commit is not None and str(commit) != str(self.commit):
            return False
        return True


def _reject(reason: str, **extra: Any) -> dict[str, Any]:
    out: dict[str, Any] = {
        "ok": False,
        "action": "REJECT",
        "reason": reason,
    }
    out.update(extra)
    return out


def _accept(note: str = "ADMISSIBLE_AS_CLAIM_ONLY") -> dict[str, Any]:
    return {
        "ok": True,
        "action": "ACCEPT_CLAIM_ONLY",
        "note": note,
        "execution_authority": False,
        "architectural_admission": False,
        "seal": False,
    }


def _require_boolish_true(value: Any, field: str) -> Optional[dict[str, Any]]:
    if value is True:
        return None
    if value is False or value is None:
        return None
    if value in ("true", "True", "TRUE", 1, "1", "yes", "YES"):
        return _reject(
            "BOOLEAN_STRING_CONFUSION",
            field=field,
            observed=repr(value),
            detail="Only Python True is accepted; string/int truthy values are rejected",
        )
    return None


def _validate_module_id(module: Any) -> Optional[dict[str, Any]]:
    if module is None:
        return None
    if not isinstance(module, str):
        return _reject("MODULE_ID_NOT_A_STRING", observed=type(module).__name__)
    stripped = module.strip()
    if not stripped:
        return _reject("MODULE_ID_EMPTY")
    if stripped != module:
        return _reject("MODULE_ID_HAS_SURROUNDING_WHITESPACE", observed=repr(module))
    if not _MODULE_ID_RE.match(module):
        return _reject("MODULE_ID_MALFORMED", observed=repr(module))
    return None


def _validate_commit(value: Any, field: str) -> Optional[dict[str, Any]]:
    if value is None:
        return None
    if not isinstance(value, str):
        return _reject("COMMIT_NOT_A_STRING", field=field, observed=type(value).__name__)
    if not value.strip():
        return _reject("COMMIT_EMPTY", field=field)
    if value != value.strip():
        return _reject("COMMIT_HAS_SURROUNDING_WHITESPACE", field=field)
    if not _HEX_COMMIT_RE.match(value):
        return _reject("COMMIT_NOT_HEX", field=field, observed=value[:80])
    return None


def evaluate_claim(
    claim: Mapping[str, Any],
    *,
    seal_records: Optional[Mapping[str, Any]] = None,
    current_commit: Optional[str] = None,
    evidence_index: Optional[Mapping[str, Any]] = None,
) -> dict[str, Any]:
    """Evaluate whether a claim object is admissible. Fail-closed on malformed inputs."""
    if not isinstance(claim, Mapping):
        return _reject("CLAIM_NOT_A_MAPPING", observed=type(claim).__name__)

    seal_records = seal_records or {}
    evidence_index = evidence_index or {}

    if not isinstance(seal_records, Mapping):
        return _reject("SEAL_RECORDS_NOT_A_MAPPING")
    if not isinstance(evidence_index, Mapping):
        return _reject("EVIDENCE_INDEX_NOT_A_MAPPING")

    err = _validate_commit(current_commit, "current_commit")
    if err:
        return err

    module = claim.get("module") if "module" in claim else claim.get("module_id")
    err = _validate_module_id(module)
    if err:
        return err

    raw_status = claim.get("status") if "status" in claim else claim.get("state")
    if raw_status is not None and not isinstance(raw_status, str):
        return _reject("STATUS_NOT_A_STRING", observed=type(raw_status).__name__)
    status = str(raw_status or "").upper().strip()
    if status and status not in KNOWN_STATES:
        return _reject("UNKNOWN_STATUS_TOKEN", status=status)

    source_raw = claim.get("source") or claim.get("claim_source") or "unknown"
    if not isinstance(source_raw, str):
        return _reject("SOURCE_NOT_A_STRING", observed=type(source_raw).__name__)
    source = source_raw.lower().strip()

    for field in (
        "verified",
        "authorized",
        "executable",
        "force_execute",
        "payload_modified",
        "hash_recalculated",
        "synthetic",
    ):
        if field in claim:
            err = _require_boolish_true(claim.get(field), field)
            if err:
                return err

    for field in ("seal_commit", "evidence_commit", "ci_commit", "ci_success_commit"):
        if field in claim:
            err = _validate_commit(claim.get(field), field)
            if err:
                return err

    if source in {"documentation", "readme", "docs", "markdown", "comment"}:
        if status in SEALED_REQUIRES_EVIDENCE:
            return _reject(
                "DOCUMENTATION_IS_NOT_ADMISSION",
                module=module,
                status=status,
                detail="DOCUMENTATION ≠ ADMISSION ≠ SEAL",
            )

    if status in SEALED_REQUIRES_EVIDENCE:
        if not module:
            return _reject("SEAL_CLAIM_MISSING_MODULE", status=status)
        record = seal_records.get(str(module))
        if not record or not isinstance(record, Mapping):
            return _reject(
                "SEAL_WITHOUT_SEAL_RECORD",
                module=module,
                status=status,
                detail="SEALED requires an explicit non-empty seal record",
            )
        if len(record) == 0:
            return _reject("SEAL_RECORD_EMPTY", module=module)
        seal_commit = record.get("commit") or record.get("seal_commit")
        err = _validate_commit(seal_commit, "seal_record.commit")
        if err:
            return err
        if current_commit and seal_commit and seal_commit != current_commit:
            return _reject(
                "SEAL_COMMIT_MISMATCH",
                module=module,
                seal_commit=seal_commit,
                current_commit=current_commit,
                detail="OLD SEAL ≠ CURRENT IMPLEMENTATION",
            )

    seal_commit = claim.get("seal_commit") or claim.get("evidence_commit")
    ci_commit = claim.get("ci_commit") or claim.get("ci_success_commit")
    if current_commit and seal_commit and ci_commit:
        if seal_commit != current_commit and ci_commit == seal_commit:
            return _reject(
                "OLD_CI_DOES_NOT_SEAL_NEW_COMMIT",
                seal_commit=seal_commit,
                current_commit=current_commit,
                ci_commit=ci_commit,
            )

    if module is not None and not status:
        return _accept(note="MODULE_NUMBER_IS_CONSTRUCTION_REFERENCE")

    upstream = claim.get("upstream_receipts") or claim.get("receipt_chain")
    if upstream is not None:
        if not isinstance(upstream, (list, tuple)):
            return _reject("UPSTREAM_RECEIPTS_NOT_A_SEQUENCE")
        for item in upstream:
            if not isinstance(item, Mapping):
                return _reject("UPSTREAM_RECEIPT_NOT_A_MAPPING")
            if item.get("synthetic") is True:
                return _reject(
                    "SYNTHETIC_UPSTREAM_RECEIPT",
                    detail="Valid hash strings do not establish real module production",
                )
            if not item.get("produced_by_module") and not item.get("evidence_ref"):
                return _reject(
                    "UPSTREAM_RECEIPT_MISSING_PROVENANCE",
                    detail="Receipt must bind to a real module or evidence_ref",
                )

    if claim.get("payload_modified") is True and claim.get("hash_recalculated") is True:
        return _reject(
            "HASH_LAUNDERING",
            detail="Recalculated hash after semantic change is not automatic trust",
        )

    if claim.get("rebound_from_module") and claim.get("original_seal_module"):
        if str(claim.get("rebound_from_module")) != str(claim.get("original_seal_module")):
            return _reject(
                "SEAL_DOMAIN_MISMATCH",
                original=claim.get("original_seal_module"),
                rebound=claim.get("rebound_from_module"),
                detail="Seal is bound to its original module domain",
            )

    if claim.get("verified") is True:
        if claim.get("authorized") is True or claim.get("executable") is True:
            if not claim.get("admission_artifact") and not claim.get("execution_authority_record"):
                return _reject(
                    "AUTHORITY_LAUNDERING",
                    detail="verified=true does not imply authorized or executable",
                )

    if status in BLOCKED_STATES:
        if claim.get("force_execute") is True or claim.get("executable") is True:
            return _reject(
                "BLOCKED_PATH_BYPASS",
                module=module,
                status=status,
                detail="Blocked/proposed state must not unlock execution",
                required_evidence=[
                    "REAL_UPSTREAM_INTEGRATION",
                    "ADMISSION_ARTIFACT",
                    "TIP_BOUND_SEAL_RECORD",
                ],
                proposed_construction_module=module,
            )

    if current_commit and seal_commit and seal_commit != current_commit:
        if status in SEALED_REQUIRES_EVIDENCE:
            return _reject(
                "SEAL_MUTATION",
                seal_commit=seal_commit,
                current_commit=current_commit,
                detail="OLD SEAL ≠ CURRENT IMPLEMENTATION",
            )

    return _accept()


def issue_admission_decision(
    claim: Mapping[str, Any],
    *,
    seal_records: Optional[Mapping[str, Any]] = None,
    current_commit: Optional[str] = None,
    evidence_index: Optional[Mapping[str, Any]] = None,
    grant_execution: bool = False,
    request_identity: Optional[str] = None,
    evidence_identity: Optional[str] = None,
) -> AdmissionDecision:
    """Turn evaluate_claim into an AdmissionDecision.

    grant_execution=True is only honored when evaluate_claim returns ok and
    the claim is not merely a construction reference. Claim-only acceptance
    never yields execution_authority.
    """
    result = evaluate_claim(
        claim,
        seal_records=seal_records,
        current_commit=current_commit,
        evidence_index=evidence_index,
    )
    module = None
    if isinstance(claim, Mapping):
        module = claim.get("module") or claim.get("module_id")
        if module is not None:
            module = str(module)

    if not result.get("ok"):
        return AdmissionDecision(
            ok=False,
            module=module,
            commit=current_commit,
            decision="REJECT",
            reason=str(result.get("reason") or "REJECTED"),
            request_identity=request_identity,
            evidence_identity=evidence_identity,
            execution_authority=False,
            architectural_admission=False,
            seal=False,
        )

    # ACCEPT_CLAIM_ONLY never becomes execution authority
    if result.get("action") == "ACCEPT_CLAIM_ONLY" and not grant_execution:
        return AdmissionDecision(
            ok=True,
            module=module,
            commit=current_commit,
            decision="ACCEPT_CLAIM_ONLY",
            reason=str(result.get("note") or "CLAIM_ONLY"),
            request_identity=request_identity,
            evidence_identity=evidence_identity,
            execution_authority=False,
            architectural_admission=False,
            seal=False,
        )

    if grant_execution and result.get("ok"):
        # Still refuse if evaluate_claim explicitly set execution_authority False
        # and action is claim-only without an admission_artifact on the claim.
        has_artifact = bool(
            isinstance(claim, Mapping)
            and (claim.get("admission_artifact") or claim.get("execution_authority_record"))
        )
        if result.get("action") == "ACCEPT_CLAIM_ONLY" and not has_artifact:
            return AdmissionDecision(
                ok=True,
                module=module,
                commit=current_commit,
                decision="ACCEPT_CLAIM_ONLY",
                reason="GRANT_EXECUTION_REFUSED_WITHOUT_ADMISSION_ARTIFACT",
                request_identity=request_identity,
                evidence_identity=evidence_identity,
                execution_authority=False,
                architectural_admission=False,
                seal=False,
            )
        return AdmissionDecision(
            ok=True,
            module=module,
            commit=current_commit,
            decision="ADMITTED",
            reason="ADMITTED_WITH_ARTIFACT",
            request_identity=request_identity,
            evidence_identity=evidence_identity,
            execution_authority=True,
            architectural_admission=True,
            seal=False,
        )

    return AdmissionDecision(
        ok=True,
        module=module,
        commit=current_commit,
        decision=str(result.get("action") or "ACCEPT_CLAIM_ONLY"),
        reason=str(result.get("note") or "CLAIM_ONLY"),
        request_identity=request_identity,
        evidence_identity=evidence_identity,
        execution_authority=False,
        architectural_admission=False,
        seal=False,
    )


def is_module_sealed(
    module: str,
    *,
    seal_records: Mapping[str, Any],
    current_commit: Optional[str] = None,
    documentation_says_sealed: bool = False,
) -> dict[str, Any]:
    claim = {
        "module": module,
        "status": "SEALED",
        "source": "documentation" if documentation_says_sealed else "programmatic",
    }
    return evaluate_claim(
        claim,
        seal_records=seal_records,
        current_commit=current_commit,
    )
