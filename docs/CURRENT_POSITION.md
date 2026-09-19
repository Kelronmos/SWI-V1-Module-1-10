# Current SWI Position — 19 September 2026

**Governance:** dependency boundaries, not module-count symmetry.

## V1 (`SWI-V1-Module-1-10` → V1.1 / Modules 00–11)

| Item | State |
|------|--------|
| Tip | `2bab827b40dd444348592fe3a557c746e4ad3fdd` |
| Tip CI | Re-verify after docs push; prior tip `f1f6e266…` was **success** (run 35342332253) |
| Local pytest (deps installed) | **190 passed** on prior tip (2026-09-19 check) |
| Foundation evidence export | IMPLEMENTED / TESTED · unsigned |
| Authority boundary | IMPLEMENTED / TESTED · prior tip CI green · **not sealed** |
| Canonicalization | Tightened (NaN/Inf reject, golden vectors) |
| Foundation Seal 5 | **NOT READY** |
| Bidirectional return path | **Not in V1** |
| V4 lessons captured | `docs/V4_LESSONS_AND_EVIDENCE_DISCIPLINE.md` |

## V2 (`SWI-V2-Modules-11-22`)

| Item | State |
|------|--------|
| M11 | **SEALED** |
| M12 | FROZEN / controlled development pending gates |
| Bidirectional return path | **DESIGN only** — pre-R · NOT AUTHORIZED · invariants NOT TESTED |
| SCAR → Firefly | Policy frozen · NOT AUTHORIZED |

## V3 / V4 / V5

| Volume | Status |
|--------|--------|
| V3 | **Not present** as a public numbered volume in this account |
| V4 | Historical research prototype (June 2026 ZIP / TypeScript). Crypto marked SIMULATED. **Not** a foundation of V1 or V2. Lessons recorded in `docs/V4_LESSONS_AND_EVIDENCE_DISCIPLINE.md` |
| V5 | **Not present** as a public numbered volume |

See `docs/SWI_VERSION_MAP_AND_IMPROVEMENT_PATH.md` for the honest cross-version map.

## Next

1. Confirm tip CI green after this push.  
2. Prove foundation gates (Seal 5 path).  
3. Do not promote pre-R into formal modules without AUTHORIZED implementation + adversarial PROVEN evidence.  
4. Do not invent V3/V5 claims; open them only when real modules + tests exist.
