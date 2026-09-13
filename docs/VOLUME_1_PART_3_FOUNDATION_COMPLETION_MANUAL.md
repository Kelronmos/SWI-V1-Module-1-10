# THE SWI ARCHITECTURE

## VOLUME 1, PART 3 — FOUNDATION COMPLETION & VERIFICATION MANUAL

**Modules 00–10**  
A step-by-step technical guide for completing, testing, documenting and sealing the SWI foundation  

**PART A — Policy, order & seals**  
**PART B — Build procedures, test protocols & release control**  
**PART C — Evidence execution, release control & transition**  

Keletso Ronald Mosidila — Lead Architect & Author — Trusts Motion  
Gaborone, Botswana — 2026  

---

## PART A — POLICY, ORDER & SEALS

### 1. PURPOSE

This manual is a construction guide for what must be implemented, tested and verified **now**.

> Finish the foundation before building another floor.

Governing chain:

> Claim → Implementation → Test → Result → Limitation → Next iteration  

If a component cannot demonstrate that chain, it remains unfinished.  
Modules **11–19 stay BLOCKED** until Foundation Seal 5.

### 2. CURRENT FOUNDATION POSITION

| Module | Status |
|--------|--------|
| 02 Security Probe | **SEALED** (kernel + Trainer halt + local + CI) |
| 05 Redaction | **KERNEL-ENFORCED** (structured PII only; confirm CI on M05 commits) |
| 03, 06, 07, 09, 01, 04, 08, 10 | Not yet kernel-migrated |
| 00 Trainer | Halt on M02/M05; final integration after remaining seams |

**Module 05 meaning (preserved):** EMAIL, PHONE, CREDIT_CARD, BW_OMANG — not complete PII, not NLP.

### 3–11. Core policy

- Six questions before every module; migration pattern `pre → _impl → post`
- Order: 02 SEALED → 05 KERNEL-ENFORCED → **03 NEXT** → 06 → 07 → 09 → 01 → 04 → 08 → 10 → 00 final → Seal 5
- Trainer: `halted_by_module_XX_kernel` + best-effort record; never swallow halt
- Language: fail-closed / tamper-evident / structured first-pass — not universal security

See also: `docs/MODULE_05_EVIDENCE.md`, `docs/MODULE_05_SEAL_RECORD.md`.

---

## PART B — BUILD PROCEDURES

Session: `git status` → `pytest -q` → `./scripts/verify.sh` → baseline.  
Per module: INSPECT → CONTRACT → PRESERVE → KERNEL → TESTS → TRAINER HALT → DOCUMENT → CI → NEXT.  
Module 03: deterministic timestamps; X−1/X/X+1 staleness; flags ≠ automatic block unless policy changes.

---

## CORRECTED MODULE 05 POSITION

Module 05 is **already** kernel-wrapped. Do **not** rebuild.

> VERIFY → HARDEN EVIDENCE → DOCUMENT → CONFIRM CI → Module 03.

Evidence: `docs/MODULE_05_SEAL_RECORD.md`.

---

## PART C — EVIDENCE EXECUTION, RELEASE CONTROL & TRANSITION

### Do not manufacture evidence

CODE → TEST → RESULT → DOCUMENT.  
Never DOCUMENT → ASSUME → IMPLEMENTED.  
States only: **VERIFIED** | **FAILED** | **UNVERIFIED** | **NOT IMPLEMENTED**.

### Module 05 evidence record

Use `docs/MODULE_05_SEAL_RECORD.md`. Mark CI PASS only from Actions.

### Discipline

One logical change per commit. Review diff. Detection ≠ understanding. Bounded claims.

### Module 03 after M05 CI seal

READ SOURCE → TESTS → CONFIG → TRAINER → CONTRACT → LIMITATIONS → then code.  
Dependency: 03 → 06 → 07 → 09 → 01 → 04 → 08 → 10 → 00.  
Later modules do not validate earlier ones.

### Evidence execution

Clean clone · commit SHA · positive/negative/adversarial · failure propagation · logging ≠ enforcement · claim-language review.

### Vocabulary

PLANNED → DESIGNED → IMPLEMENTED → TESTED → VERIFIED → SEALED

### Foundation Seal 5

Release gate, not celebration. Candidate → full matrix → seal or return to failed boundary.

### Immediate state

```text
Module 02 SEALED (prior CI)
Module 05 KERNEL-ENFORCED + local evidence (MODULE_05_SEAL_RECORD)
        → confirm CI
        → Module 03 NEXT
Modules 11–19 BLOCKED until Foundation Seal 5
```

### Principle

> Do not ask the system to be trusted before establishing what it does, what happens when it fails, and what evidence supports the claim.
