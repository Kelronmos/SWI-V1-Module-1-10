# V1 Tip CI Status

**Date:** 2026-09-29  
**Current main tip SHA:** `73a4eb1c958f191dd9c00030b47f6efb9a6e0799`  
**Message:** `docs(interoperability): verification evidence from tip 87163df — 21/21 + 204 adversarial pass`

> Older tip metadata in prior versions of this file is **historical only** and must not be treated as evidence for the current SHA.

**Code tip used for interop verification run:** `87163df01f4f43f05e60956d11c9181356cbc233`  
**Observed:** interop 21/21 PASS · full adversarial 204/204 PASS (local; re-check CI on this tip).

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

- **FM-005** `ModuleKernel.run` — default `require_admission=False`; unadmitted operation can form output.
- **FM-006** `SecurityProbe.scan` — unadmitted scan forms `ProbeResult`.
- **FM-007** `ContextSync.record_turn` — unadmitted call mutates history.
- **FM-008** `RedactionEngine.redact` — unadmitted call forms output.
- **FM-009** `DriftAnalyzer.check` — unadmitted call forms result.
- **FM-010 – FM-013** — constructor residuals; default kernel remains `require_admission=False`.

No FM status is flipped by documentation or prototype slices. Residuals remain **OPEN**.

## Prototype / bounded slices (this tip lineage)

| Control | Status |
|---------|--------|
| External Source Admission | **IMPLEMENTED + TESTED (bounded)** · REPLAYABLE_BOUNDED |
| Claim slots + change control | **IMPLEMENTED + TESTED (bounded)** |
| External API/AI input sandbox | **PROTOTYPE / TESTED** |
| Demo journey orchestrator | **PROTOTYPE / TESTED** |
| Interoperability 14-stage template | **IMPLEMENTED + TESTED (PROTOTYPE)** |
| Interop mutation & replay suite | **TESTED (10/10)** · evidence under `reports/interoperability/` |
| Consequence C4/C5 auto-BLOCK | **NOT fully enforced** (OPEN → V3) |
| Cross-node S9 pipe | **NOT_IMPLEMENTED** |

Bounded interop claim (only):

> Within the tested prototype scope, post-decision mutations of the tested classes do not silently reuse the original PASS.

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
| Production trust | **NOT CLAIMED** |
| Legal / regulatory compliance | **NOT CLAIMED** |
| Crypto proves authority / truth / path closure | **NOT CLAIMED** |

> Named ≠ Implemented · Implemented ≠ Tested · Tested ≠ Sealed · Sealed ≠ Authorized.
>
> A passing CI run, hash, or signature is not treated as authority, truth, path closure, production readiness, or regulatory approval.
