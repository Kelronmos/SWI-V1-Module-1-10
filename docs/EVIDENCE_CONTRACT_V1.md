# SWI V1 Evidence Contract

**Purpose:** Shared vocabulary for evidence maturity.  
**Status of this document:** CONSTRUCTION / REFERENCE  
**Does not grant seals, authority, or production readiness.**

---

## Maturity ladder (strict order)

```text
IMPLEMENTED
    ↓
TESTED
    ↓
LOCALLY VERIFIED
    ↓
CI VERIFIED
    ↓
INDEPENDENTLY VERIFIED
    ↓
SEALED
```

A later stage is never assumed from an earlier stage.

---

## Explicit non-equations

| Claim form | Not equivalent to |
|------------|-------------------|
| HASH | AUTHORITY |
| HASH | TRUTH |
| SIGNATURE | TRUTH |
| SIGNATURE | REPLAY PROOF |
| TEST PASS | SECURITY CERTIFICATION |
| CI PASS | PRODUCTION READINESS |
| SEALED | PRODUCTION READY |
| SEALED | REGULATORY APPROVAL |

---

## Allowed status tokens

PROPOSED  
IMPLEMENTED  
TESTED  
CI_VERIFIED  
INDEPENDENTLY_VERIFIED  
SEALED  
BLOCKED  
OPEN  
NOT_PROVEN  
NOT_IMPLEMENTED  
NOT_READY

Do not invent intermediate marketing labels.

---

## Formation-path rule

Every privileged construction, mutation, deserialization, or admission
surface must appear in the formation-path inventory with an FM-xxx ID.

If a path is not adequately tested, its status remains **OPEN**.
The inventory is a construction map, not a security certificate.

---

## Relation to existing contracts

This document is complementary to:

- `docs/CRYPTOGRAPHIC_EVIDENCE_CONTRACT_V1.md`
- `docs/formation_path_inventory.json`
- `docs/GOVERNANCE_LOCK.md`

It does not supersede them and does not change any frozen status.

---

## Freeze note

This file is part of the Phase 0–5 baseline commit.  
No Universal Gate, Seal 5, S9, or readiness upgrade is asserted here.
