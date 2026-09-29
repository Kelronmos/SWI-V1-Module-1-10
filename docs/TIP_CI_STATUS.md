# V1 Tip CI Status

**Date:** 2026-09-29  
**Current main tip SHA:** `96e93d8cc3dfda7a2e5220ce4bbe020dda61c22b`  
**Message:** `Merge pull request #4 from Kelronmos/architecture/proposed-fm-023-040`

> Previous tip metadata in this file (`6cc720f5666395696ad425a3d8bfa8f10209c536`) is **historical only** and must not be treated as evidence for the current SHA.

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

No FM status is flipped by this documentation repair. The current evidence contract deliberately preserves these residuals as **OPEN**.

## GitHub Actions

| Run | Conclusion | Note |
|-----|------------|------|
| Current tip `96e93d8…` | See Actions | Must be verified independently of older runs |
| Historical tip `f1f6e266…` | success — run 35342332253 | **historical only** — not evidence for current SHA |
| Historical tip `6cc720f…` | prior admission-fix tip | **historical only** |

## Required local verification before any seal claim

```text
pip install -r requirements.txt
python -m pytest -q
./scripts/verify.sh
```

Target: full suite green (including adversarial architecture-boundary attacks).

## Explicit non-claims

| Item | Status |
|------|--------|
| Foundation Seal 5 | NOT READY |
| Authority boundary | IMPLEMENTED / TESTED — **not sealed** |
| Bidirectional verified return path | **Not implemented in V1** |
| CRTG / production key governance | NOT IMPLEMENTED |
| Universal Gate | NOT_PROVEN until every formation path is independently covered |
| Security Maze sealed | NOT_READY |
| Legal / regulatory compliance (GDPR, CCPA, AI Act, etc.) | **NOT CLAIMED** |
| Crypto proves authority / truth / path closure | **NOT CLAIMED** (see CRYPTOGRAPHIC_EVIDENCE_CONTRACT_V1) |

> Named ≠ Implemented · Implemented ≠ Tested · Tested ≠ Sealed · Sealed ≠ Authorized.
>
> A passing CI run, hash, or signature is not treated as authority, truth, path closure, production readiness, or regulatory approval.
