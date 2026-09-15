# SWI Upgrade & Progressive Repository Integration Manual

**Status:** PROPOSED — Upgrade Governance Manual  
**Date:** 15 September 2026  
**Author:** Keletso Ronald Mosidila — Trusts Motion

## Core rule

«SWI advances by proven contracts, not by module-count symmetry.»

Evidence before expansion.  
A repository does **not** need Modules 00–10 because another has 00–10.

## Progression question

Not: *Has every repository reached Module 10?*  
Yes: *Has the dependency required by the next boundary been sufficiently proven?*

## Repository classes

| Class | Role | Examples |
|-------|------|----------|
| A | Foundation / kernel | V1 00–10, V2 Kernel |
| B | Admission / contract | M11, future CRTG |
| C | Processing engines | Math engine, Rust, Firefly |
| D | Adapters | External services |

Class C/D need **their interface contract**, not a copy of V1 modules.

## Readiness levels (governance only — not “% safe”)

| Band | Label |
|------|--------|
| 0–39% | Exploration / PROPOSED |
| 40–59% | Prototype |
| 60–74% | Development Ready (IMPLEMENTED / TESTED) |
| 75–84% | Integration Ready |
| 85–94% | Boundary Ready |
| 95–100% | Seal candidate → **SEALED** only with explicit evidence |

**Critical blockers override any high percentage.**

Suggested gates: design next ≥75% · implement next ≥85% dependency · seal dependent ≥95% prior boundary.

## 10-at-a-time rule — retired

Replaced by: complete the **minimum contract** for the next dependency boundary.

## Parallel development

Allowed. Integration claims only when the adapter/contract is evidenced.

## Two tracks (do not collapse)

**Track 1 — Foundation**  
`V1 → FoundationEvidenceEnvelope → M11 → Kernel`

**Track 2 — Trust**  
`TaskEnvelope → cert profile → trust policy → rotation → CRTG`

CRTG must **not** block Foundation Seal work.

## Current position (honest)

| Item | Status |
|------|--------|
| V1 Foundation Evidence export | IMPLEMENTED / TESTED (unsigned) |
| V2 M11 | IMPLEMENTED / TESTED · NOT SEALED |
| Ed25519 primitive | IMPLEMENTED / TESTED · not CRTG |
| CRTG | PROPOSED |
| M12–22 bulk | **Do not implement as a batch** |
| Foundation Seal 5 | **NOT READY** |

## Immediate target

Foundation → Admission → Trust **specification** — not M13…M22 for calendar reasons.

## Claim language

Use: IMPLEMENTED · TESTED · CI VERIFIED · INTEGRATION READY · BOUNDARY READY · SEALED · PROPOSED · DESIGN PENDING · NOT IMPLEMENTED.

Never: “90% secure” · certificate = truth · M11 verifies truth · all repos must be V1-shaped.
