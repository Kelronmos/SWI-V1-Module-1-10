# Known Limitations

## Module 02 Security Probe
- Pattern matching only; misses novel/paraphrased injection.
- False positives on security-research discussion of the same phrases.
- Kernel pilot validates input/output **contract**, not detection completeness.

## Module 05 Redaction
- First-pass structured redaction; not complete PII coverage.

## Module 06 Drift
- Lexical/syntactic similarity style signals — not workflow/authority/objective drift.

## Module 07 / 09 chains
- **Tamper-evident**, not tamper-proof.

## Module 10 Sandbox
- Resource-controlled subprocess boundary.
- **Not** a hardened sandbox, complete isolation, or secure multi-tenant runtime.

## Configuration
- Range validation is partial (Module 02 threshold validated at construction).

## Kernel rollout
- Only Module 02 is kernel-wrapped. Trainer does not yet map `ModuleKernelError` into a structured PipelineResult field (failure raises).
