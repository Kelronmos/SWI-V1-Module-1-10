# V1 Tip CI Status

**Date:** 2026-09-19  
**Tip SHA:** `f1f6e266d4ac49698369752e4653b9c11e9a2d73`  
**Message:** `test(m08): boolean exp and non-string sub rejection cases`

## GitHub Actions

| Run ID | Conclusion | Workflow |
|--------|------------|----------|
| [35342332253](https://github.com/Kelronmos/SWI-V1-Module-1-10/actions/runs/35342332253) | **success** | CI |

Re-verify after every push: https://github.com/Kelronmos/SWI-V1-Module-1-10/actions

## Local suite (maintenance check)

```text
pip install -r requirements.txt
python -m pytest -q
→ 190 passed (Python 3.12)
```

Requires `requirements.txt` (including `jsonschema`). Pytest without install may fail collection on schema tests.

## Historical artifacts

| File | Label |
|------|--------|
| `test_run_log.txt` | **HISTORICAL** — 27-item session; not tip evidence |

## Explicit non-claims

| Item | Status |
|------|--------|
| Foundation Seal 5 | NOT READY |
| Authority boundary | IMPLEMENTED / TESTED / tip CI green — **not sealed** |
| Bidirectional verified return path | **Not implemented in V1** |
| CRTG / production key governance | NOT IMPLEMENTED |

## Recommended sequence

```text
CURRENT TIP → CI green
  → Authority + canonicalization evidence
  → Foundation Seal 5 path
  → Response return experiment on V2 as pre-R only
  → Adversarial tests → audit → formal module decision
```
