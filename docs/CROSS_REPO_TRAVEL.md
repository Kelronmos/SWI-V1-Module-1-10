# Cross-Repository Travel Boundary

**Status:** IMPLEMENTED (envelope + JSON-capable fields) · REAL two-repo CI proof still open  
**Date:** 15 September 2026

## Correct path (not M10 → M11)

```text
V1 Trainer (M03→M02→M05→M06→M07/M09)
        → PipelineResult
        → export_foundation_evidence()
        → FoundationEvidenceEnvelope
        → SERIALIZE (JSON / transfer)
        → V2 parse
        → M11 Admission
        → AdmittedInput
        → V2 Kernel
        → M12+
```

**M10 External Sandbox is standalone.** It is **not** the V1 handoff point. Do not modify M10 to emit pipeline results for V2.

## Zero-base V2

V2 must **not** require:

- import of the V1 Python package
- shared process / singleton / ambient Trainer state
- live V1 objects in memory

V2 consumes a **serialized contract**, not V1’s runtime classes.

## Evidence vs derived state

V2 must **not** silently mutate the V1 envelope or rewrite its provenance.  
V2 **may** create **new** derived records (admission result, trust result, task state). Those must remain distinguishable from original V1 evidence.

Prefer: **admitted evidence** + **derived V2 state** — not “immutable claims” as the only vocabulary.

## Integrity

Covered: `payload`, `foundation_version`, `evidence_schema_version`, `evidence_id`, `source_reference`  
**Not covered:** `created_at` (metadata only)

Integrity ≠ authenticated sender (CRTG / signatures still DESIGN PENDING).

## Next proof

Real: Trainer → export → serialize → V2 M11 → AdmittedInput → Kernel isolation on reject.
