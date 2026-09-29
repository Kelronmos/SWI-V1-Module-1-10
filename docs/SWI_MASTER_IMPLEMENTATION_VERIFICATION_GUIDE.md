# SWI — Master Implementation & Verification Guide

**Open-Source Protection + Change Control + Replay + Violation Governance + Reproducibility**

Project: Structured Workflow Intelligence  
Repository: Kelronmos/SWI-V1-Module-1-10  
Primary objective: strengthen the existing bounded Source Admission / Replay vertical slice without falsely closing any broader SWI formation-path claims.

> This document is the control surface for implementation agents.  
> Inspect live code before modifying. Never manufacture a “passed” result.

---

## 1. Non-negotiable evidence discipline

```
CLAIM → IMPLEMENTATION → TEST → RESULT → LIMITATION → NEXT ITERATION
```

Never: `DOCUMENTATION → CLAIM`.

**Core principles:** HASH ≠ AUTHORITY ≠ TRUTH · SOURCE CODE ≠ AUTHORITY · POLICY ≠ ENFORCEMENT · DECISION ≠ EXECUTION · WARNING ≠ AUTHORIZATION · SCAN ≠ APPROVAL · PULL ≠ TRUST · SEALED ≠ PRODUCTION TRUST

**Statuses (only when demonstrated):** NOT_PROVEN · OPEN · SPECIFIED · IMPLEMENTED · TESTED · REPLAYABLE_BOUNDED · INDEPENDENTLY_VERIFIED · PROVEN_WITHIN_SCOPE · SEALED

Do not upgrade status because code/docs/tests/hash/CI/developer-assurance exist alone.

---

## 2. Inspect before modify

Inspect at minimum:

- `swi_core/source_admission/` (models, decision, evidence, halt, replay, claims, change_control, open_source)
- `test/adversarial/test_source_admission_*.py`
- `docs/SWI_EXTERNAL_SOURCE_ADMISSION_*.md`, `formation_path_inventory.json`, `TIP_CI_STATUS.md`, `status/`
- `requirements.txt`, CI workflows, LICENSE, NOTICE, SECURITY.md

Record base SHA, working tree, CI state. Do not assume an earlier tip.

---

## 3. Preserve existing source-admission contract

```
EXTERNAL SOURCE → evaluate_source → PASS/WARNING/HALT
HALT → protected operation MUST NOT execute → side_effects = 0
```

Add around this; do not weaken it.

---

## 4–11. Open-source protection + claim slots + change control

- Distinct dimensions: IDENTITY · LICENCE · AUTHORITY · SECURITY · PRIVACY · ARCHITECTURE · LEGAL INTERPRETATION — never one `approved=True`
- Claim slots must not silently expand (e.g. LICENSE_IDENTIFIED ↛ LEGAL_COMPLIANCE)
- Material change → invalidate inherited admission → revalidate → new evidence hash → new admission; preserve history (`supersedes`)
- No silent inheritance of A1 onto mutated component

---

## 12–22. Replay + violation governance

Layered failures (not generic INVALID). Access levels 0–4.  
`REPLAY_LIMITED_BY_ACCESS_CONTEXT` ≠ original decision false.  
Violation → PAUSE → report → 3 questions → disposition; CONTINUE only with explicit scoped authority.  
BLOCK ⇒ side_effects = 0.

Legal language: use `*_UNPROVEN` / `*_UNVERIFIED` / `*_REVIEW_REQUIRED` — never auto-adjudicate GDPR/copyright infringement.

---

## 23–49. Dependencies, reproducibility, test matrix, invariants

See full checklist in repository history / agent briefings. Invariants A–J must hold.  
**Do not close FM-005–013, Universal Gate, Foundation Seal 5, or regulatory compliance** from this slice alone.

---

## 50–56. Commands, git, final claim language

Use project pytest / `./scripts/verify.sh`. Status after tests only.  
Allowed bounded claim when tests pass: open-source protection + change-control IMPLEMENTED+TESTED within defined scope; material changes require revalidation; replay REPLAYABLE_BOUNDED within contract.  
Must also state: does not prove Universal Gate, production trust, legal compliance, or FM-005–013 closure.

**Central invariant:** SWI does not trust the previous state merely because the new state came from the same source. Every material change must earn its next admission through evidence.
