# Cross-Repository Travel Boundary

## Status (locked)

| Gate | State |
|------|--------|
| Local boundary (export JSON) | **PROVEN** |
| Live two-checkout CI | **PENDING** until Actions green |
| V2 M11 seal | **NOT SEALED** (see V2 closing manual) |
| CRTG | DESIGN PENDING |
| Foundation Seal 5 | **NOT READY** |

## Path

```text
Trainer → PipelineResult → export_foundation_evidence → JSON
  → V2 M11 → AdmittedInput → Kernel
```

M10 is **not** the handoff. V2 must not import this package.

## Producer for two-checkout

```bash
PYTHONPATH=. python scripts/export_travel_evidence.py --out evidence.json
```

Plan: `docs/TWO_CHECKOUT_CI_TEST_PLAN.md`  
V2 closing: upstream repo `docs/V2_CLOSING_AND_M11_SEAL_MANUAL.md`

## Integrity

Five covered fields; **`created_at` excluded** from digest.
