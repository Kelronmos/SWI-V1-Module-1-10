# THE SWI ARCHITECTURE

## VOLUME 1, PART 3 — FOUNDATION COMPLETION & VERIFICATION MANUAL

**Modules 00–10**  
A step-by-step technical guide for completing, testing, documenting and sealing the SWI foundation  

**PART A — Policy, order & seals**  
**PART B — Build procedures, test protocols & release control**  

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

### 3. SIX QUESTIONS BEFORE EVERY MODULE

1. What does this module actually do?  
2. What does it receive?  
3. What does it return?  
4. What can go wrong?  
5. What must never happen?  
6. What evidence will prove it?  

### 4. MIGRATION PATTERN

```python
self.kernel = ModuleKernel(
    name="module_xx_name",
    pre_checks=(self._input_is_valid, ...),
    post_checks=(self._result_is_valid, ...),
)

def process(self, value):
    return self.kernel.run(value, self._process_impl)
```

Preserve behaviour first. Harden the boundary second. Improve functionality later.

### 5. MIGRATION ORDER (one module at a time)

```text
02 SEALED → 05 KERNEL-ENFORCED → 03 NEXT → 06 → 07 → 09
→ 01 → 04 → 08 → 10 → 00 final → adversarial → CI/verify/clean clone
→ FOUNDATION SEAL 5 → only then Modules 11–19
```

After each module: `pytest` → `./scripts/verify.sh` → commit → push → **wait for CI** → next.

### 6. MODULE 05 — COMPLETED PATTERN (reference)

| Layer | Contract |
|-------|----------|
| Pre | `str`; `len ≤ 100_000` |
| Op | existing `_redact_impl` (regex order unchanged) |
| Post | `RedactionResult`; matches valid, ordered, non-overlapping; categories ⊆ allowed set |
| Trainer | `halted_by_module_05_kernel` → record → re-raise; drift not called |

Evidence: `docs/MODULE_05_KERNEL_MIGRATION.md`, `test/test_redaction_kernel.py`, `test/test_trainer_module05_halt.py`, adversarial boundaries.

**Limitation (must stay visible):** structured pattern detection ≠ complete PII removal.

### 7. REMAINING MODULE THEMES

| Module | Contract focus |
|--------|----------------|
| **03 Context Sync** | input/timestamp/staleness; deterministic timestamps; X−1 / X / X+1 boundaries |
| **06 Drift** | score range; exact band boundaries (e.g. 0.02 / 0.08); reject non-numeric/NaN/bool-as-int traps |
| **07 Memory** | structural validity only — not “truth”; corruption → reject |
| **09 Audit** | record shape; audit failure ≠ erase security halt |
| **01 Node Scanner** | SHA-256 mismatch detection; tamper-*evident*, not tamper-proof |
| **04 Encryption** | AES-GCM round-trip; altered ciphertext/tag/key → fail closed |
| **08 Access Auth** | negative auth matrix; never default-allow |
| **10 Sandbox** | tested execution boundary only; no hardened isolation claim without proof |
| **00 Trainer** | every seam: halt + downstream not called |

### 8. TRAINER BOUNDARY RULE

```text
try:
    result = module.op(...)
except ModuleKernelError as exc:
    reason = f"halted_by_module_XX_kernel:{exc}"
    self._record_halt(reason)  # best-effort
    raise ModuleKernelError(reason) from exc
```

Best-effort audit/memory must **never** convert halt into success.

### 9. SECURITY LANGUAGE

Use: *fail-closed contract enforcement*, *tamper-evident*, *structured PII first-pass*.  
Avoid unsupported: *universally secure*, *tamper-proof*, *complete PII*, *cannot be bypassed*, *solves AI safety*.

### 10. FOUNDATION SEAL 5 CHECKLIST

- [x] M02 sealed (+ CI)  
- [x] M05 kernel-enforced (+ local; confirm CI)  
- [ ] M03, M06, M07, M09 kernel-sealed  
- [ ] M01, M04, M08, M10 boundary-reviewed  
- [ ] Trainer final integration + e2e happy/failure paths  
- [ ] Adversarial suite green  
- [ ] pytest + `./scripts/verify.sh` green  
- [ ] CI green (includes verify.sh on 3.12)  
- [ ] Clean clone reproduces  
- [ ] Evidence matrix + limitations + claim review current  
- [ ] No unsupported security claims  

**Seal 5 failure is useful** — fix the foundation; do not weaken the gate.

### 11. MODULES 11–19 ENTRY

Only after Seal 5. Do not start CEK, SAD-DFU, Vector Memory, global SWI Kernel, Alita, or universal safety as “implemented” until separately proven.

---

## PART B — BUILD PROCEDURES, TEST PROTOCOLS & RELEASE CONTROL

### 12. SESSION START

```bash
git branch --show-current
git status
git log --oneline -10
python -m pytest -q
./scripts/verify.sh
```

Record baseline commit, Python version, test count, result.  
If baseline fails, fix or document **before** attributing failures to the new change.

### 13. INSPECT BEFORE EDIT

```bash
# implementation
sed -n '1,260p' swi_core/moduleXX_....py
# callers
grep -R "ClassName" -n swi_core test
# existing tests
grep -R "method(" -n test
```

Discover dependencies before changing the contract.

### 14. SAFE MIGRATION SEQUENCE (per module)

1. Baseline green  
2. Copy behaviour into `_impl`  
3. Add `ModuleKernel` + pre/post  
4. Run **existing** tests  
5. Add kernel + adversarial tests  
6. Trainer halt + downstream-not-called tests  
7. Full suite + `verify.sh`  
8. Update IMPLEMENTATION_STATUS, EVIDENCE_MATRIX, KNOWN_LIMITATIONS  
9. Review `git diff`  
10. Small commits → push → **CI** → only then next module  

### 15. CRITICAL TEST PROPERTIES

| Property | How to prove |
|----------|----------------|
| Pre-fail → op never runs | spy / `called is False` |
| Post-fail → no release | result never returned |
| Trainer halt | `ModuleKernelError` with `halted_by_module_XX` |
| Downstream blocked | mock assert_not_called |
| Audit fail ≠ success | raise still occurs |
| Boundary values | exact threshold ± epsilon |

### 16. MODULE 03 BUILD NOTES

- Deterministic `timestamp=` in tests; no reliance on wall clock alone  
- Staleness: test `X-1`, `X`, `X+1` from config  
- Invalid time: missing, wrong type, malformed, future — policy from **code**, not invention  

### 17. MODULE 06 BUILD NOTES

Explicit band table (adjust to implementation if different):

| Score | Expected (if contract uses 0.02 / 0.08) |
|-------|----------------------------------------|
| 0.00 | Green |
| 0.019999 | Green |
| 0.020000 | Yellow |
| 0.079999 | Yellow |
| 0.080000 | Red |

Reject: `<0`, `>1`, NaN, inf; consider rejecting `bool` (`isinstance(True, int)` is True in Python).

### 18. MODULE 07 / 09 NOTES

- **07:** structure only, not truth; valid → accept; one-field corruption → reject  
- **09:** record contract from real fields; logger failure must not erase halt  

### 19. MODULE 01 / 04 / 08 / 10 NOTES

- **01:** known-good → match; one-byte change → mismatch; language = tamper-evident  
- **04:** round-trip + altered ciphertext/tag/key fail; key management is separate  
- **08:** negative matrix only; no default allow  
- **10:** document real boundary; failed escape tests → limitations, not marketing  

### 20. TRAINER FINAL REVIEW

For each sealed module:

```text
inject failure → Trainer raises → downstream.mock.assert_not_called()
```

End-to-end: one happy path + failure injection at each boundary.

### 21. ADVERSARIAL CLASSES

Input (empty, huge, wrong type, encoding) · Structural (missing/extra fields, overlap) · Security (override patterns, path traversal) · Failure (op/check/logger/memory exceptions).

### 22. TEST THE TESTS

Temporarily break a pre-check / halt / audit-swallow; suite **must** go red. Restore immediately.

### 23. ModuleKernel EDGE CASES

Pre/post fail · check exception · bad CheckResult type · op exception · multiple checks.  
Do **not** merge blindly with `security/self_check.py` — different `CheckResult` semantics until deliberately unified.

### 24. CONFIGURATION

Every security-sensitive config field: type, range, consumer, failure behaviour. Existence in YAML ≠ enforcement.

### 25. CI & CLEAN CLONE

- Local and CI should share `./scripts/verify.sh` (CI runs it on Python 3.12).  
- Clean clone: fresh venv → `pip install -r requirements.txt` → pytest → verify.sh.  
- No secrets in tree; dependencies declared in repo.

### 26. WHEN THINGS DISAGREE

| Conflict | Rule |
|----------|------|
| Docs vs code | Code wins; fix docs |
| Tests vs code | Decide intended contract; fix the wrong side — never weaken tests for green vanity |
| CI vs local | Reproduce, classify (code/test/env/dep/CI config), fix cause |

### 27. COMMIT DISCIPLINE

One logical change per commit. Example:

```text
feat: kernel-wrap Module 03
test: Module 03 contract + adversarial
feat: Trainer halt on Module 03 kernel failure
docs: Module 03 evidence + limitations
```

### 28. FINAL SEAL RECORD

When ready, create `docs/FOUNDATION_SEAL_5.md` with: commit, date, test/CI/clean-clone results, limitations, non-claims, decision SEALED / NOT SEALED.

Failed seal attempts are retained as engineering history.

### 29. IMMEDIATE NEXT ACTION

**Module 05 is already migrated.** Do not re-do it unless CI is red.

Next authorized work:

1. Confirm CI green for Module 05 + Part 3 commits  
2. **Module 03 Context Sync** — inspect source/tests → contract → kernel → tests → Trainer halt → verify → CI  
3. Then 06 → 07 → 09 → 01 → 04 → 08 → 10 → 00 final  

One module. One contract. One evidence chain. One verified step at a time.

---

## CLOSING

SWI becomes stronger when a claim survives code, tests, failure, verification, review and reproducibility — not when documentation sounds complete.

> Do not rush the architecture. Verify the ground first.
