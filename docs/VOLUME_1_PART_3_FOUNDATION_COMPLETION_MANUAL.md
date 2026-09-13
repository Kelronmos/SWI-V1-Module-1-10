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

Evidence: `docs/MODULE_05_KERNEL_MIGRATION.md`, `docs/MODULE_05_EVIDENCE.md`, kernel/Trainer/adversarial tests.

**Limitation (must stay visible):** structured pattern detection ≠ complete PII removal.

### 7. REMAINING MODULE THEMES

| Module | Contract focus |
|--------|----------------|
| **03 Context Sync** | input/timestamp/staleness; deterministic timestamps; X−1 / X / X+1 boundaries |
| **06 Drift** | score range; exact band boundaries; reject non-numeric/NaN |
| **07 Memory** | structural validity only — not “truth” |
| **09 Audit** | record shape; audit failure ≠ erase security halt |
| **01 Node Scanner** | SHA-256 mismatch; tamper-evident, not tamper-proof |
| **04 Encryption** | AES-GCM round-trip; altered data fail closed |
| **08 Access Auth** | negative auth matrix; never default-allow |
| **10 Sandbox** | tested boundary only; no hardened isolation without proof |
| **00 Trainer** | every seam: halt + downstream not called |

### 8. TRAINER BOUNDARY RULE

```text
try:
    result = module.op(...)
except ModuleKernelError as exc:
    reason = f"halted_by_module_XX_kernel:{exc}"
    self._record_halt(reason)
    raise ModuleKernelError(reason) from exc
```

Best-effort audit/memory must **never** convert halt into success.

### 9. SECURITY LANGUAGE

Use: *fail-closed contract enforcement*, *tamper-evident*, *structured PII first-pass*.  
Avoid: *universally secure*, *tamper-proof*, *complete PII*, *cannot be bypassed*.

### 10. FOUNDATION SEAL 5 CHECKLIST

- [x] M02 sealed (+ CI)  
- [x] M05 kernel-enforced (+ local tests; confirm CI)  
- [ ] M03, M06, M07, M09 kernel-sealed  
- [ ] M01, M04, M08, M10 boundary-reviewed  
- [ ] Trainer final integration  
- [ ] Adversarial suite / verify.sh / CI / clean clone  
- [ ] Evidence matrix + limitations current  

Until complete: **MODULES 11–19 = BLOCKED**.

---

## PART B — BUILD PROCEDURES

### Session start

```bash
git status && git log --oneline -10
python -m pytest -q && ./scripts/verify.sh
```

### Per-module sequence

INSPECT → CONTRACT → PRESERVE BEHAVIOUR → KERNEL → TESTS → TRAINER HALT →
DOCUMENT → verify.sh → COMMIT → CI → NEXT MODULE ONLY

### Module 03 notes

Deterministic timestamps; staleness X−1 / X / X+1; stale/out_of_order are **flags**, not automatic pipeline blocks unless policy changes.

### Immediate next action

**Module 05 is already migrated.** Do not rebuild.

1. Confirm CI green for Module 05 evidence commits  
2. **Module 03** when authorized  
3. Then 06 → 07 → 09 → 01 → 04 → 08 → 10 → 00 final  

---

## CORRECTED MODULE 05 POSITION

Module 05 is **already** implemented and kernel-wrapped. Do **not** rebuild it.

Next M05 work is:

> VERIFY → HARDEN EVIDENCE → DOCUMENT → CONFIRM CI → then Module 03.

### Verification principle

Do not only prove redaction on good input. Prove the contract survives bad input:

- pre-fail → operation does not run  
- post-fail → output not released  
- Trainer halt; downstream not called  
- audit failure cannot convert halt into success  

### Evidence locations

See `docs/MODULE_05_EVIDENCE.md`.

### Corrected build loop (remaining modules)

INSPECT → DEFINE CONTRACT → PRESERVE BEHAVIOUR → ENFORCE → UNIT/ADVERSARIAL →  
INTEGRATE → FORCE FAILURE → VERIFY HALT → DOCUMENT → verify.sh → COMMIT → CI → NEXT

Immediate sequence: **seal M05 evidence (CI)** → **Module 03** → 06 → 07 → 09 → 01 → 04 → 08 → 10 → 00 final.

---

## CLOSING

> Do not rush the architecture. Verify the ground first.
