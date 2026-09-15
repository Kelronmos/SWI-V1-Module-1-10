# SWI Upgrade & Progressive Repository Integration Manual

**Status:** PROPOSED — Upgrade Governance Manual  
**Date:** 15 September 2026  
**Author:** Keletso Ronald Mosidila — Trusts Motion

## Core rule

«SWI advances by proven contracts, not by module-count symmetry.»

## Constitutional rule

> A readiness percentage may authorize investigation or integration preparation, but it can **never** override a failed critical dependency or integrity gate.

Project completeness ≠ dependency readiness.

## Progression question

Not: *Has every repository reached Module 10?*  
Yes: *Has the dependency required by the next boundary been sufficiently proven?*

## Repository classes

| Class | Role | Examples |
|-------|------|----------|
| A | Foundation / kernel | V1 00–10, V2 Kernel |
| B | Admission / contract | M11, future CRTG |
| C | Processing engines | Math, Rust, Firefly |
| D | Adapters | External services |

Class C/D need **their interface contract**, not a copy of V1 modules.

## Readiness bands (governance only — not “% safe”)

| Band | Label |
|------|--------|
| 0–39% | Exploration / PROPOSED |
| 40–59% | Prototype |
| 60–74% | Development Ready |
| 75–84% | Integration Ready |
| 85–94% | Boundary Ready |
| 95–100% | Seal candidate (seal only with explicit evidence) |

**Critical blockers override any high percentage.**

## Two tracks (do not collapse)

**Track 1 — Foundation:** V1 → FoundationEvidenceEnvelope → M11 → Kernel  
**Track 2 — Trust:** TaskEnvelope → cert profile → trust policy → CRTG  

CRTG must not block Foundation Seal work; foundation work must not claim sender authentication without CRTG.

## Current position

| Item | Status |
|------|--------|
| V1 Foundation Evidence export | IMPLEMENTED / TESTED (unsigned) |
| Foundation Seal 5 | **NOT READY** |
| V2 M11 / Kernel | Progressing · **not sealed** |
| CRTG | Design track |
| M13–M22 | Deliberately not bulk-built |
| Other repos | Independent, contract-driven |

## Immediate target

**Prove the foundation — do not add another layer.**

Priority: Seal 5 evidence path → M11/kernel boundary freeze → CRTG specification freeze.
