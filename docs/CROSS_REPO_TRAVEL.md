# Cross-Repository Travel Boundary

**Date:** 15 September 2026

## Status (locked)

| Gate | State |
|------|--------|
| **CROSS-REPO TRAVEL — BOUNDARY PROVEN LOCALLY** | YES (`f7be9d1`+) |
| Live two-checkout reproducibility | **PENDING** |
| CRTG | DESIGN PENDING |
| Foundation Seal 5 | **NOT READY** |

## Architecture (do not redesign this seam)

```text
V1 Trainer (M03→M02→M05→M06→M07/M09)
  → PipelineResult
  → export_foundation_evidence()
  → FoundationEvidenceEnvelope
  → SERIALIZE (JSON)
  → transfer
  → V2 M11 → AdmittedInput → Kernel → M12+
```

**M10 is not the handoff.** Do not force M10 to emit pipeline results for V2.

## Independence rule

> V1 produces a **versioned evidence contract**. V2 consumes the **serialized contract** independently of the V1 implementation.

Do **not** say “V2 imports V1.” No shared process, singleton, or ambient Trainer state.

## Two evidence levels

**V1 (local):** Trainer → exporter → JSON → integrity survives / tamper breaks digest  
**V2 (local):** V1-shaped serialized evidence → M11 accept/reject → no downstream on rejection

**Still open:** one CI (or documented script) with **two clean checkouts** so a real V1 build produces bytes a separate V2 tree admits.

## Provenance language

Do not silently mutate the V1 envelope. V2 may create **derived** state (admission, trust, task) that stays **distinguishable** from original V1 evidence. Prefer “admitted evidence” + “derived V2 state.”

## Integrity

Covered: payload, foundation_version, evidence_schema_version, evidence_id, source_reference  
**Not covered:** `created_at` (metadata only)

## Next work

1. Live two-checkout travel proof  
2. Remaining V1 Seal 5 evidence path  
3. CRTG design freeze only — no implementation rush  
