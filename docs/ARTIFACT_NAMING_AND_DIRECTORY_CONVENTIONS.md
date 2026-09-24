# SWI Artifact Naming and Directory Conventions

**Status:** ADOPTED for formal verification track  
**Scope:** Applies to new verification, evidence, and formal artifacts. Existing sealed modules remain unchanged.

## Governing Principle

> Names identify artifacts; metadata identifies meaning; hashes identify exact content; status identifies verification state.

Therefore:

- filename ≠ proof
- filename ≠ authorization
- filename ≠ seal
- filename ≠ truth

## Canonical Directory Model (logical)

```
/
├── src/
├── tests/
│   ├── unit/
│   ├── property/
│   ├── adversarial/
│   ├── boundary/
│   ├── replay/
│   └── formal/
├── specs/
├── verification/
│   ├── tla/
│   ├── graph/
│   ├── static/
│   └── runtime/
├── adapters/
├── replay/
├── evidence/
│   ├── claims/
│   ├── artifacts/
│   ├── manifests/
│   ├── hashes/
│   └── packages/
├── reports/
├── docs/
└── scripts/
```

Not every repository needs every directory. Empty directories must not be created merely to satisfy the convention.

## Source vs Generated

- **Source-controlled:** `src/`, `tests/`, `specs/`, `verification/`, `adapters/`, `scripts/`, `docs/`
- **Generated:** `reports/`, `evidence/artifacts/`, `evidence/hashes/`, `replay/runs/`

Generated artifacts must identify the source commit from which they were produced.

## Artifact Identifier Format

```
SWI-<DOMAIN>-<NNN>
```

Examples: `SWI-MATH-001`, `SWI-WORKFLOW-001`, `SWI-S9-001`, `SWI-FM005-001`

Versioned: `SWI-MATH-001.v1`

## Allowed Status Vocabulary

```
PROPOSED
MAPPED
SPECIFIED
IMPLEMENTED
TESTED
ADVERSARIALLY_TESTED
REPLAY_VERIFIED
EVIDENCE_HASHED
PROVEN
PROVEN_ON_MODEL
FALSIFIED
NOT_PROVEN
BOUND_ONLY
INAPPLICABLE
SEALED
OPEN
CLOSED
```

Do not use ambiguous terms (`DONE`, `GOOD`, `FINAL`, `VALIDATED`, `COMPLETE`, `WORKING`) unless explicitly defined.

## Status Transitions (recommended)

```
MAPPED → SPECIFIED → IMPLEMENTED → TESTED → ADVERSARIALLY_TESTED
  → REPLAY_VERIFIED → EVIDENCE_HASHED → SEALED
```

Formal properties may independently become `PROVEN_ON_MODEL`, `PROVEN`, `FALSIFIED`, or `NOT_PROVEN`.

Status advances only when the corresponding evidence exists. Never promote by filename or by proximity to a sealed module.

## Non-Claims Rule

Every evidence envelope must include explicit non-claims. A formal result never automatically becomes:

- production-code proof
- admission authority
- authorization
- standing
- execution permission
- runtime binding
- Universal Gate
- mathematical seal

## Commit SHA Convention

- Human-readable filenames: short SHA (e.g. `0c8a2e6`)
- Evidence metadata: full SHA whenever available

## Final Rule

```
CLAIM → PROPERTY → MODEL/CODE BOUNDARY → METHOD
  → PROOF | COUNTEREXAMPLE | NOT CHECKED
  → REPLAY → EVIDENCE → HASH → STATUS
```
