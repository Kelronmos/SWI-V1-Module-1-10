# SWI V1 — Modules 00–10 (Reconstruction)

Structured Workflow Intelligence foundation modules.

**Start:** [`docs/START_HERE.md`](docs/START_HERE.md) · **Governance:** [`docs/GOVERNANCE_LOCK.md`](docs/GOVERNANCE_LOCK.md)

## Verify

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
./scripts/verify.sh
```

## Pipeline

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
| Foundation evidence export | IMPLEMENTED / TESTED · **unsigned** |
| Ed25519 helper | Primitive only · **not CRTG** |
| **Foundation Seal 5** | **NOT READY** |
| CRTG | PROPOSED / design track |

## Progression rule

Advance when the **dependency boundary** is validated — not by matching another repo’s module count.  
Readiness % never overrides a failed critical gate.

«Do not claim what the code cannot demonstrate.»

Next: **prove the foundation** (Seal 5 path), not another architecture layer.
