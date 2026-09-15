# SWI Pre-Name Map — V1 (Modules 00–10)

**Purpose:** Preserve the original SWI architectural language alongside the numbered module structure for teaching and continuity.

**Rule:**

> Pre-Name explains what the module means.  
> The contract, code, tests and seal determine what the module actually does.

A Pre-Name is **not** permission to implement functionality.  
A Pre-Name does **not** change runtime behaviour.

This document is teaching metadata only. It does not alter packages, imports, tests, CI, or sealed contracts.

Source of Pre-Names: *SWI Architecture — Volume 2: The Technical Codex*.

---

## Module map

| Number | SWI Pre-Name |
|--------|--------------|
| **M00** | THE TRAINER (THE MASTER ORCHESTRATOR) |
| **M01** | THE NODE SCANNER (THE INTEGRITY PROBE) |
| **M02** | THE SECURITY PROBE (SHADOW PROMPT DETECTION) |
| **M03** | CONTEXT SYNC (TEMPORAL ALIGNMENT) |
| **M04** | ENCRYPTION HANDLER (AES-256 SHIELDS) |
| **M05** | REDACTION ENGINE (PII NEUTRALIZATION) |
| **M06** | DRIFT ANALYZER (THE TOLERANCE GOVERNOR) |
| **M07** | MEMORY VALIDATOR (SCAR INTEGRITY) |
| **M08** | ACCESS AUTH (THE IDENTITY ANCHOR) |
| **M09** | AUDIT LOGGER (THE IMMUTABLE FLIGHT RECORDER) |
| **M10** | EXTERNAL SANDBOX (THE AIR-GAP SHIELD) |

---

## Teaching format

When referring to a module in documentation or teaching materials, prefer:

```text
M02 — THE SECURITY PROBE (SHADOW PROMPT DETECTION)
```

When referring to implementation authority, prefer:

```text
M02 contract / tests / seal record
```

---

## What this file does **not** do

- Does not rename any Python package, class, or function
- Does not change sealed contracts
- Does not alter test expectations
- Does not change CI workflows
- Does not create new dependencies
- Does not claim that a Pre-Name is implemented merely because it appears here

---

## Governing principle

«DO NOT CLAIM WHAT THE CODE CANNOT DEMONSTRATE.»

The name tells us what we were trying to solve.  
The contract tells us what we agreed to build.  
The code tells us what we actually built.  
The tests tell us what we observed.  
CI tells us whether we can reproduce it.  
The audit tells us whether the evidence satisfies the gate.  
The seal tells us whether that defined dependency may be used.
