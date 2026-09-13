# Module 03 — Context Sync — Zero-Ground Inspection

**Status:** INSPECTED · BASELINE RECORDED · **DECISION: MIGRATE** · NOT sealed  
**Commit inspected:** `7e5589f49273ee8786c2248e5170c06af8e71d38` (and prior main with same module03 source)  
**Rule:** No Module 03 code change until this record is accepted and migration is authorized.

---

## Evidence map

| Area | Location | Status |
|------|----------|--------|
| Implementation | `swi_core/module03_context_sync.py` | INSPECTED |
| Contract | Drafted from source (below) | DEFINED FROM CODE |
| Unit tests | `test_swi_core.py` (`test_context_sync_*`) | FOUND |
| Trainer / config tests | `test/test_trainer_config.py`, `test_swi_core.py` timestamp tests | FOUND |
| Configuration | `config_loader` DEFAULTS + `config/swi_config.yaml` `context_sync.staleness_seconds` | FOUND |
| Trainer integration | `module00_trainer.py` → `sync.record_turn` | FOUND |
| Kernel | — | MISSING |
| Failure halt | Trainer does not halt on stale/OOO | UNVERIFIED as enforcement |
| Documentation | this file + module docstring | FOUND |

Existence ≠ correctness. Kernel and pipeline halt on contract failure remain gaps.

---

## Entry point

| Field | Value |
|-------|--------|
| File | `swi_core/module03_context_sync.py` |
| Class | `ContextSync` |
| Operation | `record_turn(turn_id, timestamp=None) → SyncResult` |
| Callers | `Trainer.process` only (package path) |
| Callees | stdlib `datetime` |
| Side effect | Appends `Turn` to internal `_turns` |

---

## Ten answers from source

1. **Input:** `turn_id` (not validated); `timestamp` optional datetime or wall clock UTC.  
2. **Output:** `SyncResult(stale, out_of_order, gap_seconds)`.  
3. **State:** Stateful turn history.  
4. **Config:** `staleness_seconds` default 1800; Trainer loads from config.  
5. **Valid context:** Not content — temporal relationship only.  
6. **Stale:** `gap > staleness_seconds` (equal → not stale).  
7. **Invalid input:** No soft success path; type errors can raise.  
8. **Exceptions:** No `ModuleKernelError`; TypeError possible.  
9. **Downstream:** Result on `PipelineResult.sync`; **`allowed` not driven by stale**.  
10. **Tests:** staleness, out-of-order, config + explicit timestamps.

---

## Baseline (before any migration)

| Field | Value |
|-------|--------|
| Relevant tests | context/sync/timestamp/staleness filters | 
| Local result | Existing suite includes Module 03 functional tests — **PASS** on main (full suite previously 95+) |
| Kernel / halt tests | **ABSENT** |

Baseline failure: none recorded for functional paths. Evidence gap: contract enforcement + failure propagation.

---

## Smallest defensible contract (draft)

```text
INPUT: turn_id; timestamp optional datetime
PRE: if timestamp provided → must be datetime; optional turn_id type policy
OPERATION: compute gap/OOO/stale; append Turn
OUTPUT: SyncResult with bool/bool/finite float (gap may be negative if OOO)
POST: type/shape of SyncResult
FAILURE (kernel): type/shape contract → ModuleKernelError
NOT failure: stale=True or out_of_order=True alone (flags only)
LIMITATION: no content truth; no clock honesty; no pipeline block on stale
```

---

## Decision record

| Field | Value |
|-------|--------|
| **Decision** | **MIGRATE** |
| **Meaning** | Existing operation is valid; add ModuleKernel for type/shape pre/post; preserve flag semantics |
| **Not** | REBUILD (algorithm stays) · VERIFY-only (kernel missing) |
| **Reason** | Functional behaviour exists and is tested; no fail-closed input/result contract; Trainer cannot distinguish type failures from normal SyncResult flags without a kernel boundary |
| **Scope of change** | Wrap `record_turn`; optional ctor validation for `staleness_seconds`; Trainer halt only on `ModuleKernelError` |
| **Must not change** | Stale rule `>`; first-turn gap 0; always-append on success; stale ≠ `allowed=False` |

---

## Classification (missing evidence vs missing function)

| Case | Classification |
|------|----------------|
| Kernel pre/post | Functionality **MISSING** for enforcement |
| Stale/OOO detection | Functionality **EXISTS**, evidence **SUFFICIENT** for basic flags |
| Pipeline stop on stale | **Not required** by current product behaviour — do not invent |
| Invalid timestamp soft-accept | Not observed — TypeError path; harden with explicit pre-check |

---

## Gate before implementation

```text
INSPECTED ✓
BASELINE RECORDED ✓
DEPENDENCIES MAPPED ✓
CONTRACT DRAFTED ✓
FAILURE PATH IDENTIFIED ✓ (flags vs TypeError vs future kernel)
DECISION RECORDED ✓ MIGRATE
→ ONLY THEN code change
```

**Blocked until authorized:** Module 03 kernel code · Module 06 · Modules 11–19.

---

## Bounded language

Use: *reports temporal gap*; *flags out-of-order*; *config sets threshold*.  
Avoid: *understands context*; *validates truth*; *cannot be bypassed*; *stale always stops the pipeline*.
