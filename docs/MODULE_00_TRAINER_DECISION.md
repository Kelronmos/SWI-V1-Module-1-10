---
FILE LOCATION & STATUS CORRECTION — 15 Sep 2026
Canonical path: docs/
Root copies are redirects only.
Correct live status: M02/M03/M05 SEALED; M06 KERNEL-ENFORCED (CI seal pending);
Next: M06 CI → seal → Module 07 inspection. Module 00 is NOT foundation-sealed yet.
---

# MODULE 00: THE TRAINER — ARCHITECTURAL DECISION RECORD

**Decision:** Trainer as orchestration scaffold, not security boundary  
**Authority:** Keletso Ronald Mosidila, SWI Architecture  
**Date:** September 15, 2026  
**Status:** Proposed / preparatory (not foundation seal)

## Context

The SWI foundation requires a master orchestrator that initializes modules in a deterministic order, applies module boundaries, and fails closed on contract violations without silently continuing.

## Decision

Trainer (`module00_trainer.py`) remains the production pipeline owner:

```text
M03 → M02 → M05 → M06 → Memory → Audit → PipelineResult
```

Kernel failures raise `ModuleKernelError` after best-effort `_record_halt`.

## Consequences

- Modules own their contracts; Trainer owns halt propagation.
- Standalone utilities (01/04/08/10) stay outside the main request path unless later integrated with evidence.
- Configuration runtime wiring remains limited to documented keys.
