# START HERE — SWI Modules 00–10

## What this repository is

Reconstruction of **Modules 00–10** of Structured Workflow Intelligence (SWI): a Trainer-orchestrated pipeline with security probe, context sync, redaction, drift detection, memory validation, access auth, audit logging, and a resource-controlled subprocess boundary.

## What this repository is not

It is **not** a complete implementation of the full historical SWI textbook (CEK, SAD-DFU, Vector Memory / Scars, Alita, 46 modules, Sovereign Mesh). Those remain architectural or historical unless code and tests prove them.

## Authority hierarchy

```text
CURRENT CODE
     ↓
AUTOMATED TESTS
     ↓
REPRODUCIBLE RESULT
     ↓
DOCUMENTATION
     ↓
ARCHITECTURAL / HISTORICAL MATERIAL
```

If documentation conflicts with executable evidence: **stop and investigate**.

## Quick verify

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
./scripts/verify.sh   # when docs + scripts are present
```

## Read next

1. `docs/IMPLEMENTATION_STATUS.md` — what is implemented vs partial
2. `docs/KNOWN_LIMITATIONS.md` — honest boundaries
3. `docs/EVIDENCE_MATRIX.md` — claim → evidence map
4. `docs/TESTING_AND_VERIFICATION.md` — how to challenge the system
5. `docs/VOLUME_1_PART_2_MODULE_KERNEL_REBUILD_MANUAL.md` — kernel rebuild path

## Package layout

| Path | Role |
|------|------|
| `swi_core/` | Modules 00–10 + config_loader + module_kernel |
| `security/self_check.py` | Shared fail-closed helper (primitive) |
| `config/swi_config.yaml` | Runtime defaults (loaded by Trainer) |
| `test/` + `test_swi_core.py` | Automated tests |
| `scripts/` | Inventory, doc checks, verify.sh |
| `.github/workflows/ci.yml` | CI workflow file (pass only after green runs) |

## Module Kernel status

- **Pilot:** Module 02 (`SecurityProbe.scan`) is wrapped with pre/post checks.
- **Not yet:** Full migration of modules 00–01, 03–10 to ModuleKernel.
- **Future:** Global SWI Kernel registry — only after foundation Seal 5.
