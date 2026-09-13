# Known Limitations

## Module 02 Security Probe
- Pattern matching only; misses novel/paraphrased injection.
- False positives on security-research discussion of the same phrases.
- Kernel pilot validates input/output **contract**, not detection completeness.

## Module 05 Redaction
- First-pass structured redaction; not complete PII coverage (especially international formats).

## Module 06 Drift
- Lexical/syntactic similarity style signals — not workflow, authority, or objective drift.

## Module 07 / 09 chains
- **Tamper-evident**, not tamper-proof. No external notary or WORM store assumed.

## Module 10 Sandbox
- Resource-controlled subprocess boundary.
- **Not** a hardened sandbox, complete isolation, or secure multi-tenant runtime.

## Configuration
- Loader merges known keys; range validation is partial (Module 02 threshold validated at construction).
- Expand validation per Part 2 manual before claiming config seal.

## Documentation
- Historical SWI documents may over-claim relative to this tree; this folder is authoritative for foundation status.

## Kernel rollout
- Only Module 02 is kernel-wrapped. Trainer does not yet special-case `ModuleKernelError` into a structured PipelineResult field (failure raises).
