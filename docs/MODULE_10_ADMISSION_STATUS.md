# Module 10 Admission Status

**MODULE:** 10  
**PROPOSED NAME:** Boundary / Evidence Handoff (BoundaryExporter)  
**STATUS:** **PROPOSED / NOT ADMITTED**  
**Date of decision:** 2026-09-19  
**Decision basis:** Red-team review of proposed Module 10 source + CI claims against the live repository tip.

---

## Architectural assignment

Module 10 is assigned as a **construction destination** for investigation of a verifiable boundary / evidence-handoff capability.

**This assignment is a construction reference, not an admission claim.**

It does **not** establish that:

- Module 10 currently exists as an admitted architectural module
- the proposed BoundaryExporter is part of the canonical V1 pipeline
- any M07 → M08 → M09 → M10 dependency chain has been demonstrated
- the component is sealed or authorized for downstream promotion

---

## Current demonstrated architecture (authoritative)

The live repository demonstrates:

```text
M03 → M02 → M05 → M06 → M07 / M09 → PipelineResult
        → export_foundation_evidence() → FoundationEvidenceEnvelope
```

Kernel contract failure → **HALT**.

Foundation Seal 5 remains **NOT READY**.

Existing Module 10 in this repository is the **External Sandbox** (subprocess isolation).  
The proposed BoundaryExporter is a separate, unadmitted proposal.

---

## What the proposal can demonstrate (if implemented)

| Item | Classification |
|------|----------------|
| BoundaryExporter Python code can run | Potentially IMPLEMENTED once committed and tested |
| Hash comparison detects mismatches in synthetic fields | UNIT-TESTED (synthetic only) |
| Canonical JSON serialization technique | UNIT-TESTED (local technique; must align with existing canonicalization contract) |
| Per-instance duplicate-export prevention (`_is_exported`) | UNIT-TESTED (memory-local only) |
| SHA-256 digest over specified inputs | IMPLEMENTATION CLAIM (integrity only) |

---

## What is NOT demonstrated / REJECTED as architectural evidence

| Claim | Classification |
|-------|----------------|
| M07 → M08 → M09 → M10 chain exists in SWI | **REJECTED / UNPROVEN** |
| Module 10 (BoundaryExporter) is part of current canonical pipeline | **REJECTED / UNPROVEN** |
| Module 10 is the final V1 architecture boundary | **REJECTED** |
| Cryptographic signature / non-repudiation exists | **REJECTED** |
| Digital signature, signer identity, key governance | **REJECTED** |
| Architecture is validated by the proposed CI naming | **REJECTED** |
| 90% coverage proves architecture | **REJECTED** |
| Isolated unit tests prove Module 10 architecture | **REJECTED** |
| Durable replay protection | **NOT DEMONSTRATED** (in-memory flag only) |
| Compatibility with FoundationEvidenceEnvelope | **NOT DEMONSTRATED** |
| Integration with real upstream modules | **NOT DEMONSTRATED** |

---

## Critical red-team findings (preserved)

1. **Competing architecture model**  
   The proposal assumes M07 → M08 → M09 → M10. The repository demonstrates a different core path. Introducing a second terminal evidence mechanism without reconciliation is blocked.

2. **Identity declaration ≠ admission**  
   `MODULE_ID = "MODULE_10_BOUNDARY_EXPORTER"` is an identity string, not independent evidence of architectural membership.

3. **Synthetic fixtures ≠ real chain**  
   Tests that invent `"a"*64` / `"b"*64` / `"c"*64` hashes prove the comparator, not that real modules produced those hashes.

4. **CI naming must not overclaim**  
   Workflow names such as “Validate SWI Architecture (Modules 00-10)” or “SWI Framework Modules 00-10 CI Pipeline” are rejected as architectural claims. CI may only claim what the executed commands actually verify.

5. **Integrity ≠ authenticity**  
   SHA-256 digest ≠ digital signature ≠ non-repudiation ≠ production key governance.

6. **Per-instance flag ≠ durable replay protection**  
   `self._is_exported = True` is process-local.

7. **Two exporters problem**  
   The repository already has `FoundationEvidenceEnvelope` / `export_foundation_evidence()`. A second independent terminal exporter must not claim final authority until the relationship is resolved.

---

## Admission requirements (blocked until)

Module 10 (BoundaryExporter) remains **PROPOSED / NOT ADMITTED** until all of the following exist as reproducible evidence:

1. Integration test that invokes the **real** canonical SWI execution path and feeds its actual evidence object into the boundary component.
2. Explicit, documented relationship to (or replacement of) `FoundationEvidenceEnvelope` / `export_foundation_evidence()` — one clear canonical evidence authority.
3. Alignment with the repository’s existing canonicalization contract (no silent second definition).
4. Negative / tamper tests against real (not only synthetic) upstream evidence.
5. Known-limitations record covering: no signature, no durable replay protection, no non-repudiation, no production key governance.
6. Passing repository verification path (`python -m pytest -q` and `./scripts/verify.sh`) on the exact commit.
7. Evidence report with commit SHA, test results, and independent review record.

Only after the above may the status advance to **INTEGRATED / VERIFIED**.  
**SEALED** requires the full evidence chain plus Foundation Seal 5 path considerations.

---

## Construction guidance for contributors

- Use `PROPOSED_MODULE_ID` / status files, not self-sealing identifiers.
- Keep synthetic unit tests; label them UNIT CONTRACT TESTS only.
- Prefer the repository’s established verification commands over a parallel unittest/coverage regime that fragments evidence.
- Name outputs “integrity-bound evidence envelope”, not “cryptographically sealed package”, unless an actual signature mechanism is present and governed.
- Do not let module number, file naming, or CI job titles become architectural authority.

---

## Status summary

```text
MODULE 10 (BoundaryExporter)
STATUS:                 PROPOSED / NOT ADMITTED
ARCHITECTURAL ADMISSION: NO
SEAL:                   NO
CANONICAL PIPELINE:     NO
FOUNDATION SEAL 5:      NOT READY (unchanged)
```

**Governing rule:** Do not claim what the code cannot demonstrate.

**MAPPED ≠ FROZEN ≠ SEALED ≠ AUTHORIZED**  
**MODULE NUMBER ≠ PERMISSION**  
**PROPOSED ≠ IMPLEMENTED ≠ ADMITTED ≠ SEALED**
