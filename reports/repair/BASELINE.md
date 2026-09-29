# SWI Repair Baseline — SWI-V1-Module-1-10

**Date:** 2026-09-29  
**Repository:** Kelronmos/SWI-V1-Module-1-10  
**Branch:** main  
**SHA:** `3e32d27f4830dbf3aa6b819e81c7fcde87c28f25`

## Rule

CLAIM → IMPLEMENTATION → TEST → RESULT → LIMITATION → NEXT ITERATION  
Do not convert unresolved conditions into PASS to improve scores.

## Scope

This baseline is **only** for `SWI-V1-Module-1-10`.

External audit findings about **Rust prototype**, **Firefly**, **Evidence Engine**, **V1.02 Cargo workspace (0 .rs files)**, and other public descriptions are **ecosystem OPEN** and are **not** fixed by changes in this repository alone.

## Audit items vs this repo

| Audit item | In this repo? | Observed |
|------------|---------------|----------|
| `test_execution_gate_allows_on_admit` | **No** | NOT_FOUND |
| `test_reconstruct` | **No** | NOT_FOUND |
| `verify_route_chain` vacuous PASS | **No** | NOT_FOUND |
| Registry SEALED vs CONTRACT_FROZEN | Token only | `CONTRACT_FROZEN` is a valid status string in admission_boundary |
| `jsonschema` undeclared | **No** | Declared in `requirements.txt`; must be installed |
| PYTHONPATH | Partial | Some scripts document `PYTHONPATH=.` |
| ZIP clutter | **Yes** | 2 zips at repo root (see hygiene) |

## Observed tests (this environment)

```text
pip install jsonschema
PYTHONPATH=. python -m pytest -q
# 375 passed in 26.09s
```

Without `jsonschema`: 2 collection errors (`tests/test_adversarial_contracts.py`, `tests/test_m00_m10_schema.py`).

## Residuals (unchanged)

| Item | Status |
|------|--------|
| FM-005–013 | OPEN |
| Universal Gate | NOT_PROVEN |
| Security Maze | NOT SEALED |
| Foundation Seal 5 | NOT READY |
| Production / legal | NOT CLAIMED |
| S9 cross-node | NOT_IMPLEMENTED (V3) |

## Hygiene (this repo)

- `swi_v1_part1_source.zip`
- `SWI_security_self_check_pilot.zip`

Classify before delete; do not remove if they hold unique source/evidence.

## Next iteration (priority)

1. Confirm CI green on tip for this repo  
2. Ecosystem: locate repos containing execution_gate / reconstruct / verify_route_chain  
3. Ecosystem: Rust exact-match + NaN fail-closed  
4. Ecosystem: claim/description alignment  
5. V3 for S9 / consequence gate — not mixed into sealed V1 history  

**SCORE: NOT_RECALCULATED** — no objective scoring rubric applied.
