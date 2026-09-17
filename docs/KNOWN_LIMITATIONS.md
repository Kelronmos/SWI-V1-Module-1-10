# Known Limitations — SWI v1.1

## Module 02 — Security Probe (SEALED enforcement)

- Heuristic regex/base64 signals only; not semantic prompt-injection defense.
- False positives possible on legitimate discussion of attack phrases.
- Default `block_threshold` 0.5 and weights are implementation defaults, not calibrated guarantees.
- **Contract failure → HALT**; **heuristic block → `allowed=False`** — different signals.
- Seal does **not** mean complete cybersecurity. See `docs/MODULE_02_SEAL_RECORD.md`.

## Module 03 — Context Sync (SEALED)

- Temporal flags only; no content truth; clock not authenticated.
- `stale` / `out_of_order` are advisory to the pipeline.

## Module 05 — Redaction (SEALED)

- Structured patterns only (EMAIL, PHONE, CREDIT_CARD, BW_OMANG).
- Not complete PII / not NLP entity recognition.

## Module 06 — Drift (not kernel-migrated)

- Bag-of-words cosine only; empty baseline → similarity 0 / often drifted.
- Advisory only; threshold not config-wired.

## Module 07 — Memory Validator + ScarStore

- Legacy hash-chained log remains in-process unless a persistent ScarStore is attached.
- ScarStore can use SQLite for durability within one deployment; this is still not a distributed ledger or external anchor.
- Embeddings are optional; no built-in embedding model or similarity search is claimed.
- Does **not** constitute full Vector Memory or Foundation Seal 5.

## Module 11 — Continuity Lock

- Bounded state tags only (default max 10).
- Optional file persistence; not multi-process safe without external locking.
- No semantic understanding of tags.

## General

- No CEK, SAD-DFU, full Vector Memory, Alita, or Sovereign Mesh as complete systems.
- Modules beyond 11 remain design-level until Foundation Seal 5 and evidence gates are satisfied.
- «Do not claim what the code cannot demonstrate.»
