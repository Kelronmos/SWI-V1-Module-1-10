# MODULE 06 — DRIFT ANALYZER — SEAL RECORD

| Field | Value |
|-------|--------|
| **Status** | **KERNEL-ENFORCED** · local verified · **CI PENDING** |
| Implementation tip | `63f94f6` (Trainer halt complete) |
| Kernel name | `module_06_drift` |
| Primary API | `check()` |
| Policy | `drifted` advisory only |
| Tests | `test/test_drift_kernel.py` |
| verify.sh | includes Module 06 kernel tests |

## Seal language (after CI)

> Kernel-enforced lexical drift contract; tested I/O and Trainer halt. Not semantic drift detection.

## Limitations

- Bag-of-words / cosine only
- Empty baseline → similarity 0.0 (often drifted)
- Threshold default 0.35; YAML threshold wiring deferred
- Baseline not authenticated / not persistent across process restart

**SEALED only after independent CI PASS on the complete tip.**
