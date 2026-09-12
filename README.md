# Structured Workflow Intelligence (SWI)

## Modules 00–10 — Verified Reference Implementation

**Author:** Keletso Ronald Mosidila  
**Organisation:** Trusts Motion  
**Status:** Active Reconstruction / Verified Reference Implementation

---

## What This Repository Is

This repository contains the **currently verified implementation of the SWI Modules 00–10 reference implementation**.

It establishes a local, single-process, reproducible engineering foundation for components that can currently be demonstrated through source code, executable tests, and documented behaviour.

This repository is **not a complete reconstruction of the broader SWI architecture** or of every capability, prototype, research direction, or architectural concept previously explored under SWI.

> **What is implemented must be distinguishable from what is remembered, proposed, or intended.**

---

## Verification Boundary

The current repository should be evaluated from the **code, tests, and documented behaviour** rather than from architectural claims alone.

| Status | Meaning |
|---|---|
| **Implemented** | Functionality exists in the repository and can be inspected in source code. |
| **Tested** | Functionality is supported by executable automated tests. |
| **Architectural** | A design or mechanism is defined as a direction but is not sufficiently implemented and verified here. |
| **Historical** | A capability or prototype may have existed in earlier development but cannot currently be reconstructed from surviving evidence. |

These categories are deliberately kept separate.

The rebuild therefore prioritises **reproducibility over reconstruction by memory**.

> **Remembering that something existed is not the same as being able to prove that it exists.**

---

## Current Scope

The current repository establishes a verified implementation foundation for the **Modules 00–10 reference implementation**.

It provides a local, single-process workflow in which **Module 00 — Trainer** is the primary orchestrator for the modules currently wired into its execution path.

### Integrated Pipeline

```text
Input
  │
  ▼
Module 00 — Trainer
  │
  ├── Module 02 — Security Probe
  ├── Module 03 — Context Sync
  ├── Module 05 — Redaction
  ├── Module 06 — Drift Detection
  ├── Module 07 — Memory Validator
  └── Module 09 — Audit Logger
