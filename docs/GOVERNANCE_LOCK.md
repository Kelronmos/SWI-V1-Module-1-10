# SWI Governance Lock

**Date:** 15 September 2026

## Rules

1. Advance by validated **dependency boundaries**, not module-count symmetry.  
2. Readiness **% never overrides** a failed critical gate.  
3. V1 produces a versioned evidence contract; V2 consumes **serialized** evidence — **not** `import` of V1.

## Status

| Item | State |
|------|--------|
| Cross-repo travel (local boundary) | **PROVEN** |
| Live two-checkout CI | **PENDING** |
| Foundation Seal 5 | **NOT READY** |
| CRTG | DESIGN PENDING |
| Bulk M13–22 | **Not authorized** |

## Architecture freeze

```text
V1 → Foundation Evidence → serialize → M11 → AdmittedInput → Kernel
TaskEnvelope / CRTG = design track only
```

Next: two-checkout proof + Seal 5 evidence — **not** another architecture layer.
