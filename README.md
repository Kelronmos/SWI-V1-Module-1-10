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

## Module Kernel (pilot)

Module **02 Security Probe** is wrapped with fail-closed pre/post checks via `swi_core/module_kernel.py`.
Other modules are not yet migrated. See `docs/VOLUME_1_PART_2_MODULE_KERNEL_REBUILD_MANUAL.md`.

## Configuration

Trainer loads `config/swi_config.yaml` (or `config_path`) and applies:
- `security_probe.block_threshold`
- `context_sync.staleness_seconds`

`process(..., timestamp=...)` is supported for deterministic Context Sync tests.

## Scope of Claims

This repository makes claims only about functionality supported by current implementation and tests.

The following should **not** be inferred (explicitly **not claimed**):

- not general intelligence;
- not consciousness;
- not semantic understanding;
- not universal AI safety;
- not complete cybersecurity;
- not complete identity management;
- not production-grade distributed enforcement;
- not autonomous governance of arbitrary AI systems.

«Do not claim what the code cannot demonstrate.»

Status: `docs/IMPLEMENTATION_STATUS.md` · `docs/EVIDENCE_MATRIX.md` · `docs/KNOWN_LIMITATIONS.md`
