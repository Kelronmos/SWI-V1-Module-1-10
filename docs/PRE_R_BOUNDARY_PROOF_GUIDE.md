# SWI Boundary Proof — Bidirectional Evidence, Authority & Return-Path Verification

| Field | Value |
|-------|--------|
| Repository | Kelronmos/SWI-V1-Module-1-10 |
| Stage | **Experimental / Pre-Module** |
| Namespace | **pre-R** |
| Status | **BUILD SPECIFICATION / DESIGN** |
| Implementation | **NOT AUTHORIZED** |
| Code | **ABSENT** |

## Proposition

> A result can travel back toward a requesting user while preserving defined evidence, integrity, provenance and authority scope, without the return path, UI, or intermediary backend creating new authority.

Not proving: SWI is secure/truthful; AI is safe; system is tamper-proof.

## Boundary propositions

| ID | Claim |
|----|--------|
| A | Information may cross without authority crossing |
| B | Backend result ≠ deliverable response |
| C | Returned authority ≤ original scope |
| D | UI ≠ authority source |
| E | Integrity ≠ semantic truth |

Preserve: `DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION`

## pre-R components

pre-R01 RequestBinding · pre-R02 AuthorityScope · pre-R03 EvidenceCarrier · pre-R04 IntegrityVerifier · pre-R05 ResponseEnvelope · pre-R06 ReturnGate · pre-R07 DestinationGate · pre-R08 TransformationGuard · pre-R09 DeliveryAdapter · pre-R10 BoundaryAudit

Isolation: `experimental/response_boundary/` only after authorization.

## Rules

```text
RETURN_SCOPE ⊆ ORIGINAL_AUTHORITY_SCOPE
UNKNOWN ⇏ ALLOW
REJECTED ⇏ DELIVERED
UI-generated authority = invalid
RESPONSE ⇏ automatic privileged action
→ NEW REQUEST → AUTHORITY CHECK
```

Return gate order: schema → binding → identity → evidence → integrity → authority → policy → destination → expiry → replay → transform → construct → seal → delivery.

## Prerequisites before code

Authority tip CI · canonicalization · Seal 5 path clarity · explicit PRE_R AUTHORIZED.

## Core adversarial test

> Alter only authority, recipient, evidence, integrity, or presentation of a valid result — can the system treat it as authorized without a new authorization event?

Expected: **NO** (via executable tests only).

## Doctrine

```text
INFORMATION MAY TRAVEL. AUTHORITY DOES NOT GROW BECAUSE IT TRAVELED.
CLAIM → IMPLEMENTATION → TEST → RESULT → LIMITATION → NEXT ITERATION
```

Index: `docs/PRE_R_INDEX.md`
