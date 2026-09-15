# SWI V1 — Modules 00–10 (Reconstruction)

Structured Workflow Intelligence foundation modules.

**Start here:** [`docs/START_HERE.md`](docs/START_HERE.md) · upgrade orientation: [`docs/00_READ_ME_FIRST.md`](docs/00_READ_ME_FIRST.md)

## Verify

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
./scripts/verify.sh
```

Package: `swi_core` (Modules 00–10, `config_loader`, `module_kernel`).

## Module Kernel status

| Module | Status |
|--------|--------|
| **02 Security Probe** | **SEALED** — heuristic probe; contract fail → HALT; risk → `allowed=False`. Detection not complete. |
| **03 Context Sync** | **SEALED** — temporal flags; contract fail → HALT |
| **05 Redaction** | **SEALED** — structured PII only |
| **06 Drift** | **KERNEL-ENFORCED** — lexical cosine; `drifted` advisory; **CI seal pending** |
| **00 Trainer** | Halt on M02/M03/M05/M06 kernel failure; not foundation-sealed |

Canonical docs live under **`docs/`**. Do not treat root-level upgrade markdown as authority if duplicates exist.

## Scope of claims

Do **not** infer: general intelligence, universal AI safety, complete cybersecurity, complete PII removal, CEK, or Modules 11–46 as implemented.

«Do not claim what the code cannot demonstrate.»

Status: `docs/IMPLEMENTATION_STATUS.md` · `docs/EVIDENCE_MATRIX.md` · `docs/KNOWN_LIMITATIONS.md`

Modules **11–19** blocked until Foundation Seal 5. **Next:** seal M06 after CI, then Module 07 inspection.
