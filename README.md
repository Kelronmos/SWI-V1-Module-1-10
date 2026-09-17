# SWI v1.1 — Modules 00–11 (Foundation + ScarStore)

Structured Workflow Intelligence reference implementation.

**Licence:** [Apache License 2.0](LICENSE)  
**Start:** [`docs/START_HERE.md`](docs/START_HERE.md) · **Governance:** [`docs/GOVERNANCE_LOCK.md`](docs/GOVERNANCE_LOCK.md)  
**Contribute:** [`CONTRIBUTING.md`](CONTRIBUTING.md) · **Provenance:** [`AUTHORS_AND_LEGACY.md`](AUTHORS_AND_LEGACY.md) · [`NOTICE`](NOTICE)

## Verify

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
./scripts/verify.sh
```

## Pipeline (core)

```text
M03 → M02 → M05 → M06 → M07 / M09 → PipelineResult
        → export_foundation_evidence() → FoundationEvidenceEnvelope
```

Kernel contract failure → **HALT**. M02 block / M03 stale / M06 drifted remain policy or **advisory** as documented.

## Status (honest)

| Item | State |
|------|--------|
| M02 / M03 / M05 / M06 | **SEALED** (bounded contracts) |
| M07 / M09 | Trainer integrity · not kernel-sealed |
| ScarStore | **IMPLEMENTED / TESTED** |
| M11 Continuity Lock | **IMPLEMENTED / TESTED** |
| Foundation evidence export | IMPLEMENTED / TESTED · **unsigned** |
| Ed25519 helper | Primitive only · **not CRTG** |
| **Foundation Seal 5** | **NOT READY** |
| CRTG | PROPOSED / design track |

## v1.1 upgrade

- Working `Scar` model + `ScarStore` (content hashing, Sovereign priority, integrity root, optional SQLite).
- Module 07 can validate attached ScarStore integrity.
- Module 11 Continuity Lock (bounded state tags, optional persistence).
- Tests for new components.
- No false seal claims.

## Progression rule

Advance when the **dependency boundary** is validated — not by matching another repo’s module count.  
Readiness % never overrides a failed critical gate.

«Do not claim what the code cannot demonstrate.»

Next: **prove the foundation** (Seal 5 path), then progressive admission of higher modules under evidence discipline.

## Collaboration

SWI is open for collaboration under Apache-2.0.  
Contribution does not rewrite provenance.  
Evidence is required before claims are accepted.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full policy.
