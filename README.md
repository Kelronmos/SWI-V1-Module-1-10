# SWI V1 — Modules 00–10 (Reconstruction)

Structured Workflow Intelligence foundation modules.

**Start here:** [`docs/START_HERE.md`](docs/START_HERE.md) · [`docs/00_READ_ME_FIRST.md`](docs/00_READ_ME_FIRST.md)

## Verify

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
./scripts/verify.sh
```

Package: `swi_core` (Modules 00–10, `config_loader`, `module_kernel`).

## Production pipeline

```text
M03 → M02 → M05 → M06 → M07 / M09 → PipelineResult
```

| Outcome | Meaning |
|---------|---------|
| Kernel contract failure | **HALT** (`ModuleKernelError`) |
| M02 `allowed=False` | Policy/block result — not “system is secure” |
| M03 stale / M06 drifted | **Advisory** flags — not automatic HALT |

Standalone (not in that linear path): M01, M04, M08, M10.

## Module status

| Module | Status |
|--------|--------|
| **02** Security Probe | **SEALED** — heuristic; contract fail → HALT; detection not complete |
| **03** Context Sync | **SEALED** — temporal; contract fail → HALT |
| **05** Redaction | **SEALED** — structured PII only |
| **06** Drift | **SEALED** — lexical cosine; `drifted` advisory; CI evidence on `8a44c52` (run 34968919030) |
| **07** Memory | TRAINER integrity/persistence · not kernel-sealed |
| **09** Audit | TRAINER integrity/persistence · not kernel-sealed |
| **00** Trainer | Fail-closed on kernel + integrity paths · **not foundation-sealed** |
| **01 / 04 / 08 / 10** | STANDALONE |

## Foundation Seal 5

**NOT READY**

See `docs/FOUNDATION_SEAL_5_COMPLETION_MANUAL.md`, `docs/FOUNDATION_REPAIR_AND_V1_V2_ADMISSION_MANUAL.md`, `docs/ROADMAP.md`.

## Cross-repository trust (certificates)

**PROPOSED / DESIGN PENDING** — `docs/CROSS_REPOSITORY_TRUST_SPECIFICATION.md`  
Not implemented. Not injected into M02–M06.

## Scope of claims

Do **not** infer: AGI, universal AI safety, complete cybersecurity, complete PII removal, CEK, Modules 11–46 as implemented, tamper-proof storage, or production certification from green tests alone.

«Do not claim what the code cannot demonstrate.»

Status: `docs/IMPLEMENTATION_STATUS.md` · `docs/EVIDENCE_MATRIX.md` · `docs/KNOWN_LIMITATIONS.md`
