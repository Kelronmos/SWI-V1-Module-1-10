# SWI Evidence-Boundary / Module Admission — 230-Step Status

**Repository:** Kelronmos/SWI-V1-Module-1-10  
**Document date:** 2026-09-19  
**Baseline tip at documentation:** `d3753d951fe5bbd86b7ebf7c098ebde998542b53` (pre-hardening)  
**This document status:** Construction / gap matrix — **not** a seal

---

## Critical invariant

> Documentation may describe admission. Tests may provide evidence for admission.  
> A hash may identify content. A seal may bind an admitted artifact.  
> None of those facts, individually, should manufacture authority that the  
> executable admission boundary does not establish.

---

## Phase summary

| Phase | Steps | Status |
|-------|-------|--------|
| 1 Establish baseline | 1–40 | **PARTIAL** — inspectable via GitHub API; full local clone/env freeze not executed in this session |
| 2 Run existing system | 41–70 | **NOT EXECUTED HERE** — requires local `./scripts/verify.sh` + pytest; do not treat prior CI as tip proof |
| 3 Define governance model | 71–100 | **DOCUMENTED** in admission status + this file; partial executable encoding in `admission_boundary.py` |
| 4 Module 10 construction boundary | 101–120 | **DONE** — PROPOSED / NOT ADMITTED; no canonical M10 exporter |
| 5 Canonical evidence authority | 121–140 | **PARTIAL** — FoundationEvidenceEnvelope exists; full caller/bypass map not completed in code |
| 6 Implement admission boundary | 141–170 | **SUBSTANTIALLY DONE** — `swi_core/admission_boundary.py` + fail-closed input validation |
| 7 Harden against input attacks | 171–200 | **PARTIAL** — core type/hex/bool/empty cases covered; Unicode confusables / normalization matrix incomplete |
| 8 Attack the evidence model | 201–230 | **PARTIAL** — attacks 1–10 + Phase 7 cases in tests; full API surface bypass audit not complete |

---

## Implemented (executable)

- `swi_core/admission_boundary.py`
  - Documentation ≠ admission/seal
  - Fake seal without record
  - Old CI / tip mismatch
  - Module number = construction reference only
  - Synthetic upstream receipts rejected
  - Hash laundering rejected
  - Seal domain rebinding rejected
  - Authority laundering (`verified` → `executable`) rejected
  - Blocked / proposed / not-admitted cannot force execute
  - Seal mutation (old seal ≠ tip)
  - Fail-closed: non-mapping claim, non-string module/status, empty/whitespace IDs,
    non-hex commits, boolean/string confusion, unknown status tokens, empty seal records

- `test/adversarial/test_architecture_boundary_attacks.py`
  - Attacks 1–10 + Phase 7 malformed-input cases

- `scripts/verify.sh` wires architecture-boundary suite

- Governance docs:
  - `docs/MODULE_10_ADMISSION_STATUS.md`
  - `docs/MODULE_10_PROPOSED_BOUNDARY_CONTRACT.md`
  - `docs/EVIDENCE_MATRIX.md`
  - `docs/KNOWN_LIMITATIONS.md`

---

## Missing / incomplete (honest)

| Item | Manual steps | Status |
|------|--------------|--------|
| Full local baseline freeze (env, packages, OS) | 1–10, 66–69 | Missing in this session |
| Fresh local `./scripts/verify.sh` + full pytest on tip | 41–65 | Not executed here |
| Exhaustive Unicode / confusable module-ID matrix | 185–187 | Missing |
| Duplicate JSON key / deep-nesting stress | 181–184 | Missing |
| Full caller graph of every execute/seal/export path | 129–138 | Missing |
| Universal enforcement (kernel cannot bypass admission_boundary) | 229–230, bypass question | **Known gap** — boundary is a tested gate, not yet proven universal |
| Mutation testing of controls (disable one check → test fails) | Manual § mutation | Missing as automated suite |
| Evidence matrix self-certification attack as automated test | Manual § 6 | Missing |
| Durable replay protection | — | Not claimed |
| Digital signature / CRTG / non-repudiation | — | Not claimed |
| Foundation Seal 5 | — | **NOT READY** |
| Module 10 BoundaryExporter integration | 101–120, admission requirements | **PROPOSED / NOT ADMITTED** |

---

## Module 10 status (unchanged)

```text
STATUS:                 PROPOSED / NOT ADMITTED
ARCHITECTURAL ADMISSION: NO
SEAL:                   NO
CANONICAL PIPELINE:     NO
FOUNDATION SEAL 5:      NOT READY
```

---

## Known bypass risk (must remain visible)

```text
admission_boundary.py  →  (if wired)  →  execution

vs

caller → kernel / direct API → bypass admission_boundary.py
```

Until every execution entrypoint is proven to call the admission boundary
(or an equivalent fail-closed gate), the control is a **tested gate**, not a
**universal enforcement boundary**. Documented in KNOWN_LIMITATIONS spirit.

---

## Required final evidence record (template — fill only from executable runs)

```json
{
  "repository": "Kelronmos/SWI-V1-Module-1-10",
  "branch": "main",
  "tested_commit": "<fill after local verify>",
  "baseline_commit": "d3753d951fe5bbd86b7ebf7c098ebde998542b53",
  "verification_command": "./scripts/verify.sh",
  "test_command": "python -m pytest -q",
  "architecture_test_command": "python -m pytest -q test/adversarial/test_architecture_boundary_attacks.py",
  "adversarial_test_command": "python -m pytest -q test/adversarial/",
  "tests_collected": null,
  "tests_passed": null,
  "tests_failed": null,
  "tests_skipped": null,
  "architecture_controls": "admission_boundary.py + architecture_boundary_attacks",
  "attacks_attempted": ["fake_seal", "docs_injection", "old_ci", "module_number", "synthetic_receipts", "hash_laundering", "seal_laundering", "authority_laundering", "blocked_bypass", "seal_mutation", "phase7_inputs"],
  "attacks_rejected": "see test suite — fill after green run",
  "known_bypasses": ["direct kernel/API paths not proven to call admission_boundary"],
  "known_limitations": ["no local verify in this session", "Unicode confusable matrix incomplete", "Foundation Seal 5 NOT READY"],
  "module_10_status": "PROPOSED / NOT ADMITTED",
  "blocked_items": ["M10 BoundaryExporter admission", "Foundation Seal 5"],
  "required_unblocking_evidence": ["real upstream integration test", "FoundationEvidenceEnvelope relationship", "tip-bound verify.sh PASS"],
  "proposed_module_destinations": {"10": "boundary/evidence handoff investigation"},
  "seal_status": "NOT SEALED",
  "ci_status": "CHECK ACTIONS ON TIP",
  "reproducibility_status": "NOT ESTABLISHED IN THIS SESSION",
  "review_status": "RED-TEAM DOCUMENTED",
  "final_admission_status": "NO NEW ADMISSION",
  "evidence_hash": null
}
```

Fill numeric fields and `evidence_hash` only after a real local or CI run against the exact tip. Do not invent them.

---

## Non-claims

- This document is not a seal.
- Passing architecture-boundary unit tests is not architectural admission of Module 10.
- SHA-256 integrity checks are not digital signatures.
- CI green on an older commit does not seal this tip.

**Do not claim what the code cannot demonstrate.**
