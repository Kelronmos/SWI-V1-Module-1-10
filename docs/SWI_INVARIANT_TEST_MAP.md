# SWI Security Invariant → Test Map

**Status:** AUDIT ARTIFACT (not a claim that all rows are enforced)  
**Date:** 18 September 2026  
**Rule:** NOT VERIFIED until a named test exists and passes on a recorded SHA.

| # | Invariant | Enforcement locus | Test evidence | Status |
|---|-----------|-------------------|---------------|--------|
| 1 | DENY no protected side effect | Action boundary | — | NOT VERIFIED |
| 2 | HALT blocks consequential execution | Kernel / Trainer | `test/test_trainer_kernel_halt.py` | PARTIAL |
| 3 | ALLOW records policy version | Authz | — | NOT VERIFIED |
| 4 | Mandatory evidence complete | Evidence / Authz | — | NOT VERIFIED |
| 5 | Authority fail-closed | M08 / ReplayGuard | `test/test_access_auth_malformed.py`, M08 unit tests | PARTIAL |
| 6 | Receipt/log tamper detection | Hash chains | M07/M09 tests, audit malformed | PARTIAL |
| 7 | Replay rejection | ReplayGuard (opt-in) | V2 replay tests if present | PARTIAL / contract-dependent |
| 8 | Decision path reconstructable | Audit / evidence | foundation export tests | PARTIAL |
| 9 | LLM text ≠ authority | Authority boundary | `test/test_authority_non_escalation.py` | PARTIAL |
| 10 | Deterministic digests | Canonicalization | `test/test_canonical*.py`, golden vectors | PARTIAL |

Paths: V1 `swi_core/canonical.py`; V2 `swi_v2/kernel/canonical.py` (not `swi_core/` on V2).  
Fixtures: `test/fixtures/canonical_vectors.json` (not `tests/fixtures/`).
