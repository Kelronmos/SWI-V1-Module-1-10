# Security Maze V1 — Residual Privileged / Formation Paths

**Purpose:** Path-closure campaign inventory.  
**Rule:** Do not flip Universal Gate to PROVEN while any PRODUCTION residual remains unattacked or open.

## Classification legend

| Class | Meaning |
|-------|--------|
| PRODUCTION | Reachable in normal product use |
| COMPATIBILITY | Default left open for callers; maze/strict path is separate |
| CONSTRUCTION | Known incomplete; must not be treated as sealed |
| TEST_ONLY | Allowed only under tests |
| GATED | Requires admission / maze path |

## ModuleKernel defaults

| Location | `require_admission` | Class |
|----------|----------------------|--------|
| `module_kernel.py` constructor default | `False` | COMPATIBILITY residual |
| `security_maze.py` formation kernel | `True` | GATED (maze path) |
| M02 / M03 / M05 / M06 constructors | default `False` (no explicit True) | PRODUCTION residual |

## Public APIs (formation-adjacent)

| API | Gated by admission? | Class |
|-----|---------------------|--------|
| `Trainer.process(..., admission=)` | Yes (keyword-only) | GATED |
| `export_foundation_evidence` / sign helpers | Yes (`_require_admission`) | GATED |
| `SecurityProbe.scan` | No (kernel default False) | PRODUCTION residual |
| `ContextSync.record_turn` | No | PRODUCTION residual |
| `RedactionEngine.redact` | No | PRODUCTION residual |
| `DriftAnalyzer.check` | No | PRODUCTION residual |
| Direct `ModuleKernel.run` with default False | No | COMPATIBILITY residual |
| `SecurityMaze.evaluate_request` + operation | Yes (strict kernel) | GATED |

## Admission authenticity (SM-V1-004)

| Surface | Finding |
|---------|--------|
| `AdmissionDecision` with `execution_authority=False` | Strict kernel rejects |
| Wrong module / commit binding | Strict kernel rejects |
| `None` / `True` as admission | Strict kernel rejects |
| Duck-typed object with `is_valid_for` → True | **Can** pass strict kernel alone — residual authenticity surface |
| Claim path (`evaluate_claim`) | Independent of duck-typing; laundering still rejected |

**Implication:** Universal Gate cannot rest only on duck-typed `is_valid_for`. Provenance of admission (issuer + claim checks + binding) must be part of path closure.

## Next attack order

1. Enumerate every production `ModuleKernel(...)` call site
2. Attack each public scan/redact/check/record_turn without admission
3. Decide per site: wire admission, mark CONSTRUCTION, or mark TEST_ONLY
4. Regression-test closed sites
5. Re-evaluate Universal Gate only after inventory is empty of unexplained PRODUCTION residuals

## Explicit non-claims

- Security Maze V1 is **NOT SEALED**
- Universal Gate is **NOT PROVEN**
- Foundation Seal 5 is **NOT READY**
