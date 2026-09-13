# THE SWI ARCHITECTURE — VOLUME 1 PART 2

## Module Kernel, Verification, Hardening & Rebuild Manual
### Modules 00–10

**Author:** Keletso Ronald Mosidila — Trusts Motion, Gaborone, Botswana — 2026
**Phase:** Reconstruction / Hardening
**Rule:** Do not advance to Modules 11–19 until the foundation gate passes.

---

### 00. Purpose

Define how Modules 00–10 are rebuilt, tested, self-checked, integrated, reviewed, and sealed.

Historical textbook material (CEK, SAD-DFU, Vector Memory, Alita, 46 modules, Sovereign Mesh) may remain important to SWI history. It does **not** become current implementation by documentation alone.

**Authority hierarchy:** current code → automated tests → reproducible result → documentation → architectural/historical material.

---

### 01. Labels

| Label | Meaning |
|-------|---------|
| Implemented | Code exists |
| Tested | Automated test exercises behavior |
| Verified | Defined verification procedure passes and is reproducible |
| Partial | Only part of the capability exists |
| Architectural | Design exists; executable proof does not |
| Historical | Prior version or earlier design |
| Unknown | Insufficient evidence |

---

### 02. Rebuild principle

```text
QUESTION → CLAIM → CODE → TEST → FAIL/PASS → CORRECT → RETEST → DOCUMENT → REVIEW → RELEASE
```

Never: IDEA → DOCUMENTATION → ASSUMPTION → "IMPLEMENTED".

---

### 03. Self-checking requirement

```text
INPUT → MODULE PRE-CHECK → MODULE EXECUTION → MODULE POST-CHECK → HANDOFF
```

A module must validate the conditions under which it may operate and the result it intends to hand downstream.

---

### 04–06. Layers

1. **Module logic** — e.g. `SecurityProbe._scan_impl`
2. **Module Kernel** — pre → execute → post (`swi_core/module_kernel.py`)
3. **SWI Kernel** — future registry; do not implement prematurely

Existing `security/self_check.py` is a useful fail-closed primitive; it is not a full integrated architecture until module boundaries use a contract.

---

### 07. Module Kernel contract

Implemented as `ModuleKernel` / `CheckResult` / `ModuleKernelError` in `swi_core/module_kernel.py`.

- Pre-check failure → do not execute
- Post-check failure → do not release output
- Checks must return `CheckResult`; wrong type → fail closed

Keep the kernel small. Module-specific intelligence stays in the module.

---

### 08–16. Pilot: Module 02

**Pre-checks:** input is `str`; size ≤ 100_000 characters.
**Construction:** `block_threshold` in [0.0, 1.0].
**Post-checks:** result is `ProbeResult`; risk_score in [0, 1]; triggered is `list[str]`; blocked consistency.

**Integration pattern:** preserve detection algorithm; wrap via `kernel.run(text, self._scan_impl)`.

**Tests:** `test/test_module_kernel.py`, `test/test_security_probe_kernel.py`.

---

### 17–19. Trainer seam & migration order

Trainer should not convert kernel failure into `allowed=True`. Raising is acceptable for the pilot.

Recommended migration order: **02 → 05 → 03 → 06 → 07 → 09 → 01 → 04 → 08 → 10 → 00 final**.
Rule: one module → tests → review → next module.

Module 10 is late: OS boundary is not solved by a generic kernel wrapper.

---

### 20–32. Module-specific notes

See `docs/KNOWN_LIMITATIONS.md` and `docs/IMPLEMENTATION_STATUS.md`.
Historical concepts (CEK, SAD-DFU, Vector Scars, ChromaDB, Alita, Sovereign Mesh) stay outside current proof unless separately implemented.

---

### 33–39. Repo structure, scripts, CI

Target tree includes `docs/`, `scripts/verify.sh`, `scripts/repository_inventory.py`, `scripts/verify_docs.py`, `scripts/check_claim_language.py`, `.github/workflows/ci.yml`.

**CI rule:** a workflow *file* is not evidence; a *passing run* is evidence.

---

### 40–54. Testing discipline

Four classes: NORMAL / EDGE / ATTACK / FALSE POSITIVE.
Mutation-style review for weak tests.
Configuration range validation and explicit env precedence.
No silent `except: return default` on security paths.

---

### 55–56. Seal levels

| Seal | Meaning |
|------|---------|
| 0 | Reconstruction exists |
| 1 | Core automated tests pass |
| 2 | Module kernel pilot passes |
| 3 | Adversarial and boundary testing passes |
| 4 | Clean environment and CI pass |
| 5 | Independent engineer can understand, run, test, and challenge the foundation |

Only Seal 5 authorizes Modules 11–19.

---

### 57–75. Engineering law

- Never upgrade from memory alone.
- Expose uncertainty before it becomes downstream certainty.
- Never allow architecture documents to outrun the code.
- Final claim form: *“Modules 00–10 reconstructed and verified to the documented foundation standard”* plus explicit limitations — not *“SWI is complete.”*

**Development law:** Before work → verify. After work → verify again. If verification fails → do not hand off.

---

### Authorization to move forward

```text
MODULE 02 KERNEL → PROVEN → (migrate remaining) → TRAINER SEAM → ADVERSARIAL → CI → CLEAN REBUILD → SEAL 5 → Modules 11–19
```

END OF VOLUME 1 — PART 2
