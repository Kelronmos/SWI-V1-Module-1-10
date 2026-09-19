# Universal Gate — Entrypoint Map

**Repository:** Kelronmos/SWI-V1-Module-1-10  
**Analysis date:** 2026-09-19  
**Controls tip (admission_boundary introduced):** `9e72d69635d222402bf228e710935f09cf5822d0`  
**Tree inspected:** main tip including subsequent docs/security commits  
**Method:** Static inspection of `swi_core/` sources via GitHub API  
**Local `./scripts/verify.sh` / pytest:** **NOT EXECUTED** in this session

---

## Critical status (unchanged and correct)

```text
admission_boundary unit tests     → IMPLEMENTED / TESTED
Universal gate                    → NOT PROVEN
Bypass risk                       → DOCUMENTED + STRUCTURAL
Module 10 BoundaryExporter        → PROPOSED / NOT ADMITTED
Foundation Seal 5                 → NOT READY
```

A tested `evaluate_claim()` does **not** establish system protection if callers can form pipeline state, audit lines, or evidence envelopes without calling it.

---

## Proof target (not yet satisfied)

```text
∀ execution_paths:
    state_formation(path)  ⇒  admission(path) == ADMITTED

admission(path) != ADMITTED
    ⇒  Δstate == 0
    ⇒  Δexternal_side_effects == 0
```

Desired shape:

```text
request → callers ─┬─ execute path A ─┐
                   ├─ execute path B ─┤
                   ├─ execute path C ─┼→ ADMISSION BOUNDARY → state formation
                   ├─ seal path ──────┤         │
                   └─ export path ────┘         └→ REJECT → NO FORMATION
```

Current shape (observed):

```text
request → Trainer.process / ModuleKernel.run / export_* / module APIs
              │
              ▼
         STATE FORMATION   (no call to admission_boundary)

admission_boundary ← only adversarial unit tests
```

---

## Entrypoint inventory

| Entrypoint | File | Forms state / side effects? | Calls `admission_boundary`? |
|------------|------|----------------------------|-----------------------------|
| `ModuleKernel.run` | `swi_core/module_kernel.py` | Yes — runs operation after pre-checks | **NO** |
| `Trainer.process` | `swi_core/module00_trainer.py` | Yes — pipeline + M07 memory + M09 audit | **NO** |
| `export_foundation_evidence` | `swi_core/foundation_evidence.py` | Yes — envelope object | **NO** |
| `sign_foundation_evidence` | `swi_core/foundation_evidence.py` | Yes — signed envelope | **NO** |
| `require_no_authority_escalation` | `swi_core/authority.py` | Raises on bad fields; no admission_boundary | **NO** |
| `require_authorization_for_action` | `swi_core/authority.py` | Raises if auth missing | **NO** |
| `SecurityProbe.scan` | `module02_security_probe.py` | Probe result | **NO** |
| `ContextSync.record_turn` | `module03_context_sync.py` | Sync state | **NO** |
| `RedactionEngine.redact` | `module05_redaction_engine.py` | Redacted text | **NO** |
| `DriftAnalyzer.check` | `module06_drift_analyzer.py` | Drift result | **NO** |
| `MemoryValidator.append` | `module07_memory_validator.py` | In-memory chain | **NO** |
| `AuditLogger.log_event` | `module09_audit_logger.py` | On-disk log | **NO** |
| `evaluate_claim` | `admission_boundary.py` | Decision only (pure) | N/A (is the gate) |

**Conclusion:** Every production-style formation path inspected can run **without** `admission_boundary`. The gate is a **tested library**, not a **universal enforcement boundary**.

---

## What *is* enforced today (different layers)

| Layer | Mechanism | Scope |
|-------|-----------|--------|
| Per-module kernel | `ModuleKernel` pre/post checks | Only modules that wrap operations in ModuleKernel |
| Pipeline halt | `Trainer` catches `ModuleKernelError` | M02/M03/M05/M06 kernel failures; M07/M09 integrity |
| Authority field scan | `authority.py` forbidden keys | Only when callers invoke `require_*` |
| Claim anti-overclaim | `admission_boundary.evaluate_claim` | Only when callers invoke it (tests today) |

These are valuable and must not be confused with ∀-path admission.

---

## Recommended experiment sequence (local / CI)

```bash
git checkout 9e72d69635d222402bf228e710935f09cf5822d0   # or current tip
git status --short
git rev-parse HEAD
git rev-parse HEAD^{tree}

./scripts/verify.sh
python -m pytest -q test/adversarial/test_architecture_boundary_attacks.py
python -m pytest -q
```

Then attack the remaining boundary:

1. Enumerate every callable execution entrypoint (this doc is the starting inventory).  
2. Enumerate seal/admission/export paths.  
3. Trace whether each reaches `admission_boundary` (table above: **no**).  
4. Attempt direct invocation around the gate (`Trainer.process`, `export_foundation_evidence`, etc.).  
5. Malformed / Unicode / confusable module IDs at claim layer (partially covered in Phase 7 tests).  
6. Mutate authorization immediately before formation.  
7. Verify zero state mutation on rejection (**not applicable** until gate is on-path).  
8. Mutation-test each security predicate in `admission_boundary`.  
9. Re-run full suite after any wiring change.

---

## What would advance “Universal Gate”

Not more unit tests alone. One of:

1. **Wire** — single choke point: all `Trainer.process` / export / seal entrypoints call `evaluate_claim` (or equivalent) before formation; reject ⇒ no write.  
2. **Prove** — automated test that fails CI if a new public `swi_core` function forms state without going through the gate (import graph / AST guard).  
3. **Shrink surface** — mark direct module APIs as internal; only orchestrator is public.

Until then, status remains:

```text
UNIVERSAL_GATE = NOT PROVEN
BYPASS = STRUCTURAL DEFAULT PATH
```

---

## Non-claims

- This document is not a seal.  
- Static analysis is not a substitute for local `./scripts/verify.sh`.  
- Wiring the gate is a deliberate design change; it is **not** done in this commit.  
- Module 10 remains **PROPOSED / NOT ADMITTED**.  
- Foundation Seal 5 remains **NOT READY**.

**Do not claim what the code cannot demonstrate.**
