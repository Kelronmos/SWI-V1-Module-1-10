# Security Maze V1 — Status

**Version:** security-maze-v1  
**Location:** inside SWI workflow (`swi_core/security_maze.py`)  
**Micro-kernel:** `ModuleKernel` with `require_admission=True` on maze formation path only  
**Admission engine:** `evaluate_claim` / `issue_admission_decision`  

## Classification

| Item | Status |
|------|--------|
| Architecture | DEFINED |
| Implementation | PARTIAL |
| Unit / adversarial tests | ACTIVE (`test/adversarial/test_security_maze_v1.py`) |
| **Seal** | **NOT SEALED** |
| Universal Gate | **NOT PROVEN** |

## What is wired

- G0 entry run + evidence trail
- G1 identity presence
- G2–G5 via existing `evaluate_claim` (structure, provenance, integrity, authority, blocked path)
- G6 boundary: claim-only cannot form state without admission when `operation` is supplied
- G7/G8 minimal pass/fail + NOT_RUN after failure (SM-V1-009)
- Formation only through **strict** `ModuleKernel(require_admission=True)`
- SM-V1-003 retry does not raise `privileged_access`

## Residual (explicit)

- Production modules still construct `ModuleKernel(require_admission=False)` by default
- Direct M02–M09 APIs remain ungated relative to Trainer / Maze
- Full sandbox runtime object, import/export revalidation, and cross-repo maze contract remain construction

## Non-claims

- Not universal security
- Not legal compliance
- Not production key custody
- Not Foundation Seal 5

## Principle

> There are many routes through SWI, but privileged execution under the Maze path must not skip validation. Residual routes are documented, not denied out of existence.

Flip Universal Gate / Maze seal only when every production-reachable formation path is independently demonstrated.
