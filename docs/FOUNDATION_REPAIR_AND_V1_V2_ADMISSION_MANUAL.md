# SWI — Foundation Repair & V1 → V2 Admission Manual

**Author:** Keletso Ronald Mosidila — Trusts Motion  
**Status:** CONTROLLED REPAIR GATE  
**Rule:** Evidence before expansion.

## Current position (do not inflate)

### V1

Pipeline: `M03 → M02 → M05 → M06 → M07 → M09 → PipelineResult`

| Module | Status |
|--------|--------|
| 02 | **SEALED** |
| 03 | **SEALED** |
| 05 | **SEALED** |
| 06 | **SEALED** (lexical/cosine kernel; CI on `8a44c52`) |
| 07 | TRAINER integrity/persistence · **not kernel-sealed** |
| 09 | TRAINER integrity/persistence · **not kernel-sealed** |
| 01/04/08/10 | STANDALONE |
| 00 | Orchestrator · **not foundation-sealed** |
| **Foundation Seal 5** | **NOT READY** |

### V2 (`c58daaf`)

| Component | Status |
|-----------|--------|
| Kernel | IMPLEMENTED / TESTED / NOT SEALED |
| M11 | FIXTURE-TESTED / NOT SEALED |
| M12–22 | PROPOSED / DESIGN PENDING |

## Promotion rule

`PROPOSED → IMPLEMENTED → TESTED → CI VERIFIED → SEALED`  
No jumps. No architecture-as-evidence.

## Distinctions

Integrity is not validity · Tamper-evident is not tamper-proof · Authorization is not security  
Admission ≠ truth · Testing ≠ certification · Implementation ≠ seal

## Immediate order

1. Freeze baselines  
2. M06 exact-tip CI (done for `8a44c52`)  
3. Inspect M07 → decide kernel  
4. M07 tests/CI/decision record  
5. Inspect M09 → decide  
6. Review 01/04/08/10  
7. M00 integration evidence  
8. Claim audit · clean clone · Seal 5 record  
9. **Only if PASSED:** V1 Foundation Evidence Contract  
10. Repair M11 against real contract  
11. Freeze M12 · only then implement

## Forbidden

- Synthetic V1 evidence in M11  
- `verified: true` as proof  
- M12–22 implementation before M11 seal against real V1 export  
- V1 Modules 11–20  
- Universal safety / tamper-proof claims without evidence
