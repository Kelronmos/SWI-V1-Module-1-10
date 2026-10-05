# V1 Tip CI Status

**Date:** 2026-10-05  
**Current main tip SHA:** `e51543bb41cb6c384a41c7fd486772496f6b2125`  
**Message:** `docs(status): weekly status 2026-W41 — honest snapshot, no FM flips`

> Older tip metadata in prior versions of this file is **historical only** and must not be treated as evidence for the current SHA.
>
> This alignment commit updates the recorded tip. The SHA above is the parent weekly-status commit. Re-read `git rev-parse main` after this file lands; do not treat this document's own commit as a new FM or CI result.

**Code tip used for last recorded interop verification run:** `87163df01f4f43f05e60956d11c9181356cbc233`  
**Observed (historical, local):** interop 21/21 PASS · full adversarial 204/204 PASS. Not re-run for this alignment. Not evidence that GitHub Actions is green on the current tip.

**Mutation evidence tip (docs only):** `3ea83e4d5382cc5a0e6f2e122a01ebbf31a855f2`  
mutmut package install unavailable (PyPI 502); in-repo pilot 5/5 killed; domain 10/10. Separate scores. Security Maze status unchanged (**NOT_READY**).

## Current formation-path inventory (canonical)

Source of truth: `docs/formation_path_inventory.json`

| Band | Status |
|------|--------|
| FM-001 – FM-004 | **TESTED** |
| FM-005 – FM-013 | **OPEN** |
| Universal Gate | **NOT_PROVEN** |
| Security Maze V1 | **NOT SEALED / NOT_READY** |
| Foundation Seal 5 | **NOT READY** |
| Legal / regulatory compliance | **NOT CLAIMED** |

### Explicit residuals preserved

- **FM-005** `ModuleKernel.run` — default `require_admission=False`; unadmitted operation can form output. `ModuleKernel.for_privileged()` exists for gated paths. Default was **not** flipped.
- **FM-006** `SecurityProbe.scan` — unadmitted scan forms `ProbeResult`.
- **FM-007** `ContextSync.record_turn` — unadmitted call mutates history.
- **FM-008** `RedactionEngine.redact` — unadmitted call forms output.
- **FM-009** `DriftAnalyzer.check` — unadmitted call forms result.
- **FM-010 – FM-013** — constructor residuals; default kernel remains `require_admission=False`.

No FM status is flipped by documentation, the privileged factory, or prototype slices. Residuals remain **OPEN**.

## Prototype / bounded slices (this tip lineage)

| Control | Status |
|---------|--------|
| External Source Admission | **IMPLEMENTED + TESTED (bounded)** · REPLAYABLE_BOUNDED |
| Claim slots + change control | **IMPLEMENTED + TESTED (bounded)** |
| External API/AI input sandbox | **PROTOTYPE / TESTED** |
| Demo journey orchestrator | **PROTOTYPE / TESTED** |
| Interoperability 14-stage template | **IMPLEMENTED + TESTED (PROTOTYPE)** |
| Interop mutation & replay suite | **TESTED (10/10)** on `87163df` · evidence under `reports/interoperability/` |
| FM-005 Priority-0/1 baseline | Caller map + privileged factory · residual **OPEN** |
| Consequence C4/C5 auto-BLOCK | **NOT fully enforced** (OPEN → V3) |
| Cross-node S9 pipe | **NOT_IMPLEMENTED** |

Bounded interop claim (only):

> Within the tested prototype scope, post-decision mutations of the tested classes do not silently reuse the original PASS.

Weekly snapshot: `docs/status/WEEKLY_STATUS_2026-W41.md`.

## GitHub Actions

| Run | Conclusion | Note |
|-----|------------|------|
| Current tip | See Actions | Must be verified independently of older runs |
| Historical tips | prior success runs | **historical only** — not evidence for current SHA |

## Required local verification before any seal claim

```text
pip install -r requirements.txt
PYTHONPATH=. python -m pytest -q
./scripts/verify.sh
```

Targeted:

```text
PYTHONPATH=. python -m pytest -q test/adversarial/
PYTHONPATH=. python -m pytest -q test/adversarial/test_interoperability_template.py test/adversarial/test_interoperability_mutation_replay.py
```

## Explicit non-claims

| Item | Status |
|------|--------|
| Foundation Seal 5 | NOT READY |
| Authority boundary | IMPLEMENTED / TESTED — **not sealed** |
| Bidirectional verified return path | **Not implemented in V1** |
| CRTG / production key governance | NOT IMPLEMENTED |
| Universal Gate | NOT_PROVEN |
| Security Maze sealed | NOT_READY |
| Production-wide replay | NOT_PROVEN (REPLAYABLE_BOUNDED only) |
| Production trust | **NOT CLAIMED** |
| Legal / regulatory compliance | **NOT CLAIMED** |
| Crypto proves authority / truth / path closure | **NOT CLAIMED** |

> Named ≠ Implemented · Implemented ≠ Tested · Tested ≠ Sealed · Sealed ≠ Authorized.
>
> A passing CI run, hash, or signature is not treated as authority, truth, path closure, production readiness, or regulatory approval.
