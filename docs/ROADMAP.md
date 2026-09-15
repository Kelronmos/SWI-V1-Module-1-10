# SWI Roadmap (locked)

## Phase A — V1 Foundation (current)

```text
M06 sealed (evidence recorded)
  → M07 / M09 decisions + evidence package
  → M01 / M04 / M08 / M10 boundary review
  → M00 final integration evidence
  → adversarial + claim audit
  → clean clone + exact-tip CI
  → FOUNDATION_SEAL_5_RECORD.md
  → binary: PASSED | NOT READY
```

**Current decision: FOUNDATION SEAL 5 — NOT READY**

## Phase B — Trust Boundary (after or parallel to A, no Seal 5 claim)

```text
CA / cert profile freeze
  → task envelope + canonical serialization
  → key lifecycle / rotation / revocation / replay
  → CRTG implement + negative tests + CI
```

Status: **PROPOSED / DESIGN PENDING**

## Phase C — V1 → V2

```text
Real V1 Foundation Evidence export
  → CRTG
  → M11 against real evidence (not fixtures only)
  → AdmittedInput
  → V2 Kernel
```

Blocked until Seal 5 PASS + contract derived from V1.

## Phase D — V2 modules

```text
M12 → test → freeze → M13 → … → M22
```

One module at a time. No parallel “finish 12–22.”

## Anti-goals

- More modules instead of evidence  
- Certificates as truth engine  
- V2 claiming V1 verified what V1 did not  
- “Almost sealed”
