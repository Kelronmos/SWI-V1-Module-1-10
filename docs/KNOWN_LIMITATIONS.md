# Known Limitations — SWI V1

**Status date:** 18 September 2026  
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

## Module 10 — External Sandbox

- Subprocess with timeout; optional resource limits where the platform provides them.
- Not a complete security sandbox or isolation guarantee.

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
