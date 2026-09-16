# Volume 1 Consolidated Rebuild Manual — Handling Note

**Date:** 16 September 2026

An externally compiled document titled *SWI Volume 1 — Parts 2 Through Foundation Remediation* (Consolidated Rebuild Manual) was supplied. It claims to reproduce the real contents of this repository (Modules 00–10): architecture manuals, setup, full source under `swi_core/`, full test suite, and operational scripts.

## Decision

- The live repository remains the **authoritative** source of code, tests, and seal records.
- A compiled dump is treated as a **reference / rebuild aid only**.
- No bulk overwrite of `swi_core/`, `test/`, or existing seal records from the compilation.
- No claim that the compilation itself constitutes Foundation Seal 5 or supersedes current evidence.

## Rationale (SWI discipline)

> Evidence before claim.  
> Code → test → result → documentation.  
> Never documentation → assume → implemented.

Replacing live, tested files with a static compilation would invert that order.

## Current foundation position (unchanged by this note)

Refer to:

- `docs/CURRENT_POSITION.md`
- `docs/IMPLEMENTATION_STATUS.md`
- Individual module seal records under `docs/`
- `docs/FOUNDATION_SEAL_5_*` materials

Modules 11–22 remain in the separate V2 repository and are governed by V2’s own admission/seal process.

## Next controlled step (if desired)

If the compilation is to be retained in-repo for convenience, it should be stored as a clearly labelled reference artifact (e.g. under `docs/reference/` or as a release asset) without altering runtime code or seal status.
