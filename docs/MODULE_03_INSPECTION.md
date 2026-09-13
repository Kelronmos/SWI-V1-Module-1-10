# Module 03 — Context Sync — Zero-Ground Inspection

**Status:** INSPECTED · CONTRACT DRAFTED FROM SOURCE · **NOT kernel-migrated** · **NOT sealed**  
**Inspection basis:** `swi_core/module03_context_sync.py` on main (post Module 05 seal)  
**Rule:** Do not modify Module 03 code until this inspection is accepted and a migration is authorized.

---

## 1. What the name does *not* prove

“Context Sync” is architectural language. Verification requires behaviour evidence, not the filename.

---

## 2. Answers from source (ten questions)

| # | Question | Evidence from code |
|---|----------|---------------------|
| 1 | **Input** | `record_turn(turn_id, timestamp=None)`. `turn_id` stored on `Turn` (intended int; **not validated**). `timestamp`: `Optional[datetime]`; `None` → `datetime.now(timezone.utc)`. |
| 2 | **Output** | `SyncResult(stale: bool, out_of_order: bool, gap_seconds: float)`. |
| 3 | **State** | Stateful: `self._turns: List[Turn]`. Each call **appends**; `history()` returns a copy. |
| 4 | **Configuration** | Ctor `staleness_seconds` default **1800.0**. Trainer sets via `config_loader` → `context_sync.staleness_seconds`. |
| 5 | **“Valid context”** | Module does **not** validate conversation content. It only compares successive timestamps. |
| 6 | **Stale** | `stale = gap > staleness_seconds` (**strict greater-than**). Gap from previous turn; first turn gap `0.0`, not stale. |
| 7 | **Invalid input** | No formal contract rejection. Non-datetime / naive-vs-aware mix → likely **TypeError**. Bad types are **not** converted to a soft “valid” SyncResult. |
| 8 | **Exceptions** | No custom `ModuleKernelError`. Type/compare errors can escape. |
| 9 | **Downstream** | Trainer always calls `record_turn` early in `process`. Result stored on `PipelineResult.sync`. **`allowed` is not set from `stale` / `out_of_order`** — security block is separate (Module 02). |
| 10 | **Existing tests** | `test_context_sync_flags_staleness`, `test_context_sync_flags_out_of_order`; Trainer config + explicit timestamp tests (`test_trainer_config` / `test_swi_core`). |

---

## 3. Boundary map

```text
Input (turn_id, timestamp?)
        ↓
[no type validation today]
        ↓
Compute gap / out_of_order / stale
        ↓
Append Turn (always, if no exception)
        ↓
SyncResult → Trainer.PipelineResult.sync
        ↓
Downstream modules run regardless of stale flag
```

**Detection vs enforcement:** Module 03 **detects** stale/out-of-order. Trainer does **not** halt the pipeline on those flags. Kernel migration must not invent “stale ⇒ stop pipeline” unless product policy is explicitly changed.

---

## 4. Minimum testable contract (draft — for future migration)

| Layer | Proposed rule (must match code unless behaviour change is intentional) |
|-------|---------------------------------------------------------------------|
| Pre | Prefer validate `timestamp is None or isinstance(timestamp, datetime)`; validate `turn_id` as int if required |
| Op | Existing gap / OOO / stale logic + append |
| Post | Result is `SyncResult`; bool fields are bool; `gap_seconds` is finite float (**may be negative** when out_of_order) |
| Ctor | Optional: reject non-numeric or negative `staleness_seconds` |
| Trainer | Kernel type/shape failure → halt; **stale=True alone remains a flag**, not ModuleKernelError |

Boundary to lock: `gap == staleness_seconds` → **not** stale (`>` only).

---

## 5. Bounded claims

**May claim (once tested):** reports temporal gap vs threshold; flags out-of-order timestamps; config can set threshold via Trainer.

**Must not claim:** context content is true; clock is honest; stale means pipeline blocked; “valid context” in a semantic sense.

---

## 6. Three-state snapshot

| Item | State |
|------|--------|
| Implementation exists | VERIFIED (source read) |
| Functional tests (stale / OOO / config) | VERIFIED (existing tests) |
| Kernel enforcement | **NOT IMPLEMENTED** |
| Trainer halt on M03 contract failure | **NOT IMPLEMENTED** |
| Full boundary / invalid-type matrix | **UNVERIFIED** |
| Module 03 seal | **NOT SEALED** |

---

## 7. Next authorized step

Only after this inspection is accepted:

1. Optional: add `docs/MODULE_03_CONTRACT.md` formalizing the draft table  
2. Kernel-wrap **without** changing detection meaning  
3. Negative + boundary tests (X−1 / X / X+1)  
4. Trainer halt **only** for contract failure (types/shape), not for `stale=True`  
5. CI → seal record  

**Do not** start Module 06 until Module 03 is sealed under the same discipline as Module 05.
