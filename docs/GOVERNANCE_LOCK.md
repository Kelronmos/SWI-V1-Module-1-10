# SWI Governance Lock (V1)

**Updated:** 17 September 2026

Supersedes the 15 September 2026 status row that listed live two-checkout CI as PENDING.

## Rules

1. Advance by validated **dependency boundaries**, not module-count symmetry.
2. Readiness **% never overrides** a failed critical gate.
3. V1 produces a versioned evidence contract; V2 consumes **serialized** evidence — **not** `import` of V1.
4. Ed25519 helper ≠ CRTG. Signature ≠ factual truth. Signature ≠ production key governance.

## Status

| Item | State |
|------|--------|
| Cross-repo travel (local boundary) | **PROVEN** |
| Live two-checkout CI | **DONE** — V2 run **#50** / ID `35253244912`; V1 tip at seal time `e0c6a521…` |
| Evidence authority for that run | V2 `docs/M11_SEAL_RECORD.md` |
| Foundation Seal 5 | **PATH OPEN / NOT SEALED** — optional sign/verify v0 wired; pin + CI verify pending (`docs/FOUNDATION_SEAL_5_STATUS.md`) |
| CRTG | DESIGN PENDING |
| Bulk M12–22 | **Not authorized** from V1 governance |

## Architecture freeze

```text
V1 → Foundation Evidence → serialize → M11 → AdmittedInput → Kernel
TaskEnvelope / CRTG = design track only until Seal 5 complete
```

## Next

1. CI verifies Seal 5 signatures; pin public key when ready.
2. M12+ remains governed by V2 controlled sequence (not this lock alone).
3. Do **not** open NAB Stage 2 before Seal 5 is complete.
