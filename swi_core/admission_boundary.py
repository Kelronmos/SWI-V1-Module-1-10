"""Admission / claim boundary — executable anti-overclaim controls.

Governing rules (must remain true):

  DOCUMENTATION ≠ ADMISSION ≠ SEAL
  MODULE NUMBER = CONSTRUCTION REFERENCE (not authority)
  HASH ≠ AUTHORITY
  verified=true ≠ authorized ≠ executable
  OLD CI / OLD SEAL ≠ CURRENT TIP
  SYNTHETIC RECEIPT ≠ REAL UPSTREAM PRODUCTION

This module is a pure checker. It does not grant execution authority.
It only answers: is this claim admissible under the current evidence?
"""

from __future__ import annotations

from typing import Any, Mapping, Optional


# States that may never be self-asserted without a matching seal record + tip evidence.
SEALED_REQUIRES_EVIDENCE = frozenset({"SEALED", "ADMITTED", "SYSTEM_VERIFIED", "RELEASED"})

# States that block downstream execution paths.
BLOCKED_STATES = frozenset({"BLOCKED", "PROPOSED", "NOT ADMITTED", "NOT READY", "REJECTED"})


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
        # Explicitly not executable authority
        "execution_authority": False,
        "architectural_admission": False,
        "seal": False,
    }


def evaluate_claim(
    claim: Mapping[str, Any],
    *,
    seal_records: Optional[Mapping[str, Any]] = None,
    current_commit: Optional[str] = None,
    evidence_index: Optional[Mapping[str, Any]] = None,
) -> dict[str, Any]:
    """Evaluate whether a claim object is admissible.

    Parameters
    ----------
    claim:
        Candidate claim dict. Typical keys:
          module, status, source, seal_commit, ci_commit, verified,
          authorized, executable, upstream_receipts, evidence_sha256
    seal_records:
        Optional map of module_id -> seal record (must contain commit, evidence refs).
    current_commit:
        Tip commit SHA under evaluation. Required when seal/CI commit is present.
    evidence_index:
        Optional map of evidence identifiers that are known to exist.

    Returns a structured decision. Never silently returns True for authority.
    """
    if not isinstance(claim, Mapping):
        return _reject("CLAIM_NOT_A_MAPPING", observed=type(claim).__name__)

    seal_records = seal_records or {}
    evidence_index = evidence_index or {}

    module = claim.get("module") or claim.get("module_id")
    status = str(claim.get("status") or claim.get("state") or "").upper().strip()
    source = str(claim.get("source") or claim.get("claim_source") or "unknown").lower()

    # ------------------------------------------------------------------
    # Attack 2 / documentation injection
    # Documentation is never sufficient for seal or admission.
    # ------------------------------------------------------------------
    if source in {"documentation", "readme", "docs", "markdown", "comment"}:
        if status in SEALED_REQUIRES_EVIDENCE:
            return _reject(
                "DOCUMENTATION_IS_NOT_ADMISSION",
                module=module,
                status=status,
                detail="DOCUMENTATION ≠ ADMISSION ≠ SEAL",
            )

    # ------------------------------------------------------------------
    # Attack 1 — fake seal (status SEALED without seal record + tip evidence)
    # ------------------------------------------------------------------
    if status in SEALED_REQUIRES_EVIDENCE:
        if not module:
            return _reject("SEAL_CLAIM_MISSING_MODULE", status=status)
        record = seal_records.get(str(module))
        if not record:
            return _reject(
                "SEAL_WITHOUT_SEAL_RECORD",
                module=module,
                status=status,
                detail="SEALED requires an explicit seal record",
            )
        # Seal record must itself be non-empty and tip-bound when current_commit given
        seal_commit = record.get("commit") or record.get("seal_commit")
        if current_commit and seal_commit and seal_commit != current_commit:
            return _reject(
                "SEAL_COMMIT_MISMATCH",
                module=module,
                seal_commit=seal_commit,
                current_commit=current_commit,
                detail="OLD SEAL ≠ CURRENT IMPLEMENTATION",
            )

    # ------------------------------------------------------------------
    # Attack 3 — old CI substitution
    # ------------------------------------------------------------------
    seal_commit = claim.get("seal_commit") or claim.get("evidence_commit")
    ci_commit = claim.get("ci_commit") or claim.get("ci_success_commit")
    if current_commit and seal_commit and ci_commit:
        if seal_commit != current_commit and ci_commit == seal_commit:
            # Claiming current tip is sealed because an older commit was green
            return _reject(
                "OLD_CI_DOES_NOT_SEAL_NEW_COMMIT",
                seal_commit=seal_commit,
                current_commit=current_commit,
                ci_commit=ci_commit,
            )

    # ------------------------------------------------------------------
    # Attack 4 — module-number injection
    # Presence of a module number never grants architectural authority.
    # ------------------------------------------------------------------
    if module is not None and not status:
        # Bare module number with no status/evidence is only a construction reference
        return _accept(note="MODULE_NUMBER_IS_CONSTRUCTION_REFERENCE")

    # ------------------------------------------------------------------
    # Attack 5 — fake upstream receipt chain (synthetic hashes)
    # Valid SHA-256 strings alone do not prove real modules produced them.
    # ------------------------------------------------------------------
    upstream = claim.get("upstream_receipts") or claim.get("receipt_chain")
    if upstream is not None:
        if not isinstance(upstream, (list, tuple)):
            return _reject("UPSTREAM_RECEIPTS_NOT_A_SEQUENCE")
        for item in upstream:
            if not isinstance(item, Mapping):
                return _reject("UPSTREAM_RECEIPT_NOT_A_MAPPING")
            # Require provenance marker; pure hash strings are insufficient
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

    # ------------------------------------------------------------------
    # Attack 6 — hash laundering (semantic change + re-hash)
    # A newly calculated valid hash does not restore admissibility if the
    # payload diverges from the authorized evidence identity.
    # ------------------------------------------------------------------
    if claim.get("payload_modified") is True and claim.get("hash_recalculated") is True:
        return _reject(
            "HASH_LAUNDERING",
            detail="Recalculated hash after semantic change is not automatic trust",
        )

    # ------------------------------------------------------------------
    # Attack 7 — seal laundering (reuse sealed artifact under new module id)
    # ------------------------------------------------------------------
    if claim.get("rebound_from_module") and claim.get("original_seal_module"):
        if str(claim.get("rebound_from_module")) != str(claim.get("original_seal_module")):
            return _reject(
                "SEAL_DOMAIN_MISMATCH",
                original=claim.get("original_seal_module"),
                rebound=claim.get("rebound_from_module"),
                detail="Seal is bound to its original module domain",
            )

    # ------------------------------------------------------------------
    # Attack 8 — authority laundering (verified → authorized → executable)
    # ------------------------------------------------------------------
    if claim.get("verified") is True:
        if claim.get("authorized") is True or claim.get("executable") is True:
            # verified alone must never escalate
            if not claim.get("admission_artifact") and not claim.get("execution_authority_record"):
                return _reject(
                    "AUTHORITY_LAUNDERING",
                    detail="verified=true does not imply authorized or executable",
                )

    # ------------------------------------------------------------------
    # Attack 9 — blocked-path bypass
    # ------------------------------------------------------------------
    if status in BLOCKED_STATES:
        if claim.get("force_execute") is True or claim.get("executable") is True:
            return _reject(
                "BLOCKED_PATH_BYPASS",
                module=module,
                status=status,
                detail="Blocked/proposed state must not unlock execution",
            )

    # ------------------------------------------------------------------
    # Attack 10 — seal mutation (implementation changed after seal)
    # ------------------------------------------------------------------
    if current_commit and seal_commit and seal_commit != current_commit:
        if status in SEALED_REQUIRES_EVIDENCE:
            return _reject(
                "SEAL_MUTATION",
                seal_commit=seal_commit,
                current_commit=current_commit,
                detail="OLD SEAL ≠ CURRENT IMPLEMENTATION",
            )

    # Default: claim may be recorded as a claim only — never as authority.
    return _accept()


def is_module_sealed(
    module: str,
    *,
    seal_records: Mapping[str, Any],
    current_commit: Optional[str] = None,
    documentation_says_sealed: bool = False,
) -> dict[str, Any]:
    """Convenience: is this module sealed under executable rules?"""
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
