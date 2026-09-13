# SWI V1 — Modules 00–10 (Reconstruction)

Structured Workflow Intelligence foundation modules.

**Start here for current status:** [`docs/START_HERE.md`](docs/START_HERE.md)

## Verify

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
./scripts/verify.sh
```

Package import path: `swi_core` (Modules 00–10, `config_loader`, `module_kernel`).

## Module Kernel (pilot)

Module **02 Security Probe** is wrapped with fail-closed pre/post checks via `swi_core/module_kernel.py`.
Other modules are not yet migrated. See `docs/VOLUME_1_PART_2_MODULE_KERNEL_REBUILD_MANUAL.md`.

## Configuration

Trainer loads `config/swi_config.yaml` (or `config_path`) and applies:
- `security_probe.block_threshold`
- `context_sync.staleness_seconds`

`process(..., timestamp=...)` is supported for deterministic Context Sync tests.

## Scope of Claims

This repository makes claims only about functionality supported by its current implementation and verification evidence.

The following should **not** be inferred merely from the existence of this repository
(each item is explicitly **not claimed** by current Modules 00–10):

- not general intelligence;
- not consciousness;
- not semantic understanding;
- not universal AI safety;
- not complete cybersecurity;
- not complete identity management;
- not production-grade distributed enforcement;
- not autonomous governance of arbitrary AI systems; or
- not capabilities that existed only in earlier unrecovered development.

Where those concepts are relevant to broader SWI research, they should be treated as architectural, research, or historical context unless supported by current implementation and tests.

## Guiding Principle

«Do not claim what the code cannot demonstrate.
Do not treat documentation as evidence of execution.»

Further status: `docs/IMPLEMENTATION_STATUS.md`, `docs/EVIDENCE_MATRIX.md`, `docs/KNOWN_LIMITATIONS.md`.
