# SWI V4.7 Status Engine

**Status:** IMPLEMENTED / TESTED  
**Location:** `src/verification/status_engine.mjs`  
**Tests:** `src/verification/status_engine.test.mjs` (30 cases)

## Purpose

Mechanically reject illegal status promotions so that overclaiming becomes difficult.

## Closed status domains

Three independent tracks (cross-domain transitions are rejected):

| Track | Statuses |
|-------|----------|
| Construction | PROPOSED, MAPPED, SPECIFIED, IMPLEMENTED, TESTED, ADVERSARIALLY_TESTED, REPLAY_VERIFIED, EVIDENCE_HASHED, SEALED |
| Formal | NOT_PROVEN, PROVEN_ON_MODEL, PROVEN, FALSIFIED, BOUND_ONLY |
| Residual | OPEN, CLOSED, INAPPLICABLE |

## Core rules

```
PROVEN_ON_MODEL → SEALED          HARD BLOCK (cross-domain + absolute)
FALSIFIED → PROVEN_ON_MODEL       HARD BLOCK
FALSIFIED → PROVEN                HARD BLOCK
NOT_PROVEN → SEALED               HARD BLOCK
Unknown status                    REJECTED
Cross-domain transition           REJECTED
PROVEN_ON_MODEL → PROVEN          CONDITIONAL (requires runtime_correspondence + refinement)
OPEN → CLOSED                     CONDITIONAL (requires closure_evidence)
```

## Evidence acceptance

Accepted forms only:
- boolean `true`
- non-empty string (id / hash / path)
- non-empty array of non-empty strings
- object with `id`, `hash`, or `sha256` field

Rejected: `false`, empty string, empty array, empty object, unrelated keys.

## Non-claims

- Does not prove production correctness
- Does not close FM-005
- Does not establish Universal Gate
- Does not invent TLC results
- Does not modify frozen V1
- Hash ≠ truth; expected ≠ actual until execution occurs

## Run tests

```bash
node src/verification/status_engine.test.mjs
```
