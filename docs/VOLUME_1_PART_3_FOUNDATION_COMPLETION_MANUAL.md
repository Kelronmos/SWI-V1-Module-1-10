# THE SWI ARCHITECTURE

## VOLUME 1, PART 3 — FOUNDATION COMPLETION & VERIFICATION MANUAL

**Modules 00–10**  
Kernel Migration, Adversarial Verification, CI Evidence & Foundation Seal  

Keletso Ronald Mosidila — Lead Architect & Author — Trusts Motion  
Gaborone, Botswana — 2026  

---

### 1. PURPOSE

This manual defines the work required to complete and independently verify the SWI V1 Modules 00–10 foundation **before** beginning Modules 11–19.

Governing rule:

> Claim → Implementation → Test → Result → Limitation → Next Iteration  

No feature should be described more strongly than its implementation and evidence permit.

---

### 2. CURRENT FOUNDATION STATUS (as of Module 05 landing)

```text
Modules 00–10
       │
       ├── Existing implementations + tests + docs
       └── ModuleKernel foundation
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
    Module 02              Module 05
     SEALED              KERNEL-ENFORCED
   (CI witness)        (await CI on M05 commits)
```

**Module 05** remains a **structured PII first-pass** (email, phone, card-shaped, BW Omang). It does **not** claim complete PII detection.

Modules 11–19 remain **BLOCKED** until Foundation Seal 5.

---

### 3. ZERO-GROUND RULE

Before modifying any module:

1. Read current implementation  
2. Read current tests  
3. Identify behavior, claims, limitations  
4. Add enforcement around behavior  
5. Do **not** silently redefine the module  

Migration is: existing behavior → explicit contract → kernel → adversarial tests → Trainer boundary → documentation → CI evidence.

---

### 4. WHAT KERNEL MIGRATION MEANS

```text
INPUT → PRECONDITIONS → OPERATION → POSTCONDITIONS → OUTPUT
```

Pre-fail → operation does not run → halt.  
Post-fail → output not released → halt.  

A kernel is an **enforcement boundary**, not proof that the underlying algorithm is universally safe.

Use: *fail-closed contract enforcement*.  
Avoid: *universally secure* / *impossible to bypass*.

---

### 5. MIGRATION ORDER

| Order | Module | Status |
|-------|--------|--------|
| 1 | 02 Security Probe | **SEALED** (local + CI) |
| 2 | 05 Redaction | **KERNEL-ENFORCED** (structured PII only) |
| 3 | 03 Context Sync | NEXT |
| 4 | 06 Drift | pending |
| 5 | 07 Memory Validator | pending |
| 6 | 09 Audit Logger | pending |
| 7 | 01 Node Scanner | pending |
| 8 | 04 Encryption | pending |
| 9 | 08 Access Auth | pending |
| 10 | 10 External Sandbox | pending |
| 11 | 00 Trainer final review | after seams |
| — | Full adversarial + CI verify.sh + clean clone | then **Seal 5** |
| — | Modules 11–19 | **only after Seal 5** |

---

### 6. MODULE 05 CONTRACT (completed pattern)

| Layer | Requirements |
|-------|----------------|
| Pre | `str`; length ≤ 100_000 |
| Operation | existing `_redact_impl` detection meaning |
| Post | `RedactionResult`; matches are `RedactionMatch`; categories ⊆ {EMAIL, PHONE, CREDIT_CARD, BW_OMANG}; valid ordered non-overlapping spans |
| Trainer | `halted_by_module_05_kernel` → record → re-raise; drift must not run |

Evidence: `docs/MODULE_05_KERNEL_MIGRATION.md`, `test/test_redaction_kernel.py`, `test/test_trainer_module05_halt.py`, adversarial boundaries.

---

### 7. PER-MODULE CONTRACT THEMES (remaining)

| Module | Focus |
|--------|--------|
| **03 Context Sync** | input/timestamp/staleness/output; deterministic timestamps in tests |
| **06 Drift** | exact Green/Yellow/Red boundary values; malformed inputs |
| **07 Memory Validator** | structure, types, tamper-evident hash behavior (not “tamper-proof”) |
| **09 Audit Logger** | record shape; logging failure must never convert halt → success |
| **01 Node Scanner** | path/hash integrity; tamper-*evident* language |
| **04 Encryption** | encrypt/decrypt round-trip; wrong key/nonce/tag fail closed |
| **08 Access Auth** | deny unauthorized; no “warn and continue” |
| **10 Sandbox** | timeout/exception/resource; do not claim OS isolation unless proven |
| **00 Trainer** | every sealed seam: failure stops pipeline; no silent continue |

---

### 8. MIGRATION TEMPLATE (every module)

1. Inventory implementation + tests + limitations  
2. Write pre/post contract  
3. Wrap with `ModuleKernel`; keep `_impl` for existing meaning  
4. Precondition / postcondition / “operation never ran” tests  
5. Adversarial boundary tests  
6. Trainer halt + downstream-not-called tests  
7. Update IMPLEMENTATION_STATUS, EVIDENCE_MATRIX, KNOWN_LIMITATIONS  
8. `pytest` + `./scripts/verify.sh`  
9. Push → wait for CI → inspect  
10. Only then next module  

---

### 9. TRAINER BOUNDARY RULE

```text
try:
    result = module.operation(...)
except ModuleKernelError as exc:
    reason = f"halted_by_module_XX_kernel:{exc}"
    self._record_halt(reason)   # best-effort
    raise ModuleKernelError(reason) from exc
```

Best-effort audit/memory **must never** swallow the halt.

---

### 10. VERIFICATION

**Local:** `python -m pytest -q` then `./scripts/verify.sh`  

**CI:** pytest matrix 3.10–3.12 + doc/claim checks; prefer also running `./scripts/verify.sh`  

**Clean clone:** fresh venv, install, pytest, verify.sh must reproduce.

`verify.sh` reports evidence. It does **not** prove universal security, complete PII, or production readiness.

---

### 11. FOUNDATION SEAL 5 CHECKLIST

- [x] M02 kernel sealed (+ CI)  
- [x] M05 kernel-enforced (+ local tests; confirm CI)  
- [ ] M03, M06, M07, M09 kernel-sealed  
- [ ] M01, M04, M08, M10 boundary-reviewed  
- [ ] Trainer final integration  
- [ ] Adversarial suite green  
- [ ] Full pytest + verify.sh green  
- [ ] CI green (prefer full verify.sh)  
- [ ] Clean clone reproduces  
- [ ] Evidence matrix + known limitations current  
- [ ] No unsupported security claims  

Until complete: **MODULES 11–19 = BLOCKED**.

---

### 12. FINAL PRINCIPLE

> Build only what can be explained, tested, and defended.  

A module is a foundation component when:

code + contract + tests + failure path + integration + CI + documented limitations  

Do not outrun the evidence.
