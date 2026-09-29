# V3 Start Freeze Gate

**Freeze date:** 2026-09-29  
**Machine-readable record:** `docs/V3_START_FREEZE.json`  
**V3 started:** **No** — this document freezes the boundary; it does not open V3 implementation.

> **Rule:** V3 must not rewrite historical V1 evidence.  
> V1 is the evidence of what existed. V3 is evidence of what changed.

---

## Baseline hierarchy

```text
V1 ORIGINAL BASELINE
  7f40a19b2b2f554ca7ea5adebd568b7fcfdc99b5
  (docs/BASELINE_FREEZE.md — 2026-09-15)
        ↓
V1 FROZEN AUDIT TARGET
  0c8a2e662dc2b906a1166c091f37de6bd5c67299
  (docs/S9_E01_FROZEN_V1_RESIDUAL_REPLAY.md)
  Do not modify the frozen SHA to improve the report.
        ↓
V1 PATH-CLOSURE / GEOMETRY HISTORY
  path_closure_baseline 0e15fc96791cc97ab712dcdc1b76aab6dc66ee7e
  formation inventory blob 6ecba6948e226f0d79dfe87550d92892fbec607e
        ↓
V2 ADMISSION BASELINE
  c58daaf3f8ea8a12e436eb71e571bea44ff05634
  (docs/BASELINE_FREEZE.md)
        ↓
PRE-V3 MAIN TIP (this freeze)
  d2cab7aa2eab1fd95332bc472779916385648183
  Includes External Source Admission bounded slice (IMPLEMENTED/TESTED).
  Does not close FM-005–013.
        ↓
V3 START (not yet)
  new branch + new SHA + new evidence only
```

These are different freeze points with different purposes. Do not collapse them.

---

## What must NOT be changed once V3 starts

| Artifact | Treatment |
|----------|-----------|
| V1 frozen SHA `0c8a2e6…` | **NEVER rewrite** |
| `docs/S9_E01_FROZEN_V1_RESIDUAL_REPLAY.md` | Preserve permanently |
| Path-closure baseline `0e15fc9…` | Preserve as V1 evidence |
| `docs/formation_path_inventory.json` V1 geometry | Preserve; V3 uses successor file if needed |
| M02 / M03 / M05 / M06 bounded seal evidence + limitations | Preserve exact evidence |
| `docs/GOVERNANCE_LOCK.md` | Preserve governing decision history |
| `docs/BASELINE_FREEZE.md` | Preserve historical values |

The configuration distinction in S9 must survive any V3 improvement:

```text
require_admission=False  → residual OPEN (reproducible)
require_admission=True   → strict control exists (≠ universal closure)
```

---

## V1 geometry snapshot at this freeze

| Band | Status |
|------|--------|
| FM-001 – FM-004 | **TESTED** |
| FM-005 – FM-013 | **OPEN** |
| Universal Gate | **NOT_PROVEN** |
| Security Maze | **NOT_READY** |
| Foundation Seal 5 | **NOT READY** |
| External Source Admission | **IMPLEMENTED / TESTED (bounded)** — does not close V1 residuals |
| Replay engine | **NOT IMPLEMENTED/TESTED** |
| Legal/regulatory compliance | **NOT CLAIMED** |

---

## What V3 may change (with new evidence only)

FM-005–013, Universal Gate, replay engine, External Source Admission extensions, execution adapters, Foundation Seal 5, CRTG, V3 architecture.

Process:

```text
V1 evidence (left)          V3 work (right)
─────────────               ────────────────
preserved SHA/docs     →    new implementation
OPEN remains OPEN      →    new tests
historical claims      →    new evidence hash
                       →    new SHA
                       →    new status on V3 inventory only
```

Never rewrite the left side to make the right side look better.

Preferred shape:

- Keep `main` as historical / current V1 evidence line until V3 is formally declared on a controlled branch.
- When V3 geometry is claimed, add `docs/formation_path_inventory_v3.json` (or equivalent) rather than silently mutating the V1 inventory’s meaning.

---

## Non-claims

- This freeze is **not** Foundation Seal 5.
- This freeze is **not** Universal Gate PROVEN.
- This freeze does **not** start V3 implementation.
- External Source Admission bounded tests do **not** close FM-005–013.

> Named ≠ Implemented · Implemented ≠ Tested · Tested ≠ Sealed · Sealed ≠ Authorized.

**End of V3 start freeze gate.**
