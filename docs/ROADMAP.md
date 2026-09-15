# SWI Roadmap (dependency-driven)

See: `docs/UPGRADE_AND_PROGRESSIVE_INTEGRATION_MANUAL.md`

## Constitutional rule

> A readiness percentage may authorize investigation or integration preparation, but it can **never** override a failed critical dependency or integrity gate.

Example: reported 94% with a broken evidence seam → **NOT READY**.  
Example: engine 70% overall, but the exact interface M12 needs is implemented, tested, documented, and verifiable → that **dependency** may be READY.

Advance when the **required dependency boundary** is validated — not because every repository reached the same module number.

## Do not change the architecture again

Current direction is locked:

```text
V1 Foundation → Foundation Evidence → V2 M11 → V2 Kernel
                      ├─ M12+ (one at a time)
                      └─ CRTG design (parallel, not bulk-coded)
```

Math / Rust / Firefly / adapters: **their** contracts only — they do not impersonate V1.

## Priority 1 — V1 Foundation Seal path

1. M06 CI evidence (recorded where available)  
2. M07 / M09 boundaries  
3. M00 integration  
4. Adversarial / failure testing  
5. Documentation / claim reconciliation  
6. Clean-clone verification  
7. Exact-tip CI evidence  
8. `FOUNDATION_SEAL_5_RECORD.md` + binary decision  

**Foundation Seal 5: NOT READY**

## Priority 2 — V2 M11 + Kernel (downstream)

Invalid evidence → HALT · valid → AdmittedInput · failed admission never reaches downstream · then freeze.

## Priority 3 — CRTG design only

Freeze TaskEnvelope, canonical bytes, cert profile, trust policy, key lifecycle, revocation, replay/expiry, failure codes, adversarial tests.  
**No implementation rush.**

## Anti-goals

Bulk M13–M22 · every repo must implement 00–10 · percentage overrides integrity · certificates as truth
