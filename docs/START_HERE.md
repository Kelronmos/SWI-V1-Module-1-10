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
5. `docs/VOLUME_1_PART_2_MODULE_KERNEL_REBUILD_MANUAL.md` — kernel rebuild path
6. `docs/FOUNDATION_MILESTONE.md` — what “finished foundation” means
7. `docs/MODULE_05_KERNEL_MIGRATION.md` — Module 05 kernel contract
8. `docs/VOLUME_1_PART_3_FOUNDATION_COMPLETION_MANUAL.md` — path to Seal 5 (11–19 blocked)

## Module Kernel status

- **Pilot:** Modules **02** and **05** are wrapped with pre/post checks.
- **Trainer:** kernel failure on Module 02 or 05 → halt, record reason, re-raise (no silent continue).
- **Not yet:** Full migration of modules 00–01, 03–04, 06–10 to ModuleKernel.
- **Future:** Global SWI Kernel registry — only after foundation Seal 5.
