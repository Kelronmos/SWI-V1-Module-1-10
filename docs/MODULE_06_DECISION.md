# MODULE 06 DECISION

| Field | Value |
|-------|--------|
| **Module** | 06 — Drift Analyzer |
| **Decision** | **MIGRATE** |
| **Rebuild** | NO |
| **Primary boundary** | `DriftAnalyzer.check()` |
| **Secondary** | `set_baseline()` — review only |
| **Input** | `str` (production: M05 redacted text) |
| **Output** | `DriftResult` |
| **Policy** | `drifted` remains advisory |
| **Kernel** | Required when authorized |
| **Trainer halt** | On `ModuleKernelError` only |
| **Config wiring** | Deferred |
| **Algorithm** | Preserve |
| **Implementation** | **NOT EXECUTED** |
| **Procedure** | `docs/MODULE_06_MIGRATION.md` |
| **Seal** | **BLOCKED** |

Authorize with: **kernel Module 06**
