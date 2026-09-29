# Security Maze Repair — Baseline (Priority 0–1)

**Date:** 2026-09-29  
**Repository:** Kelronmos/SWI-V1-Module-1-10  
**Baseline SHA:** `bc33232c999551905cea374f952582f3e011861e`

## Status (unchanged by this work unless stated)

| Item | Status |
|------|--------|
| Security Maze V1 | **PARTIAL / NOT SEALED / NOT_READY** |
| Universal Gate | **NOT_PROVEN** |
| FM-001–004 | TESTED |
| FM-005–013 | **OPEN** |

## Priority 0 — Caller inventory (ModuleKernel)

| Caller | Kernel config | Admission on run? | Notes |
|--------|---------------|-------------------|--------|
| `SecurityProbe.__init__` | default `require_admission=False` | No | FM-006/010 |
| `ContextSync.__init__` | default False | No | FM-007/011; **mutates history** |
| `RedactionEngine.__init__` | default False | No | FM-008/012 |
| `DriftAnalyzer.__init__` | default False | No | FM-009/013 |
| `SecurityMaze._formation_kernel` | `require_admission=True` | Required when operation provided | Maze-internal only |
| Tests (many) | mix True/False | Varies | Includes OPEN attack docs |

## FM-005 architecture decision (Priority 1)

**Do not** globally set `require_admission=True` as default.

Reason: M02/M03/M05/M06 construct kernels without admission parameters on `scan` / `record_turn` / `redact` / `check`. Flipping the default would break formation APIs without a migration that threads admission through every public method and test.

**Chosen path:**

1. Keep compatibility default **False** → FM-005 remains **OPEN** (honest residual).
2. Add `ModuleKernel.for_privileged(...)` for gated construction.
3. Prove privileged path: unadmitted → `calls == []`.
4. Next iteration: migrate modules one-by-one (Priority 2–5) to privileged kernels + admission APIs.

## Tests observed (maze-focused)

```text
PYTHONPATH=. python -m pytest -q \
  test/adversarial/test_security_maze_fm_open_attacks.py \
  test/adversarial/test_security_maze_path_closure.py \
  test/adversarial/test_universal_gate_construction.py
# 25 passed
```

## Work queue

| Priority | Path | State |
|----------|------|--------|
| 1 | FM-005 | OPEN — factory added; default not flipped |
| 2–5 | FM-006–009 | OPEN — pending module admission APIs |
| 6 | FM-010–013 | OPEN |
| 7 | G7 Replay | OPEN (placeholder in maze) |
| 8–9 | SM-V1-005/013 | NOT_PROVEN / cross-repo |

## Non-claims

No Security Maze seal. No Universal Gate. No production trust.
