# SWI International Validation Harness

**Status:** Implemented as repo-native tooling (v0)  
**Not:** A compliance certificate, audit opinion, or legal determination

## Purpose

Generate evidence from the repository itself:

```text
CLAIM
  → REPOSITORY IMPLEMENTATION
  → EXECUTABLE TEST
  → OBSERVED RESULT
  → CRYPTOGRAPHIC HASH
  → REPORT
```

Not:

```text
Claim → generated certificate
```

## Outputs

```bash
python scripts/swi_validation_harness.py
# → evidence/validation/validation_evidence.json
# → evidence/validation/framework_mapping.csv
# → evidence/validation/VALIDATION_REPORT.md
# → evidence/validation/SHA256SUMS
```

## Status vocabulary

| Token | Meaning |
|-------|---------|
| PASS | Executable evidence exists and passed for that control |
| FAIL | Executable evidence exists and failed |
| BLOCKED | Prerequisite failure prevents valid verification |
| NOT_TESTED | No evidence yet |
| NOT_PROVEN | Implementation exists; evidence insufficient |
| PARTIAL | Some evidence; gaps remain |
| OPEN | Requirement not addressed |
| PROPOSED | Design only |
| SEALED | Only after defined seal procedure |

## Hard non-claims

- Not EU AI Act compliant / certified  
- Not UN / UNESCO / Council of Europe certified  
- Not NIST AI RMF certified  
- Universal Gate **NOT PROVEN**  
- Module 10 **PROPOSED**  
- Foundation Seal 5 **NOT READY**  
- No automatic `compliant` field in any export  

## Relation to Universal Gate

The harness **records** `UNIVERSAL_GATE=NOT_PROVEN` until every production formation path is admission-bound and proven. Framework alignment does not close that gap.
"}, {