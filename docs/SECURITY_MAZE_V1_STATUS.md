# Security Maze V1 — Status

**Version:** security-maze-v1  
**Location:** inside SWI workflow (`swi_core/security_maze.py`)  
**Micro-kernel:** `ModuleKernel` with `require_admission=True` on maze formation path only  
**Admission engine:** `evaluate_claim` / `issue_admission_decision`  

## Seal record (honest)

```text
SECURITY MAZE V1
────────────────────────────────────────
Implementation       PARTIAL / TESTED
Targeted evidence    maze + architecture + authenticity tests
Sandbox              IMPLEMENTED / TESTED
Strict kernel path   IMPLEMENTED / TESTED
Retry invariant      SM-V1-003 TESTED
Admission authenticity
                     SM-V1-004 PARTIAL (duck-type residual documented)

Direct APIs          RESIDUAL (see SECURITY_MAZE_RESIDUAL_PATHS.md)
Default kernel       COMPATIBILITY SURFACE
Universal Gate       NOT PROVEN
Foundation Seal 5    NOT READY
Security Maze Seal   NOT READY

Next construction:
Enumerate → attack → close → regression-test
every privileged formation path.
```

## What is wired

- G0 entry run + evidence trail
- G1 identity presence
- G2–G5 via existing `evaluate_claim`
- G6 boundary: claim-only cannot form state without admission when `operation` is supplied
- G7/G8 minimal + NOT_RUN after failure (SM-V1-009)
- Formation only through **strict** `ModuleKernel(require_admission=True)` on the maze path
- SM-V1-003 retry does not raise `privileged_access`
- SM-V1-004 tests for forged / wrong-bound / claim-only / non-object admission

## Residual (explicit)

See `docs/SECURITY_MAZE_RESIDUAL_PATHS.md`.

## Non-claims

- Not universal security
- Not legal compliance
- Not production key custody
- Not Foundation Seal 5
- Duck-typed `is_valid_for` is **not** full admission authenticity

## Principle

> There are many routes through SWI, but privileged execution under the Maze path must not skip validation. Residual routes are documented, not denied out of existence.
