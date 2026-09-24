# Structured Workflow Intelligence (SWI) V4.7 — Discipline Patch

Purpose: a repository-overlay patch/reference pack derived from the supplied SWI v5.12 archive and the established V1 formal-verification discipline.

This pack is deliberately conservative. It does **not** declare the supplied archive production-ready, independently verified, mathematically sealed, or universally gated.

## Core construction rule

`CLAIM → PROPERTY → MODEL/CODE BOUNDARY → METHOD → PROOF | COUNTEREXAMPLE | NOT CHECKED → REPLAY → EVIDENCE → HASH → STATUS`

## Non-negotiable SWI distinctions

- Structured Workflow Intelligence (SWI) is the canonical system name.
- A filename is not proof.
- A model result is not runtime proof.
- A hash is not authority.
- A signature is not truth by itself.
- `TESTED` is not `SEALED`.
- `PROVEN_ON_MODEL` is not `PROVEN`.
- `SIMULATED`, `PARTIAL`, and `VERIFIED` must describe the actual boundary.
- `OPEN` remains `OPEN` until the specified closure evidence exists.
- Proposed module mappings are construction references, not completion claims.
- Frozen historical implementations are not silently rewritten.

## Application modes

1. **Patch mode:** copy the files into the repository and review each proposed replacement.
2. **Reference mode:** use the documents, model, templates, and module map to rebuild equivalent controls in another SWI repository.
3. **Audit mode:** compare existing claims against the status vocabulary and evidence contract before promoting anything.

See `PATCH_PLAN.md` and `SWI_V4_7_MODULE_MAP.md`.
