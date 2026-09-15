# Module Integration Dependency Matrix (summary)

**Canonical under `docs/`.** Full long-form upload was root-misplaced; this summary matches **live** pipeline code.

## Production order (`Trainer.process`)

```text
M03 Context Sync (kernel) ──HALT──┐
         ↓                        │
M02 Security Probe (kernel) ─HALT─┤
         ↓                        │
M05 Redaction (kernel) ──────HALT─┤
         ↓                        │
   [if not blocked]               │
M06 Drift (kernel) ──────────HALT─┤
         ↓                        │
memory / audit (best-effort)      │
         ↓                        │
PipelineResult                    │
                                  ▼
                    ModuleKernelError → _record_halt → re-raise
```

## Status

| Module | Kernel |
|--------|--------|
| 02, 03, 05 | **SEALED** |
| 06 | **KERNEL-ENFORCED** (CI pending) |
| 01, 04, 07, 08, 09, 10 | Not migrated |
| 00 | Orchestrator; not sealed |

## Policy vs contract

| Event | Continues? |
|-------|------------|
| Kernel contract fail | **No** — halt |
| M02 blocked | Yes — `allowed=False`, skip M06 |
| M03 stale / M06 drifted | Yes — advisory |
