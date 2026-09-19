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
| M02 / M03 / M05 / M06 constructors | default `False` | PRODUCTION residual |

## Public APIs — attack results (path-closure)

| API | Without admission | Class | Test |
|-----|-------------------|--------|------|
| `Trainer.process(..., admission=)` | Rejected | GATED | existing trainer suite |
| `export_foundation_evidence` / sign | Rejected | GATED | foundation suite |
| `SecurityProbe.scan` | **Forms ProbeResult** | PRODUCTION residual | `test_residual_security_probe_scan_without_admission` |
| `ContextSync.record_turn` | **Mutates history** | PRODUCTION residual | `test_residual_context_sync_record_turn_without_admission` |
| `RedactionEngine.redact` | **Forms redacted output** | PRODUCTION residual | `test_residual_redaction_engine_redact_without_admission` |
| `DriftAnalyzer.check` | **Forms drift result** | PRODUCTION residual | `test_residual_drift_analyzer_check_without_admission` |
| `ModuleKernel.run` default False | Runs operation | COMPATIBILITY residual | universal-gate construction |
| `SecurityMaze.evaluate_request` + operation | Strict kernel | GATED | maze v1 suite |

**Do not** set every residual to `require_admission=True` without a migration plan for callers and Trainer orchestration.

## Admission authenticity (SM-V1-004)

| Surface | Finding |
|---------|--------|
| `execution_authority=False` | Strict kernel rejects |
| Wrong module / commit | Strict kernel rejects |
| `None` / `True` | Strict kernel rejects |
| Duck-typed `is_valid_for` → True | Can pass strict kernel alone |
| Claim path (`evaluate_claim`) | Independent; laundering rejected |

## State machine (maze layer)

| Attempt | Expected | Test |
|---------|----------|------|
| SANDBOXED → EXECUTING | INVALID_STATE_TRANSITION | `test_security_maze_state_machine` |
| HALTED → EXECUTING | INVALID_STATE_TRANSITION | same |
| UNVALIDATED → EXECUTING | INVALID_STATE_TRANSITION | same |
| Retry ×50 | authority stays false | same |

## Next attack order

1. ~~Enumerate public scan/redact/check/record_turn~~ (documented above)
2. Decide per residual: wire admission at Trainer-only boundary, or strict kernel, or CONSTRUCTION label
3. Factories / restore / replay / import
4. V2 AdmittedInput forgery (cross-repo)
5. Replay-after-mutation on admitted objects
6. Crash/recovery incomplete state

## Explicit non-claims

- Security Maze V1 is **NOT SEALED**
- Universal Gate is **NOT PROVEN**
- Foundation Seal 5 is **NOT READY**
- Residual API success in tests means **documented open surface**, not approval
