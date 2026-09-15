# SWI Governance Lock

**Date:** 15 September 2026

## Rules

1. Advance when the required **dependency boundary** is validated — not module-count symmetry.  
2. A readiness **percentage never overrides** a failed critical dependency or integrity gate.

## Freeze architecture this phase

```text
V1 → Foundation Evidence → M11 → AdmittedInput → Kernel
         (Track A — evidence)
TaskEnvelope → CRTG          (Track B — design only)
```

## Priorities

1. **Foundation Bridge / Seal 5 evidence** — see `FOUNDATION_BRIDGE_AND_SEAL5_REMEDIATION_MANUAL.md`  
2. V2 M11 + Kernel isolation  
3. CRTG **design** freeze — no implementation rush  

**No bulk M13–M22.** Next: prove the foundation, don't add another layer.
