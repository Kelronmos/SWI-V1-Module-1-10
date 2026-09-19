# Known Limitations — SWI V1

**Status date:** 19 September 2026  
**Rule:** Do not claim what the code cannot demonstrate.

## Module 07 — Memory Validator

- In-process, in-memory hash chain only.
- Does not provide durable disk persistence (that is M09).
- Does not prove historical truth of recorded content.

## Module 08 — Access Auth

- HMAC session tokens with expiry; not a full identity provider.
- Fail-closed on malformed tokens (including signed non-JSON).

## Module 09 — Audit Logger

- Append-only file log with hash chaining.
- Fail-closed on malformed lines.
- Not a multi-node consensus log.

## Module 10 — External Sandbox (existing)

- Subprocess with timeout; optional resource limits where the platform provides them.
- Not a complete security sandbox or isolation guarantee.

## Module 10 — Proposed Boundary / Evidence Handoff (BoundaryExporter)

- **Status: PROPOSED / NOT ADMITTED** (see `docs/MODULE_10_ADMISSION_STATUS.md`).
- Not part of the current canonical pipeline.
- Any synthetic M07→M08→M09→M10 chain is unproven against the live architecture.
- SHA-256 integrity digest ≠ digital signature ≠ non-repudiation.
- In-memory duplicate-export flag ≠ durable replay protection.
- Must not compete with or silently replace `FoundationEvidenceEnvelope` / `export_foundation_evidence()` without explicit reconciliation.

## Foundation evidence

- Export is versioned and integrity-bound; unsigned unless Seal 5 path is completed.
- Integrity excludes `created_at` by design.

## SCAR / ScarStore

- Content hash covers a defined field subset only.
- Optional embeddings; no built-in embedding model or similarity search is claimed.
- Does **not** constitute full Vector Memory or Foundation Seal 5.

## Module 11 — Continuity Lock

- Bounded state tags only (default max 10).
- Optional file persistence; not multi-process safe without external locking.
- Does not provide semantic understanding of tags.

## General

- No CEK, SAD-DFU, full Vector Memory, Alita, or Sovereign Mesh as complete systems.
- Modules beyond 11 remain design-level until Foundation Seal 5 and evidence gates are satisfied.
- «Do not claim what the code cannot demonstrate.»
- MODULE NUMBER ≠ PERMISSION. MAPPED ≠ FROZEN ≠ SEALED ≠ AUTHORIZED.
