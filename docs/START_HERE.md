# START HERE — SWI Modules 00–10

CODE → TESTS → RESULT → DOCUMENTATION → ARCHITECTURE

**Live demonstration doctrine:** [`docs/LIVE_DEMONSTRATION_DOCTRINE.md`](LIVE_DEMONSTRATION_DOCTRINE.md)  
Volumes teach. This repository proves.

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
| Authority boundary | IMPLEMENTED / TESTED (see doctrine + tests) |

## Docs layout

Canonical documentation is under **`docs/`** only.

- Orientation: `docs/00_READ_ME_FIRST.md`
- **Live demos:** `docs/LIVE_DEMONSTRATION_DOCTRINE.md`
- Enhanced Part 3: `docs/VOLUME_1_PART_3_ENHANCED_FOUNDATION_COMPLETION_MANUAL.md`
- Integration matrix: `docs/MODULE_INTEGRATION_DEPENDENCY_MATRIX.md`
- Existing seals: `docs/MODULE_02_SEAL_RECORD.md`, `MODULE_03_SEAL_RECORD.md`, `MODULE_05_SEAL_RECORD.md`, `MODULE_06_SEAL_RECORD.md`
- Authority: `docs/AUTHORITY_BOUNDARY_MODEL.md`

Modules **11–19 as volume chapters** are not automatically live in this tree.
V2 admission / travel lives in `Kelronmos/SWI-V2-Modules-11-22`.

**Next engineering gates:** tip CI green · Lane B canonicalization · only then
new Part 2 module ports with tests — not manual-only claims.
