# MODULE 10 — PROPOSED Boundary / Evidence Handoff Contract

**Status:** PROPOSED / NOT ADMITTED  
**Date:** 2026-09-19  
**Authority:** Construction reference only. Does not admit the module into the evidence chain.

---

## Purpose

Investigate and (when evidence permits) implement a verifiable boundary handoff for evidence produced by the **canonical** SWI execution path.

This document defines the proposed contract against which future tests may be written. It does not claim that the contract is currently satisfied by live code.

---

## INPUT (proposed)

A verified evidence object produced by the canonical SWI execution path:

```text
M03 → M02 → M05 → M06 → M07 / M09 → PipelineResult
        → export_foundation_evidence() → FoundationEvidenceEnvelope
```

(or an explicitly documented successor of that path).

### Required properties (proposed)

1. Evidence object is structurally valid according to the canonical schema.
2. Required upstream evidence / hashes are present.
3. Hash relationships validate under the repository’s canonicalization contract.
4. Required gate / integrity status is satisfied.
5. Canonical serialization is used (reuse existing mechanism; do not invent a second one).
6. Payload digest is reproducible.

---

## OUTPUT (proposed)

An **integrity-bound evidence envelope** (SHA-256 digest over the canonical representation of the payload).

Preferred naming:

- integrity-bound evidence envelope
- hash-bound evidence envelope

**Do not** describe the output as:

- cryptographically sealed package
- cryptographically signed evidence
- non-repudiable record

unless a governed digital-signature layer is separately implemented and evidenced.

---

## FAILURE (proposed)

Any unmet invariant causes rejection with machine-readable evidence:

```json
{
  "status": "HALTED",
  "component": "MODULE_10_PROPOSED",
  "reason_code": "BOUNDARY_HASH_MISMATCH",
  "claim_status": "UNVERIFIED",
  "evidence_required": [
    "VALID_UPSTREAM_EVIDENCE",
    "MATCHING_PAYLOAD_HASH"
  ]
}
```

---

## NON-CLAIMS (mandatory)

This contract does **not** by itself establish:

- digital signature
- signer identity
- non-repudiation
- durable replay protection
- legal validity
- production key governance
- architectural admission
- Foundation Seal 5
- existence of an M07 → M08 → M09 → M10 chain

---

## Relationship to existing evidence authority

There must be **one** clearly defined canonical evidence authority.

Options (must be chosen explicitly before admission):

1. Existing `FoundationEvidenceEnvelope` remains terminal; Module 10 is a downstream handoff primitive.
2. Module 10 becomes the new terminal and the existing exporter is retired or wrapped.
3. Module 10 remains a research/prototype component with no production authority.

Silent dual-terminal designs are **blocked**.

---

## Canonicalization

Reuse the repository’s existing canonicalization contract.

Do not introduce a second independent `json.dumps(sort_keys=True, separators=(',', ':'))` definition unless a documented divergence and migration path exists.

---

## Replay / single-use semantics

In-memory `self._is_exported = True` is **per-instance duplicate-export prevention** only.

It is **not** durable replay protection.

Durable single-use requires a separate, specified, and tested persistent mechanism.

---

## Test classification (mandatory)

| Test type | May claim |
|-----------|-----------|
| Synthetic unit tests | UNIT CONTRACT TESTS only |
| Integration against real pipeline | INTEGRATION evidence |
| Tamper / negative against real evidence | INTEGRITY evidence |
| Architecture graph / admission checks | ARCHITECTURE evidence |

Isolated unit tests must never be described as “architecture verified”.

---

## Admission gate

See `docs/MODULE_10_ADMISSION_STATUS.md`.

**PROPOSED → IMPLEMENTED → UNIT-TESTED → INTEGRATED → VERIFIED → ADMITTED → SEALED**

No stage may be skipped because tests pass in isolation.
