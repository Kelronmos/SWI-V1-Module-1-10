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

## General

- No CEK, SAD-DFU, Vector Memory, Alita, Sovereign Mesh as implemented systems.
- Modules 11–19 blocked until Foundation Seal 5.
