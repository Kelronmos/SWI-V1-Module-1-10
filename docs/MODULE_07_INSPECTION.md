# Module 07 — Memory Validator — Inspection Record

## Location

`swi_core/module07_memory_validator.py`

## What it does

- In-memory append-only **hash-chained** records (`MemoryRecord`)
- `append(payload)` → SHA-256 over canonical `{index, timestamp, payload, prev_hash}`
- `validate_chain()` → first break index or valid
- `tamper_for_testing` mutates payload without rehash (test helper only)

## What it does not do

- Not tamper-**proof** (operator with memory access can rebuild chain)
- Not distributed / not externally anchored
- Not semantic “scar” intelligence beyond structured records

## Production caller

`Trainer.process`:

1. `validate_chain` before append  
2. `append`  
3. `validate_chain` after append  
4. Any failure → `ModuleKernelError` + best-effort `_record_halt` (halt still primary)

## Existing tests

`test/test_trainer_persistence_integrity.py`:

- corrupt memory → fail-closed  
- append failure → fail-closed  
- halt-recording failure does not create success  

## Decision (Phase 3)

**TRAINER_INTEGRITY_ENFORCED · ModuleKernel wrap = DEFERRED**

Rationale:

1. Production path already fail-closes on integrity and persistence.  
2. Forcing ModuleKernel on every `append` for symmetry is not required for Seal 5 if Trainer boundary + negative tests hold.  
3. Direct-API callers remain unprotected — **KNOWN LIMITATION**, not silent security claim.  
4. Algorithm and tamper-evident language stay unchanged.

**Not sealed** as a ModuleKernel pilot.  
**Seal 5 still requires** documented decision (this file), persistence evidence, and M00 integration evidence — not forced migration.

## Next

M09 inspection with the same discipline.
