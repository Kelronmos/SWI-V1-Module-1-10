# SWI Universal Gate, Unauthorized-Flow Denial, Replay and Evidence

**Status:** DOCUMENTATION / HARDENING IN PROGRESS  
**Not:** Universal Gate PROVEN, FM-005 CLOSED, or Foundation Seal 5

## Governing rule

Never confuse: CLAIM, PROPERTY, EVIDENCE, ADMISSION, AUTHORIZATION, EXECUTION, RESULT.

Primary invariant:

```
Admission(request) != VALID  ⇒  ΔProtectedState = 0
Admission(request) != VALID  ⇒  ΔExternalSideEffects = 0
DENY  ⇒  HALT  ⇒  NO EXECUTION
```

Measure **side effects**, not only decision strings.

## Baseline (main, recorded)

| Field | Value |
|-------|-------|
| Repository | Kelronmos/SWI-V1-Module-1-10 |
| Main tip (recorded) | 080a78e55a18ab78fe49d85b5867ffa2622332b0 |
| Formal track tip | see formal/v47-discipline-patch |
| Universal Gate | **NOT PROVEN** |
| ModuleKernel default | `require_admission=False` |
| Direct M02–M09 APIs | **Ungated residual** |
| Foundation Seal 5 | **NOT READY** |

## Seven-gate path

```
G1 Formation paths closed (registry + gate)
G2 Production admission bypasses removed
G3 DENY enforced at execution adapters
G4 Scope / environment / policy revalidation
G5 Incident + mutation attacks
G6 TLA+ ↔ code ↔ tests ↔ evidence
G7 Foundation Seal 5
     ↓
   M12+ only after G7
```

## Non-implication (permanent regression)

module, version, role, weight, category, PASS, VERIFIED, evidence, credential possession,
approval, documentation, model claim, target reachability, hash equality
**must not** imply authority or execution.

## Decisive tests (must exist; status until run = NOT_TESTED)

1. Missing admission → reject → operation not called (`execution_count == 0`)
2. Direct module API without admission → DENY/HALT or residual remains OPEN
3. DENY then every adapter → zero consequential executions (INC-010)
4. Scope/env/policy hash mismatch → HALT
5. Positive path: valid admission → allowed operation + evidence

## Seal condition (excerpt)

Universal Gate leaves NOT_PROVEN only when: inventory complete, all production
formation paths gated, unauthorized execution = 0, direct bypasses rejected,
scope/env/policy revalidation proven, mutation tests fail correctly, replay
deterministic, positive controls work, CI green.

## Non-claims

This document is not evidence. Hash ≠ truth. Formal model ≠ production enforcement.
