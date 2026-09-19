# Current SWI Position — 19 September 2026

**Governance:** dependency boundaries, not module-count symmetry.

## V1 (`SWI-V1-Module-1-10` → V1.1 / Modules 00–11)

| Item | State |
|------|--------|
| Tip | `f1f6e266…` |
| Tip CI | **success** — run 35342332253 (`docs/TIP_CI_STATUS.md`) |
| Local pytest (deps installed) | **190 passed** (2026-09-19 check) |
| Foundation evidence export | IMPLEMENTED / TESTED · unsigned |
| Authority boundary | IMPLEMENTED / TESTED · tip CI green · **not sealed** |
| Canonicalization | Tightened (NaN/Inf reject, golden vectors) |
| Foundation Seal 5 | **NOT READY** |
| Bidirectional return path | **Not in V1** |

## V2 (`SWI-V2-Modules-11-22`)

| Item | State |
|------|--------|
| M11 | **SEALED** |
| M12 | FROZEN pending controlled gates |
| Bidirectional return path | **DESIGN only** — pre-R · NOT AUTHORIZED · invariants NOT TESTED |
| SCAR → Firefly | Policy frozen · NOT AUTHORIZED |

## Next

Prove foundation gates (Seal 5 path). Do not promote pre-R into formal modules without AUTHORIZED implementation + adversarial PROVEN evidence.
