# SWI Package Validation Report

**Package:** SWI-Evidence-Package-2026-10-29-v1.zip  
**Local path (agent workspace):** `/home/workdir/artifacts/SWI-Evidence-Package-2026-10-29-v1.zip`  
**SHA-256:** `c74a2348ae3547a7ae4b19889a20d3b7946c9e8319cd74e54415a84fc6a61dca`  
**Entries:** 32  
**Integrity (CRC + path checks):** PASS  

## Original evidence

- `claim_evidence_2026-10-29/`: FOUND  
- `CLAIM_TEST_REPLAY_MANIFEST.json` SHA-256: `d119968b23ecfdfef4ac3fb035d9f56461acad9286e223a86d213303898c815a` — **VERIFIED**  
- Original claim files copied unmodified into the ZIP  

## Claims included

| Claim | Commit | Prior targeted result |
|-------|--------|----------------------|
| CLAIM-ARCH-INT-001 | e0fc8b34… | 10 passed |
| CLAIM-ART-ID-001 | 1ec76400… | 9 passed |
| CLAIM-MATH-AUTH-001 | 8bd8c0c9… | 5 passed |

## Open gaps

- V2 empty-capability: NOT_RUN / NOT fixed  
- Firefly OTP still sets `replay_permission: true` on success alone (code inspection)  
- V4 `build_engine.py`: ABSENT at 2e8ced1e  
- Independent review: PENDING  

```
PROVEN = NO
SEALED = NO
AUTHORIZED = NO
PRODUCTION_AUTHORIZED = NO
```
