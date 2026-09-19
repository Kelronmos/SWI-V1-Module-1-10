# SWI v1.1 — Modules 00–11 (Foundation + ScarStore)

Structured Workflow Intelligence reference implementation.

> **Repository identity:** GitHub name `SWI-V1-Module-1-10` is retained for historical continuity.
> The current reference implementation is **V1.1 / Modules 00–11** (Foundation + ScarStore + continuity helpers).
> It is **not** limited to modules 1–10 despite the repository slug.

**Licence:** [Apache License 2.0](LICENSE)  
**Start:** [`docs/START_HERE.md`](docs/START_HERE.md) · **Governance:** [`docs/GOVERNANCE_LOCK.md`](docs/GOVERNANCE_LOCK.md)  
**Tip CI:** [`docs/TIP_CI_STATUS.md`](docs/TIP_CI_STATUS.md) · **pre-R (design):** [`docs/PRE_R_INDEX.md`](docs/PRE_R_INDEX.md)

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

Kernel contract failure → **HALT**.

## Status (honest)

| Item | State |
|------|--------|
| M02 / M03 / M05 / M06 | **SEALED** (bounded contracts) |
| M07 / M09 | Trainer integrity · not kernel-sealed |
| ScarStore | **IMPLEMENTED / TESTED** |
| M11 Continuity Lock | **IMPLEMENTED / TESTED** |
| Foundation evidence export | IMPLEMENTED / TESTED · **unsigned** |
| Authority boundary | IMPLEMENTED / TESTED · tip CI · **not sealed** |
| Ed25519 helper | Primitive only · **not CRTG** |
| **Foundation Seal 5** | **NOT READY** |
| CRTG | PROPOSED / design track |
| Tip CI | See `docs/TIP_CI_STATUS.md` |
| Bidirectional return path (pre-R) | **DESIGN only** · NOT AUTHORIZED · NOT IMPLEMENTED |

## Progression rule

Advance when the **dependency boundary** is validated — not by matching another repo’s module count.  
Readiness % never overrides a failed critical gate.

«Do not claim what the code cannot demonstrate.»

Next: **prove the foundation** (Seal 5 path). pre-R remains experimental design until explicitly authorized.
