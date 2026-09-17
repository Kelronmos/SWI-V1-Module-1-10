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
| Live two-checkout CI | **DONE** — V2 workflow run **#50** / ID `35253244912` (2026-09-17); V1 producer tip at seal time `e0c6a521d7965c46c18464edc5dc6fbd8f9e254c` |
| Evidence authority for that run | See V2 `docs/M11_SEAL_RECORD.md` (not this file alone) |
| Foundation Seal 5 | **NOT READY** — envelope export still **unsigned** at source; primary architectural debt |
| CRTG | DESIGN PENDING (minimal v0 only when Seal 5 path exists) |
| Bulk M12–22 / M13–22 | **Not authorized** from V1 governance |

## Architecture freeze

```text
V1 → Foundation Evidence → serialize → M11 → AdmittedInput → Kernel
TaskEnvelope / CRTG = design track only until Seal 5
```

## Next (dependency order)

1. **Foundation Seal 5** — sign `FoundationEvidenceEnvelope` at export; pin verification public key in-repo; CI verifies signature.
2. Keep M12+ blocked until V2 independent evidence rediscovery + controlled module manuals.
3. Do **not** open network/Stage-2 Node Access Boundary before Seal 5.

Stale claim removed: “Live two-checkout CI: PENDING” is no longer accurate as of run `35253244912`.
