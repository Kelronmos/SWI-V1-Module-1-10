# S9-E01 — Frozen V1 Residual Replay

**Audit target (frozen):** `0c8a2e662dc2b906a1166c091f37de6bd5c67299`  
**Repository:** Kelronmos/SWI-V1-Module-1-10  
**S9 status after this milestone:** `NOT_PROVEN`  
**Do not modify the frozen SHA to improve the report.**

---

## Configuration fork (decisive)

```text
require_admission=False  →  admission block skipped  →  op may form output  →  OPEN
require_admission=True   →  validate admission      →  reject or execute
```

Strict mode **exists** in the kernel. Default construction does **not** use it.  
Those are different claims.

---

## Inventory (authoritative at frozen SHA)

| Path | Entry | maze_protected | status |
|------|-------|----------------|--------|
| FM-001 | Trainer.process | true | TESTED |
| FM-002 | export_foundation_evidence | true | TESTED |
| FM-003 | sign_foundation_evidence | true | TESTED |
| FM-004 | SecurityMaze.evaluate_request | true | TESTED |
| **FM-005** | ModuleKernel.run default | **false** | **OPEN** |
| **FM-006** | SecurityProbe.scan | **false** | **OPEN** |
| **FM-007** | ContextSync.record_turn | **false** | **OPEN** |
| **FM-008** | RedactionEngine.redact | **false** | **OPEN** |
| **FM-009** | DriftAnalyzer.check | **false** | **OPEN** |
| **FM-010…013** | module constructors → ModuleKernel | **false** | **OPEN** |

`universal_gate`: **NOT_PROVEN**  
`security_maze_seal`: **NOT_READY**  
`foundation_seal_5`: **NOT_READY**

---

## Demonstrable pair (FM-005)

### Case A — residual reproduction (default)

```json
{
  "formation_path": "FM-005",
  "commit_sha": "0c8a2e662dc2b906a1166c091f37de6bd5c67299",
  "configuration": {
    "require_admission": false,
    "module_id": null,
    "expected_commit": null
  },
  "input": { "admission": null },
  "execution": {
    "admission_validation_entered": false,
    "operation_executed": true,
    "output_formed": true
  },
  "authority": { "maze_authority_granted": false },
  "inventory": { "status_before": "OPEN", "status_after": "OPEN" },
  "determination": {
    "residual_reproduced": true,
    "path_closed": false,
    "promotion": "NONE"
  }
}
```

### Case B — strict control (not closure)

```json
{
  "formation_path": "FM-005-STRICT-CONTROL",
  "commit_sha": "0c8a2e662dc2b906a1166c091f37de6bd5c67299",
  "configuration": { "require_admission": true },
  "input": { "admission": null },
  "execution": {
    "admission_validation_entered": true,
    "operation_executed": false
  },
  "result": { "exception": "AdmissionRequiredError" },
  "promotion": "NONE",
  "note": "Strict control confirms the branch exists; does not close FM-005 or Universal Gate"
}
```

---

## Non-equivalences (S9 must preserve)

```text
DEFAULT CHANGE           ≠  PATH CLOSURE
STRICT MODE EXISTS       ≠  STRICT MODE IS UNIVERSAL
TEST EXIT 0              ≠  PROVEN / SEALED
FM-005 FIXED (kernel)    ≠  FM-006…009 AUTO-CLOSED
execution PASS + OPEN    ≠  status promotion to TESTED
```

---

## Promotion rules (mechanical)

```text
IF require_admission == false
   AND admission == null
   AND operation_executed == true
THEN residual_reproduced = true
     path_status = OPEN
     promotion = NONE

IF require_admission == true
   AND admission == null
   AND AdmissionRequiredError observed
THEN strict_control_confirmed = true
     universal_gate = NOT_PROVEN
     fm_005_status = OPEN   # strict test does not overwrite inventory
```

---

## Dependency attribution (report only — do not collapse status)

```text
FM-005 = shared kernel admission-default dependency
FM-006 → uses ModuleKernel (constructor FM-010)
FM-007 → uses ModuleKernel (constructor FM-011)
FM-008 → uses ModuleKernel (constructor FM-012)
FM-009 → uses ModuleKernel (constructor FM-013)
```

Each path remains independently **OPEN** until its own closure evidence exists.

---

## S9 self-attack cases (required)

| Case | Injected lie | Expected determination |
|------|----------------|------------------------|
| 1 | Strict-mode PASS → label FM-005 TESTED | `STATUS_PROMOTION_REJECTED` |
| 2 | Evidence SHA-A vs audit target SHA-B | `EVIDENCE_SHA_MISMATCH` |
| 3 | `admission_validation_entered=true` while `require_admission=false` | `EXECUTION_EVIDENCE_INCONSISTENT` |
| 4 | Inventory OPEN → report SEALED | `STATUS_MISMATCH` |
| 5 | Valid artifact hash + status OPEN | remain **OPEN** |
| 6 | Modified bytes after hash | `INTEGRITY_FAILURE` |
| 7 | Missing execution record | `NOT_EXECUTED` |

---

## Milestone outputs (external audit preferred)

```text
swi-s9-external-audit/   # optional separate repo; mode READ_ONLY_EXTERNAL
reports/
  S9_DETERMINATION.json
  S9_AUDIT_REPORT.json
  S9_AUDIT_REPORT.pdf
evidence/FM-005 … FM-013/
integrity/hashes.sha256
replay/execution_manifest.json
```

Top-level determination must remain:

```json
{
  "s9_status": "NOT_PROVEN",
  "target_sha": "0c8a2e662dc2b906a1166c091f37de6bd5c67299",
  "fm_005": "OPEN",
  "fm_006": "OPEN",
  "fm_007": "OPEN",
  "fm_008": "OPEN",
  "fm_009": "OPEN",
  "fm_010": "OPEN",
  "fm_011": "OPEN",
  "fm_012": "OPEN",
  "fm_013": "OPEN",
  "independent_verification": "NOT_PROVEN"
}
```

---

## Construction (only after S9-E01 evidence)

```text
0c8a2e6  (frozen)
   └── hardening/fm-005-admission-closure   # new branch, not freeze mutation

CALLER INVENTORY → PATH INVENTORY → CLASSIFICATION → MIGRATION
  → STRICT ADMISSION → TESTS → CLEAN CI → NEW SHA → S9 REPLAY
```

First construction question: **Where are all ModuleKernel constructors and `.run` callers?**  
Not: “Can we flip the default to True?”

---

## Bottom line

```text
FM-005 current state     → OPEN
Default residual         → REPRODUCIBLE (Case A)
Strict mode              → AVAILABLE / TESTABLE (Case B)
Universal Gate           → NOT_PROVEN
S9                       → PRESERVE THE DISTINCTION
```

**Do not claim what the code cannot demonstrate.**
