# START HERE — SWI Modules 00–10

CODE → TESTS → RESULT → DOCUMENTATION → ARCHITECTURE

```bash
python -m pip install -r requirements.txt
python -m pytest -q && ./scripts/verify.sh
```

| Module | Status |
|--------|--------|
| 02 | **SEALED** |
| 03 | **SEALED** |
| 05 | **SEALED** |
| 06 | **KERNEL-ENFORCED** · CI seal pending |
| 00 | Orchestration + halt; not foundation-sealed |
| 01, 04, 07–10 | Not kernel-migrated |

## Docs layout

Canonical documentation is under **`docs/`** only.

- Orientation: `docs/00_READ_ME_FIRST.md`
- Enhanced Part 3: `docs/VOLUME_1_PART_3_ENHANCED_FOUNDATION_COMPLETION_MANUAL.md`
- Integration matrix: `docs/MODULE_INTEGRATION_DEPENDENCY_MATRIX.md`
- Existing seals: `docs/MODULE_02_SEAL_RECORD.md`, `MODULE_03_SEAL_RECORD.md`, `MODULE_05_SEAL_RECORD.md`, `MODULE_06_SEAL_RECORD.md`

Modules **11–19 BLOCKED** until Foundation Seal 5.

**Next engineering gate:** CI green on Module 06 complete tip → M06 SEAL → inspect Module 07 (do **not** re-migrate Module 03).
