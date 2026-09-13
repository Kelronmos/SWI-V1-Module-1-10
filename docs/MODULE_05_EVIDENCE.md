# Module 05 — Evidence Package (Kernel-Enforced)

**Status:** KERNEL-ENFORCED · under foundation seal process (not “universally secure”)  
**Meaning preserved:** structured patterns only — EMAIL, PHONE, CREDIT_CARD, BW_OMANG  

## Contract

| Layer | Rule |
|-------|------|
| Pre | input is `str`; `len(text) ≤ 100_000` |
| Operation | existing `_redact_impl` (pattern order unchanged) |
| Post | `RedactionResult`; matches are `RedactionMatch`; categories ⊆ allowed set; spans valid, ordered, non-overlapping |
| Trainer | `halted_by_module_05_kernel` → best-effort halt record → re-raise; drift must not run |

## Evidence map

| Area | Location |
|------|----------|
| Implementation | `swi_core/module05_redaction_engine.py` |
| Kernel unit | `test/test_redaction_kernel.py` |
| Trainer halt | `test/test_trainer_module05_halt.py` |
| Boundaries / limitation | `test/adversarial/test_redaction_boundaries.py` |
| Regression (email/phone) | `test_swi_core.py` + kernel normal path |
| verify.sh | Module 05 kernel + Trainer↔05 + adversarial steps |
| Migration notes | `docs/MODULE_05_KERNEL_MIGRATION.md` |

## What tests prove

- Invalid type → operation does not run  
- Oversized input → rejected  
- Exact max length accepted; max+1 rejected  
- Non-`RedactionResult` / unknown category / overlap / invalid spans → not released  
- Trainer halt on post-fail; drift not called; audit failure does not swallow halt  
- Free-text (“Westwood Primary”) not claimed as redacted  

## What is NOT proven

- Complete PII removal  
- Semantic entity recognition  
- Zero false positives  
- Universal security  

## Seal language

Prefer:

> Module 05 has a kernel-enforced input/output contract with automated tests covering defined failure boundaries. Detection remains structured-pattern first-pass only.

Avoid:

> Module 05 is secure / removes all personal information.

## Next after M05 evidence review

Confirm CI green → **Module 03 Context Sync** (contract exploration complete; implement only when authorized).
