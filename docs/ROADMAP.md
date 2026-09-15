# SWI Roadmap (locked)

**Governance:** `docs/GOVERNANCE_LOCK.md` · `docs/UPGRADE_AND_PROGRESSIVE_INTEGRATION_MANUAL.md`

## Constitutional rules

1. Advance by **validated dependency boundaries**, not module-count symmetry.  
2. A readiness **percentage never overrides** a failed critical dependency or integrity gate.

## Architecture (do not redesign this phase)

```text
V1 Foundation → Foundation Evidence → M11 → Kernel
                    ├── M12+ (sequential)
                    └── CRTG design track
```

## Priority 1 — V1 Foundation Seal path

M07 / M09 boundaries · M00 integration · adversarial · claim audit · clean-clone · exact-tip CI · `FOUNDATION_SEAL_5_RECORD`

**Foundation Seal 5: NOT READY**

## Priority 2 — V2 (after / alongside evidence, not bulk modules)

M11 + Kernel boundary proof → freeze

## Priority 3 — CRTG design only

TaskEnvelope · canonical bytes · cert profile · trust policy · key lifecycle · revocation · replay · failure codes · adversarial tests  
**No implementation rush.**

## Position

| Area | State |
|------|--------|
| V1 evidence seam | IMPLEMENTED / TESTED (unsigned) |
| Seal 5 | **NOT READY** |
| V2 M11 / Kernel | Progressing · not sealed |
| CRTG | Design track |
| M13–M22 | **Not bulk-built** |
| Other repos | Independent, contract-driven |
