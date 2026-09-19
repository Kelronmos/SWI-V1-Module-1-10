# Packaging and Release Status

**Tip context:** main after admission wiring (`a90fb0f…` and later)  
**Document date:** 2026-09-19

---

## Corrected security status (do not use stale notes)

| Item | Status |
|------|--------|
| Trainer.process admission | **WIRED** — required keyword `admission: AdmissionDecision`; check before `_turn_counter++` |
| export / sign admission | **WIRED** |
| Pre-admission `_record_halt` | **Not invoked** on admission reject |
| Direct M02–M09 APIs | **Ungated residual** |
| ModuleKernel default | `require_admission=False` |
| Universal Gate | **NOT PROVEN** |
| Module 10 | **PROPOSED / NOT ADMITTED** |
| Foundation Seal 5 | **NOT READY** |

Stale claim “Trainer.process NOT WIRED” is **false** as of the admission commits.

---

## Actual tree (not a fictional swi_v1 module set)

Package boundary is **`swi_core/`** only:

- `admission_boundary.py`, `module_kernel.py`, `module00_trainer.py`, …
- There is **no** `swi_v1/` package of `swi_module_00_contract.py` … `swi_module_10_boundary.py` as the live implementation.
- Do **not** add a compatibility façade that pretends those filenames are the implementation.

---

## Packaging present vs proposed

| Component | Status |
|-----------|--------|
| `pyproject.toml` | **Alpha only** — `0.1.0a1`, Development Status :: 3 - Alpha |
| Name | `swi-v1-core` (import: `swi_core`) |
| Production/Stable classifier | **Forbidden** while Universal Gate NOT PROVEN |
| Version 1.0.0 | **Do not tag/publish** yet |
| Fail-closed `__init__` security exports | **Yes** — no `try/except ImportError` soft fallback |
| PyPI publish workflow | **Absent** |
| Build → hash → clean-install → test artifact | **NOT VERIFIED** |
| SHA256SUMS release evidence | **NOT GENERATED** |
| Atomic PyPI + GitHub release | **NOT ACHIEVED** |
| Coverage fail_under enforced in CI | **Partial** — CI runs `--cov` but threshold not release-blocking at 90% |
| Python matrix | CI: 3.10 / 3.11 / 3.12 |

---

## Release architecture (target — not implemented)

```text
SOURCE COMMIT
    → Architecture / adversarial / admission tests
    → BUILD ONCE (wheel + sdist)
    → SHA-256 manifest
    → CLEAN INSTALL exact wheel (no source tree on path)
    → Run security suite against installed package
    → Version equality (tag == pyproject == installed)
    → GitHub draft + evidence
    → Human review
    → PyPI publish exact artifact
```

Principle: **publish only the artifact that passed verification.**

---

## Do not

- Publish `1.0.0` or Production/Stable while Universal Gate is NOT PROVEN
- Soft-fallback missing `AdmissionDecision` to `None`
- Treat tag push as security evidence
- Mix `unittest discover` patterns that diverge from `pytest` discovery
- Claim Modules 00–10 are sealed because a wheel builds

---

## Next engineering order

1. Close residual direct-API / child-kernel ungated paths (or mark internal + CI)  
2. Local `./scripts/verify.sh` on tip  
3. Then optional: build once + clean-install security tests  
4. Only after Universal Gate candidate + independent verification: consider beta/rc  
5. Module 10 / Foundation Seal 5 remain separate evidence tracks  

**Do not claim what the code cannot demonstrate.**
