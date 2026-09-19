# SWI V1 Cryptographic Evidence Contract

**Contract:** `canonicalization_v0`  
**Helpers:** `swi_core/canonical.py`, `swi_core/security_maze.py`, `swi_core/ed25519_sig.py`, `swi_core/evidence_artifact.py`  
**Status:** IMPLEMENTED / TESTED (bounded) — **not** CRTG, Seal 5, or Universal Gate

---

## Pipeline (only)

```text
CANONICALIZATION (canonicalization_v0)
        ↓
SHA-256 INTEGRITY
        ↓
MAZE EVIDENCE CHAIN (optional previous_evidence_hash)
        ↓
OPTIONAL ED25519 BINDING
        ↓
EVIDENCE ARTIFACT
```

```text
CRYPTOGRAPHIC INTEGRITY
        ≠  MAZE AUTHORITY ENFORCEMENT
        ≠  UNIVERSAL GATE
        ≠  FOUNDATION SEAL 5
```

---

## Permitted claims

| Evidence | May claim |
|----------|-----------|
| SHA-256 canonical digest | Integrity under `canonicalization_v0` |
| Maze gate chain | Ordered/bound evidence for **that** maze run |
| Ed25519 verify | Private-key holder signed the canonical message |
| Commit + test_id | Traceability to repo/test state |
| CI result | That CI execution produced that result |
| Combined package | Reproducible under documented contracts |

## Forbidden claims

| Must not claim |
|----------------|
| hash → legal truth / authorization |
| signature → factual truth / compliance |
| CI PASS → universal safety |
| evidence artifact → CRTG / production PKI / HSM |
| S9 attachment → S9 compliance |
| signature alone → FM closed / Universal Gate / Seal 5 |

**`signature: null` is legitimate.** Do not invent signatures to make records look stronger.

---

## FM attack artifact (minimum fields)

```json
{
  "fm_id": "FM-005",
  "status": "OPEN",
  "decision": "OBSERVED",
  "input_hash": "...",
  "evidence_hash": "...",
  "previous_evidence_hash": null,
  "commit": "...",
  "test_id": "...",
  "canonicalization_contract": "canonicalization_v0",
  "signature": null,
  "maze_authority_granted": false,
  "privileged_operation_performed": false
}
```

`evidence_hash` = `canonical_hash` of the record **excluding** `evidence_hash` and `signature` (see `build_fm_evidence_artifact`).

---

## Hold status (unchanged by this contract)

| Item | Status |
|------|--------|
| V1 crypto evidence | IMPLEMENTED / TESTED (bounded) |
| Security Maze | PARTIAL / NOT SEALED |
| FM-005…009 | OPEN (attacked) |
| Universal Gate | NOT PROVEN |
| Foundation Seal 5 | NOT READY |

Roadmap Phase 6 (steps 126–150): **reuse these facilities** — do not introduce a parallel crypto subsystem.
