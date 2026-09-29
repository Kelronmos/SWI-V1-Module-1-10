# SWI External Source Admission — Status

**Date:** 2026-09-29  
**Tip lineage:** see `docs/TIP_CI_STATUS.md`

| Stage | State |
|-------|--------|
| SPECIFIED | **Yes** — `docs/SWI_EXTERNAL_SOURCE_ADMISSION_POLICY.md` |
| IMPLEMENTED | **Yes (bounded)** — `swi_core/source_admission/` |
| TESTED | **Yes (bounded)** — halt + replay adversarial suites |
| REPLAYABLE | **REPLAYABLE_BOUNDED** (this slice only) |
| PROVEN (beyond slice) | **NOT CLAIMED** |
| SEALED | **NOT CLAIMED** |
| Regulatory compliance | **NOT CLAIMED** |

## Halt slice

- Policy violation → `SourceAdmissionHalt`
- Protected operation is **not** invoked on HALT
- Side-effect counter remains **0** on HALT paths

## Replay slice — layered invalidity (not generic INVALID)

| Failure class | Meaning |
|---------------|---------|
| SERIALIZATION_INVALID | Canonical reconstruction failed |
| SCHEMA_INVALID | Required fields/types missing or malformed |
| HASH_MISMATCH | Recomputed digest ≠ recorded evidence_hash |
| ACCESS_CONTEXT_INVALID | Knowledge level / restricted-info boundary violated |
| SOURCE_MUTATED | Identity/hash/version differs from recorded |
| DECISION_MISMATCH | Re-evaluation differs from recorded decision |
| AUTHORITY_UNPROVEN | Continuation authority not demonstrated |

**Access dimension:** knowledge levels 0–4. Insufficient level → `REPLAY_LIMITED_BY_ACCESS_CONTEXT` (does **not** mean “original decision was false”).

**Violation path:** PAUSE/BLOCK → `ViolationReport` → 3 questions (what failed / consequence / continuation authority) → disposition. `CONTINUE` only with explicit `AUTHORIZED:` / `SCOPED:` authority; default **BLOCK** with `side_effects=0`.

**HASH ≠ AUTHORITY ≠ TRUTH** remains in claim language. A hash match proves byte–digest correspondence for recorded material only.

## What is still not claimed

- FM-005–013 closed
- Universal Gate PROVEN
- Foundation Seal 5 READY
- CRTG / signature-based cryptographic authority
- GDPR / CCPA / EU AI Act compliance
- Cross-node V3 replay under separated stores

## Code map

- `swi_core/source_admission/models.py`
- `swi_core/source_admission/decision.py`
- `swi_core/source_admission/halt.py`
- `swi_core/source_admission/evidence.py`
- `swi_core/source_admission/replay.py`
- `test/adversarial/test_source_admission_halt.py`
- `test/adversarial/test_source_admission_replay.py`

> Named ≠ Implemented · Implemented ≠ Tested · Tested ≠ Sealed · Sealed ≠ Authorized.

**Limitation text:** REPLAYABLE within the tested source-admission contract and evidence format; not proof of Universal Gate closure, legal compliance, or production-wide replayability.
