---
FILE LOCATION & STATUS CORRECTION — 15 Sep 2026
Canonical path: docs/
M02/M03/M05 SEALED; M06 KERNEL-ENFORCED (CI pending);
Next: M06 CI → seal → Module 07. Module 00 NOT foundation-sealed.
---

# MODULE 00 — TRAINER INSPECTION

## Production path (from source)

```text
process(text, timestamp?)
  → M03.record_turn
  → M02.scan
  → M05.redact
  → if not blocked: M06.check(redacted_text)
  → memory.append / audit.log_event
  → PipelineResult
```

## Failure handling observed

- M03/M02/M05/M06 `ModuleKernelError` → `_record_halt` → re-raise
- Audit/memory on halt path are best-effort and must not convert halt to success

## Gaps for final M00 seal

- M07/M09 normal-path persistence failure contracts still incomplete relative to Part 2/3 manuals
- Standalone modules not in main path by design
