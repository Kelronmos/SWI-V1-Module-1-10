# THE SWI ARCHITECTURE — VOLUME 1 PART 2

## Module Kernel, Verification, Hardening & Rebuild Manual
### Modules 00–10

**Author:** Keletso Ronald Mosidila — Trusts Motion, Gaborone, Botswana — 2026
**Rule:** Do not advance to Modules 11–19 until the foundation gate passes.

### Authority hierarchy

current code → automated tests → reproducible result → documentation → architectural/historical material.

### Self-checking

```text
INPUT → PRE-CHECK → EXECUTE → POST-CHECK → HANDOFF
```

### Module Kernel

Implemented in `swi_core/module_kernel.py`.
Pilot: Module 02 Security Probe.

Migration order: 02 → 05 → 03 → 06 → 07 → 09 → 01 → 04 → 08 → 10 → 00 final.

### Seal levels

| Seal | Meaning |
|------|---------|
| 0 | Reconstruction exists |
| 1 | Core automated tests pass |
| 2 | Module kernel pilot passes |
| 3 | Adversarial and boundary testing passes |
| 4 | Clean environment and CI pass |
| 5 | Independent engineer can understand, run, test, and challenge the foundation |

Only Seal 5 authorizes Modules 11–19.

### Development law

Before work → verify. After work → verify again. If verification fails → do not hand off.

END OF VOLUME 1 — PART 2
