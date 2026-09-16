# Known Limitations

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

## Module 07 — Memory Validator (in-process only)

- The hash-chained "scar" log is a **plain in-memory Python list** held on the
  `MemoryValidator` instance. Nothing is written to disk, a database, or any
  durable store.
- A fresh instance (process restart, or Trainer re-instantiation) starts with
  an empty chain and reports that empty chain as `valid=True`. Cross-process
  or cross-restart tampering / data loss is therefore invisible to
  `validate_chain()`.
- In-process tampering *is* detected (see `tamper_for_testing()` and the
  existing tests); that is the actual scope of the current implementation.
- Docstring previously used "storage medium" language that implied a durable
  store existed. That framing has been corrected; this limitation is now
  explicit. Contrast with Module 09, which does persist to an append-only file.
- Decision still open: keep as pure in-process structure, or later add
  disk-backed persistence mirroring Module 09. Until then, do not claim
  durability.

## General

- No CEK, SAD-DFU, Vector Memory, Alita, Sovereign Mesh as implemented systems.
- Modules 11–19 blocked until Foundation Seal 5.
