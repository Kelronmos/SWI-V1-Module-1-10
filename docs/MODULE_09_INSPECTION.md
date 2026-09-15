# Module 09 — Audit Logger — Inspection Record

## Location

`swi_core/module09_audit_logger.py`

## What it does

- On-disk append-only **hash-chained** JSON lines  
- `log_event(event)` → SHA-256 over `{prev_hash, timestamp, event}`  
- `verify_log()` → first broken line or valid  

## What it does not do

- Not tamper-**proof** (filesystem rewrite + rehash possible)  
- Docstring correctly avoids “immutable” as absolute

## Production caller

`Trainer.process`: pre-verify → `log_event` → post-verify; failures → `ModuleKernelError` + best-effort halt record.

## Tests

`test_trainer_persistence_integrity.py` — corrupt audit, write failure, halt-recording failure does not create success.

## Decision

**TRAINER_INTEGRITY_ENFORCED · ModuleKernel wrap = DEFERRED**  
Same rationale as M07: production fail-closed path exists; forced kernel symmetry not required for this iteration.  
Direct API without Trainer remains a **known limitation**.

## Foundation Seal 5

M09 inspection complete. Still **NOT READY** overall until remaining checklist items (standalone reviews, M00 evidence, claim audit, clean-clone, Seal 5 record).
