# SWI Foundation Bridge & Seal 5 Remediation Manual

**Version:** 1.0 · **Date:** 15 September 2026  
**Status:** OPERATIONAL REMEDIATION GUIDE  
**Author:** Keletso Ronald Mosidila — Trusts Motion

## Purpose

Prove the first major cross-repo boundary — **not** redesign SWI:

```text
V1 Trainer → PipelineResult → export_foundation_evidence()
  → FoundationEvidenceEnvelope → V2 M11 → AdmittedInput → V2 Kernel
```

Track B (TaskEnvelope → CRTG) stays **design only** until Track A has evidence.

## Does not authorize

Bulk M13–M22 · production CA/keys · CRTG implementation · rewriting sealed modules · treating fixtures as V1 production evidence · claiming Seal 5 without a record

## Phases

0 Freeze · 1 V1 reproduce · 2 module evidence · 3 Trainer integration · 4 adversarial · 5 Foundation Evidence · 6 **real V1→V2 integration** · 7 M11/Kernel · 8 claim audit · 9 Seal decision

## Integrity semantics (contract)

Digest covers **only**:

`payload`, `foundation_version`, `evidence_schema_version`, `evidence_id`, `source_reference`

**`created_at` is metadata and is NOT part of the integrity-covered material.**

## Status meanings

`v1_trainer_pipeline_completed` = Trainer completed and exported the declared object.  
≠ truth · ≠ authenticated sender · ≠ authorized action · ≠ safe to execute

## Checkpoint decision

Exactly one: **FOUNDATION BRIDGE — READY** or **NOT READY**.  
Then Seal 5: **PASSED** or **NOT READY**. No “almost.”

## Next authorized stage

Foundation bridge evidence → Seal 5 decision → TaskEnvelope/CRTG **design** freeze → controlled M12 — **not** bulk 13–22.
