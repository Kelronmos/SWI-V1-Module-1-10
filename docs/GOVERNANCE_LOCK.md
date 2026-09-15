# SWI Governance Lock

**Date:** 15 September 2026  
**Status:** CONSTITUTIONAL FOR THIS PHASE

## Progression rule

> Advance when the required **dependency boundary** is validated — not because every repository has reached the same module number.

## Constitutional override rule

> A readiness percentage may authorize investigation or integration preparation, but it can **never** override a failed critical dependency or integrity gate.

Examples:

- Reported 94% but evidence seam broken → **NOT READY**
- Engine overall 70% but the **exact interface** M12 needs is implemented, tested, documented, reproducible → that **dependency** may be READY

Distinguish **project completeness** from **dependency readiness**.

## Do not change the architecture again this phase

```text
V1 Foundation → Seal 5 path → Foundation Evidence
        → V2 M11 → V2 Kernel
              ├── M12+ (one at a time)
              └── CRTG design (parallel, not bulk-code)
```

Supporting engines (math, Rust, Firefly, adapters) progress on **their contracts** — they do not impersonate V1 Modules 00–10.

## Priorities

| Priority | Work |
|----------|------|
| **1 — V1** | Seal 5 evidence: M07/M09/M00, adversarial, docs/claims, clean-clone, exact-tip CI, Seal 5 record |
| **2 — V2** | M11 + Kernel: invalid → HALT; valid → AdmittedInput; failed admission never reaches downstream; then **freeze** |
| **3 — Parallel** | CRTG **design** freeze only (envelope, profile, trust policy, lifecycle, failure codes, adversarial matrix) — no implementation rush |

## Explicit non-goals this phase

- Bulk M13–M22
- Redesigning the pipeline to absorb certificates into every module
- Claiming Seal 5 or CRTG complete without evidence

**Next move: prove the foundation, don't add another layer.**
