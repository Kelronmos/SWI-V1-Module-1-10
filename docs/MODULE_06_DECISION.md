# MODULE 06 DECISION

| Field | Value |
|-------|--------|
| **Module** | 06 — Drift Analyzer |
| **Decision** | **MIGRATE** |
| **Rebuild** | NO |
| **Primary boundary** | `DriftAnalyzer.check()` |
| **Secondary** | `set_baseline()` — review only; do not redesign |
| **Input** | `str` (production: M05 redacted text) |
| **Output** | `DriftResult` |
| **Policy** | `drifted` remains advisory |
| **Kernel** | Required when implementation authorized |
| **Trainer halt** | Required on `ModuleKernelError` only |
| **Config wiring** | Deferred |
| **Algorithm** | Preserve bag-of-words cosine |
| **Implementation** | **NOT STARTED** |
| **Seal** | **BLOCKED** |

## Why migrate

Function works and is integrated; deficiency is enforcement (type/shape, fail-closed, Trainer halt), not absence of detector.

## Non-goals

Embeddings · semantic drift · drift-driven block · CEK · Modules 11–19 · silent empty-baseline “fix”

## Next

Explicit authorization: **kernel Module 06** → implement → tests → Trainer halt → verify → CI → seal.
