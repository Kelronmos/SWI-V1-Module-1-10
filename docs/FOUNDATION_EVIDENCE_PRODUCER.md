# V1 Foundation Evidence Producer

**Status:** IMPLEMENTED / TESTED · unsigned · **not** Seal 5 · **not** CRTG

## Flow

```text
Trainer.process() → PipelineResult → export_foundation_evidence()
  → FoundationEvidenceEnvelope
```

Do not export after HALT / `ModuleKernelError`.

## Integrity-covered fields (SHA-256 canonical JSON)

| Included in digest |
|--------------------|
| payload |
| foundation_version |
| evidence_schema_version |
| evidence_id |
| source_reference |

| **Excluded from digest** |
|--------------------------|
| **`created_at`** — export metadata only; changing it must **not** be required to match `integrity_reference` |

## Status string

`verification_status = v1_trainer_pipeline_completed`

Means: V1 Trainer pipeline completed and produced this envelope.  
Does **not** mean: authenticated sender, universal truth, or safe action.

## vs test fixtures (V2)

| Kind | `verification_status` |
|------|------------------------|
| Real V1 export | `v1_trainer_pipeline_completed` |
| Unit-test fixture only | `foundation_verified_test_fixture` |

Hash match proves field integrity, **not** that V1 produced the object. Sender authenticity requires future TaskEnvelope + signature + CRTG.

## Module

`swi_core/foundation_evidence.py` · tests: `test/test_foundation_evidence_export.py`
