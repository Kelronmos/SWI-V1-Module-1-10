# Module 05 Kernel Migration

## Status

**Kernel-enforced (second seam after Module 02).**

## Contract

| Layer | Checks |
|-------|--------|
| Pre | input is `str`; `len(text) <= 100_000` |
| Operation | existing structured redaction (`_redact_impl`) |
| Post | result is `RedactionResult`; `redacted_text` is str; matches is list of `RedactionMatch`; categories ⊆ {EMAIL, PHONE, CREDIT_CARD, BW_OMANG}; spans valid, ordered, non-overlapping |

## Preserved meaning

Detection is still structured-pattern only (email, phone, card-shaped, BW Omang).  
Kernel wrapping **does not** claim complete PII removal.

## Trainer

Module 05 `ModuleKernelError` → halt reason `halted_by_module_05_kernel:...` → re-raise.  
Downstream (drift) must not run after Module 05 contract failure.

## Tests

- `test/test_redaction_kernel.py`
- `test/test_trainer_module05_halt.py`
- `test/adversarial/test_redaction_boundaries.py`

## Not claimed

Complete PII protection · NLP entity recognition · Modules 11–46 · CEK
