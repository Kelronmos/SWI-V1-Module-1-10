# SWI Security Invariants

**Status:** SPECIFICATION / PROPOSED for system-wide kernel  
**Date:** 18 September 2026  

These are **target invariants**. Listing them here does **not** mean every
module implements all of them. Point to code + tests before claiming a row is
enforced.

| # | Invariant | Typical enforcement locus |
|---|-----------|---------------------------|
| 1 | DENY must not create a protected external side effect | Action boundary |
| 2 | HALT must prevent consequential execution until a valid transition | Kernel / Trainer |
| 3 | ALLOW must identify the policy version used | Authz / policy (future) |
| 4 | Consequential ALLOW requires all mandatory evidence | Authz |
| 5 | Invalid/expired/revoked authority must fail closed | AccessAuth / ReplayGuard |
| 6 | Protected receipt modification must be detectable | Hash chains / seals |
| 7 | Consumed one-time authority must reject replay | ReplayGuard (opt-in) |
| 8 | A receipt must permit reconstruction of the decision path | Audit / evidence |
| 9 | LLM-generated text is not execution authority | Authority boundary |
| 10 | Deterministic kernel inputs → deterministic decisions under deterministic contract | Canonicalization + policy |

**Related live fragments:** fail-closed M08/M09, M11 unexpected fields, Lane A
authority non-escalation, Lane B canonicalization_v0, optional ReplayGuard.
