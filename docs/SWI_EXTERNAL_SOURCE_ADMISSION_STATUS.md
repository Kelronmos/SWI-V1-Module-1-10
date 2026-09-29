# SWI External Source Admission — Status

**Date:** 2026-09-29  
**Tip lineage:** see `docs/TIP_CI_STATUS.md`

| Stage | State |
|-------|--------|
| SPECIFIED | **Yes** — `docs/SWI_EXTERNAL_SOURCE_ADMISSION_POLICY.md` |
| IMPLEMENTED | **Yes (bounded)** — `swi_core/source_admission/` |
| TESTED | **Yes (bounded)** — halt + adversarial suite |
| REPLAYABLE | **Yes (bounded)** — `replay_admission` + adversarial replay suite |
| PROVEN (beyond slice) | **NOT CLAIMED** |
| SEALED | **NOT CLAIMED** |
| Regulatory compliance | **NOT CLAIMED** |

## What this slice proves

**Enforcement**
- Policy violation → `SourceAdmissionHalt`
- Protected operation is **not** invoked on HALT
- Side-effect counter remains **0** on HALT paths

**Replay (bounded)**
- Same source + same evidence → same decision and same `evidence_hash`
- Same HALT / same PASS evidence reproduced
- Modified source, tampered hash, licence/privacy/architecture change → `REPLAY_INVALID`
- Claimed authorization cannot turn a violation into PASS
- Missing evidence → `NOT_PROVEN`

## What this slice does **not** prove

- FM-005–013 closed
- Universal Gate PROVEN
- Foundation Seal 5 READY
- GDPR / CCPA / EU AI Act or any compliance conclusion
- Production-wide or cross-module replayability

## Code map

- `swi_core/source_admission/models.py`
- `swi_core/source_admission/decision.py`
- `swi_core/source_admission/halt.py`
- `swi_core/source_admission/evidence.py`
- `swi_core/source_admission/replay.py`
- `test/adversarial/test_source_admission_halt.py`
- `test/adversarial/test_source_admission_replay.py`

> Named ≠ Implemented · Implemented ≠ Tested · Tested ≠ Sealed · Sealed ≠ Authorized.

**Limitation text attached to every ReplayResult:**  
REPLAYABLE within the tested source-admission contract and evidence format; not proof of Universal Gate closure, legal compliance, or production-wide replayability.
