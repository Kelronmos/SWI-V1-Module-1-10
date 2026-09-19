# SWI Security Maze V1 — Remaining Construction, Reopening & Seal Roadmap

**Repository:** SWI-V1-Module-1-10  
**Path-closure baseline:** `0e15fc96791cc97ab712dcdc1b76aab6dc66ee7e`  
**Attack baseline (hold point):** `c8a7e120b27311e0597aaa0d4b76bfc8bd9b3ef8`  

This document **freezes** unfinished work and assigns **reopening conditions**.  
It does **not** seal Security Maze V1.

---

## Seal discipline (non-negotiable)

```text
DOCUMENTED ≠ IMPLEMENTED
IMPLEMENTED ≠ TESTED
TESTED ≠ REPRODUCED
REPRODUCED ≠ COMPLETE
HASHED ≠ TRUE
SIGNED ≠ TRUE
PASS ≠ UNIVERSAL
OPEN ≠ FAILED
CONSTRUCTION ≠ SEALED
```

---

## Current hold point (frozen)

| Item | Status |
|------|--------|
| Security Maze V1 | **PARTIAL / TESTED** |
| FM-001 … FM-004 | **TESTED / PROTECTED** |
| FM-005 … FM-009 | **OPEN / ATTACKED** |
| FM-010 … FM-013 | **COMPATIBILITY** |
| Universal Gate | **NOT PROVEN** |
| Security Maze Seal | **NOT READY** |
| Foundation Seal 5 | **NOT READY** |

**Qualification:** `unknown_paths == 0` means no inventory row is classified UNKNOWN. It does **not** prove the repository has no undiscovered formation path.

---

## Final construction contract

```text
OPEN → ASSIGN → IMPLEMENT → ATTACK → CONTAIN → REGRESSION
    → EVIDENCE → REPLAY → CI → INDEPENDENT REVIEW → BOUNDED CLOSURE
```

- A row moves from OPEN only when **required evidence** exists.  
- Status must not change by documentation alone.  
- A test pass is not completeness.  
- Hash = integrity of the artifact, not factual truth or legal authority.

---

## Phase map (750-step campaign — condensed assignment)

| Phase | Steps | Focus | Gate before next |
|-------|-------|--------|------------------|
| 1 Freeze & baseline | 1–25 | Record SHA, suites, freeze NOT PROVEN | Work log exists |
| 2 Repository inventory | 26–50 | Enumerate kernels, APIs, factories, restore | Discrepancy log |
| 3 FM inventory | 51–75 | Validate JSON / forbidden combos | Inventory tests green |
| 4 Discovery completeness | 76–100 | Scanner vs inventory; no false completeness claim | Limitations documented |
| 5 Evidence model | 101–125 | Schema; NOT_RUN ≠ PASS | Schema tested |
| 6 Crypto evidence | 126–150 | Canonical hash reuse; not CRTG | Determinism tested |
| 7 SM-V1-004 | 151–175 | Admission authenticity | Attack + regression |
| 8 SM-V1-005 | 176–200 | Forged AdmittedInput (V2) | Cross-repo evidence |
| 9 SM-V1-006 / FM-005 | 201–225 | Default ModuleKernel | **NEXT development** |
| 10 SM-V1-007 / FM-006 | 226–250 | `scan()` | After FM-005 decision |
| 11 SM-V1-008 / FM-007 | 251–275 | `record_turn()` | After FM-006 |
| 12 SM-V1-009 / FM-008 | 276–300 | `redact()` | After FM-007 |
| 13 SM-V1-010 / FM-009 | 301–325 | `check()` | After FM-008 |
| 14 Constructors FM-010…013 | 326–350 | Compatibility classification | Explicit bounds |
| 15 Sandbox hardening | 351–375 | Escape routes | No universal claim |
| 16 Replay defense | 376–400 | Mutation / stale / wrong commit | Regression |
| 17 Retry invariants | 401–425 | SM-V1-003 / 012 | Authority unchanged |
| 18 Crash/recovery | 426–450 | SM-V1-013 | Incomplete ≠ admitted |
| 19 Three-run validation | 451–475 | Structure / boundary / evidence | NOT_RUN preserved |
| 20 V1↔V2 boundary | 476–500 | Cross-repo | M11 seal unchanged unless evidence |
| 21 Temporary bridges | 501–525 | Explicit temporary | No maze bypass |
| 22 Static regression | 526–550 | Scan vs inventory | New path fails CI |
| 23 Adversarial mutation | 551–575 | Field mutation suite | Contained |
| 24 Evidence reporting | 576–600 | JSON + manifest hash | Replayable |
| 25 CI | 601–625 | Maze + inventory + FM attacks | Per-SHA CI |
| 26 Clean checkout | 626–650 | Independent reproduce | Match tip |
| 27 Second adversarial pass | 651–675 | Reattack all FM | No regression |
| 28 Seal readiness review | 676–700 | Review only — **not** a seal | OPEN ⇒ no seal |
| 29 Seal decision | 701–725 | Bounded claim or NOT READY | Explicit non-claims |
| 30 Reopening / future | 726–750 | Assign conditions below | Evidence-bound only |

**Completing all 750 steps does not imply a seal.** They define evidence required for a *future* seal decision.

---

## OPEN path reopening conditions (must all be met to change status)

### FM-005 — `ModuleKernel.run` default (`require_admission=False`)

| Field | Value |
|-------|--------|
| **Blocked reason** | Compatibility default allows unadmitted operation; production-reachable via residual modules |
| **Reopen when** | (A) production callers maze/admission-bound **or** (B) documented non-privileged boundary with architecture review |
| **Required evidence** | Attack regression; positive strict-kernel test; FM row update; path-closure tests; clean-checkout; CI on that SHA |
| **Construction module** | Kernel / Security Maze |
| **Dependency** | Caller inventory complete |
| **Next development** | **Assigned first** |

### FM-006 — `SecurityProbe.scan`

| Field | Value |
|-------|--------|
| **Blocked reason** | Unadmitted scan forms `ProbeResult`; `maze_protected=false` |
| **Reopen when** | Maze-routed if privileged **or** bounded non-privileged classification with evidence |
| **Required evidence** | Direct-call attack; caller list; regression; inventory + path-closure green |
| **Dependency** | FM-005 decision (shared kernel default) preferred first |

### FM-007 — `ContextSync.record_turn`

| Field | Value |
|-------|--------|
| **Blocked reason** | Unadmitted mutation of turn history |
| **Reopen when** | Protection implemented **or** explicit non-privileged bound proven |
| **Required evidence** | Mutation attack; retry/sandbox tests; inventory update |

### FM-008 — `RedactionEngine.redact`

| Field | Value |
|-------|--------|
| **Blocked reason** | Unadmitted redaction output |
| **Reopen when** | Same as FM-006 pattern for this module |
| **Required evidence** | Direct attack; regression; inventory |

### FM-009 — `DriftAnalyzer.check`

| Field | Value |
|-------|--------|
| **Blocked reason** | Unadmitted check result |
| **Reopen when** | Same as FM-006 pattern for this module |
| **Required evidence** | Direct attack; regression; inventory |

### FM-010 … FM-013 — module constructors

| Field | Value |
|-------|--------|
| **Blocked reason** | Construct `ModuleKernel` with default False |
| **Reopen when** | Classification confirmed (compatibility / construction-only) **and** privileged use attempts contained |
| **Required evidence** | Constructor attack suite; no silent privilege |

### SM-V1-005 (V2 AdmittedInput forgery)

| Field | Value |
|-------|--------|
| **Status** | **NOT_RUN** in V1-only campaign |
| **Reopen when** | Cross-repo tests against V2 M11 boundary |
| **Required evidence** | Forged input rejected; M11 seal limitations preserved |

### SM-V1-013 (crash/recovery)

| Field | Value |
|-------|--------|
| **Status** | **NOT_RUN** / construction |
| **Reopen when** | Controlled interruption tests CI-safe |
| **Required evidence** | Incomplete validation ≠ admitted |

---

## Seal readiness (Phase 28–29) — hard stops

Do **not** set Security Maze Seal or Universal Gate = PROVEN if any of:

- Any privileged OPEN row remains without reviewed exception  
- `privileged ∧ maze_required ∧ ¬maze_protected ∧ status=TESTED`  
- Paperwork-only status change  
- Discovery completeness overclaimed  
- Privileged escape demonstrated  
- CI/clean-checkout missing for candidate SHA  

If residuals remain: **NOT READY**, assign construction modules, keep inventory honest.

---

## NEXT DEVELOPMENT

```text
NEXT = FM-005
```

One path at a time: implement boundary or classify → attack → regression → update FM record → path-closure tests → CI → then FM-006.

---

## Explicit non-claims

- This roadmap is **not** a seal.  
- Targeted test counts are **not** universal proof.  
- Attachments / monorepo / S9 / CEK product claims remain outside this freeze unless separately proven.  
- Foundation Seal 5 remains **NOT READY** under its own gates.

---

*End of freeze. Status changes require evidence bound to a specific commit.*
