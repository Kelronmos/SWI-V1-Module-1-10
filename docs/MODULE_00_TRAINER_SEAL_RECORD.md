# MODULE 00 — TRAINER — PREP RECORD (NOT FOUNDATION-SEALED)

> **STATUS:** Module 00 is **NOT** foundation-sealed.  
> Trainer **does** halt on M02 / M03 / M05 / **M06** `ModuleKernelError`.  
> Final M00 seal waits for remaining module kernels + Seal 5 gate.

| Field | Value |
|-------|--------|
| Implementation | `swi_core/module00_trainer.py` |
| Halt reasons | `halted_by_module_0{2,3,5,6}_kernel` |
| Advisory (no halt) | M03 stale/out_of_order; M06 `drifted=True`; M02 `blocked` → `allowed=False` |

See `docs/MODULE_00_TRAINER_DECISION.md`, `INSPECTION.md`, `MIGRATION.md` when those copies exist under `docs/`.
