# SWI V4.7 Status Engine

**Status:** IMPLEMENTED / TESTED  
**Location:** `src/verification/status_engine.mjs`  
**Tests:** `src/verification/status_engine.test.mjs` (14 cases)

## Purpose

Mechanically reject illegal status promotions so that overclaiming becomes difficult.

## Core rule

```
PROVEN_ON_MODEL
        ↓
request SEALED
        ↓
STATUS_PROMOTION_REJECTED
        ↓
missing: runtime_correspondence, replay, evidence_hash, required_review, …
```

## Hard blocks

- `PROVEN_ON_MODEL` → `SEALED`
- `FALSIFIED` → `PROVEN_ON_MODEL`
- `FALSIFIED` → `PROVEN`
- `NOT_PROVEN` → `SEALED`
- `PROVEN_ON_MODEL` → `PROVEN` (without refinement evidence)
- `OPEN` residual → `CLOSED` without `closure_evidence`

## Non-claims

- Does not prove production correctness
- Does not close FM-005
- Does not establish Universal Gate
- Does not invent TLC results
- Does not modify frozen V1

## Run tests

```bash
node src/verification/status_engine.test.mjs
```
