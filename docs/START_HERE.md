# START HERE — SWI Modules 00–10

## What this repository is

Reconstruction of **Modules 00–10** of Structured Workflow Intelligence (SWI): a Trainer-orchestrated pipeline with security probe, context sync, redaction, drift detection, memory validation, access auth, audit logging, and a resource-controlled subprocess boundary.

## What this repository is not

It is **not** a complete implementation of the full historical SWI textbook (CEK, SAD-DFU, Vector Memory / Scars, Alita, 46 modules, Sovereign Mesh). Those remain architectural or historical unless code and tests prove them.

## Authority hierarchy

```text
CURRENT CODE
     ↓
AUTOMATED TESTS
     ↓
REPRODUCIBLE RESULT
     ↓
DOCUMENTATION
     ↓
ARCHITECTURAL / HISTORICAL MATERIAL
```

If documentation conflicts with executable evidence: **stop and investigate**.

## Quick verify

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
./scripts/verify.sh
```

## Read next

1. `docs/IMPLEMENTATION_STATUS.md`
2. `docs/KNOWN_LIMITATIONS.md`
3. `docs/EVIDENCE_MATRIX.md`
4. `docs/TESTING_AND_VERIFICATION.md`
5. `docs/VOLUME_1_PART_2_MODULE_KERNEL_REBUILD_MANUAL.md`
6. `docs/FOUNDATION_MILESTONE.md`
7. Module 05: `MODULE_05_KERNEL_MIGRATION.md` · `MODULE_05_EVIDENCE.md` · `MODULE_05_SEAL_RECORD.md` (**SEALED**)
8. Module 03: `docs/MODULE_03_INSPECTION.md` — **inspected only; not sealed**
9. `docs/VOLUME_1_PART_3_FOUNDATION_COMPLETION_MANUAL.md` — Seal 5 path (11–19 blocked)

## Module Kernel status

- **02** SEALED · **05** SEALED  
- **03** inspected (see inspection doc); not kernel-migrated  
- Others: not yet migrated  
- Trainer halt on Module 02 / 05 kernel failure only (today)
