# SWI V4.7 Status Engine

**Status:** IMPLEMENTED / TESTED  
**Location:** `src/verification/status_engine.mjs`  
**Tests:** `src/verification/status_engine.test.mjs` (38 cases)

## Architecture

Closed transition system:

```
INPUT → NULL/EMPTY → UNKNOWN/UNDEFINED/INVALID
     → closed vocabulary → domain isolation
     → explicit TRANSITIONS matrix → evidence check
     → ALLOW / REJECT
```

## Domains

| Domain | Statuses |
|--------|----------|
| Construction | PROPOSED → MAPPED → SPECIFIED → IMPLEMENTED → TESTED → ADVERSARIALLY_TESTED → REPLAY_VERIFIED → EVIDENCE_HASHED → SEALED |
| Formal | NOT_PROVEN → PROVEN_ON_MODEL / BOUND_ONLY / FALSIFIED; PROVEN_ON_MODEL → PROVEN |
| Residual | OPEN → CLOSED |

Illegal jumps (e.g. PROPOSED → SEALED) are rejected even when full seal evidence is supplied.

## Input boundary (not lifecycle statuses)

| Token | Code |
|-------|------|
| null / undefined | STATUS_VALUE_ABSENT |
| "" | STATUS_VALUE_EMPTY |
| UNKNOWN / UNDEFINED / INVALID | STATUS_VALUE_UNRESOLVED |
| other unknown string | STATUS_VALUE_UNDEFINED |

Identity ALLOW applies only after successful classification.

## Non-claims

Does not prove production correctness, close FM-005, establish Universal Gate, or invent TLC results.
Hash ≠ truth. Expected ≠ actual until execution occurs.

```bash
node src/verification/status_engine.test.mjs
```
