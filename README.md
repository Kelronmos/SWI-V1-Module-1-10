# SWI V1 — Modules 00–10 (Reconstruction)

Structured Workflow Intelligence foundation modules.

**Start here:** [`docs/START_HERE.md`](docs/START_HERE.md)

## Verify

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
./scripts/verify.sh
```

Package: `swi_core` (Modules 00–10, `config_loader`, `module_kernel`).

## Module Kernel (sealed boundaries)

| Module | Status |
|--------|--------|
| **02 Security Probe** | **SEALED** — kernel-enforced **heuristic** probe; contract fail → **HALT**; risk ≥ threshold → `allowed=False`. Detection is **not** complete. |
| **03 Context Sync** | **SEALED** — temporal flags; contract fail → HALT |
| **05 Redaction** | **SEALED** — structured PII only |
| **06 Drift** | Inspected; MIGRATE decision; **not** kernel-migrated yet |

Seal records: `docs/MODULE_02_SEAL_RECORD.md` · `MODULE_03_SEAL_RECORD.md` · `MODULE_05_SEAL_RECORD.md`

## Configuration

Trainer loads config and applies `security_probe.block_threshold` and `context_sync.staleness_seconds`.  
`process(..., timestamp=...)` supported for deterministic Context Sync tests.

## Scope of claims

Do **not** infer: general intelligence, consciousness, semantic understanding, universal AI safety, complete cybersecurity, complete identity management, production-grade distributed enforcement, or autonomous governance of arbitrary AI systems.

«Do not claim what the code cannot demonstrate.»

Status: `docs/IMPLEMENTATION_STATUS.md` · `docs/EVIDENCE_MATRIX.md` · `docs/KNOWN_LIMITATIONS.md`

## Foundation

[`docs/FOUNDATION_MILESTONE.md`](docs/FOUNDATION_MILESTONE.md) · [`docs/VOLUME_1_PART_3_FOUNDATION_COMPLETION_MANUAL.md`](docs/VOLUME_1_PART_3_FOUNDATION_COMPLETION_MANUAL.md)

Modules **11–19** blocked until Foundation Seal 5. Active migration target: **Module 06** (when authorized).
