# V1 Tip CI Status

**Date:** 2026-09-29  
**Current main tip SHA:** `c76c1d8f0f25f5ac3a5de5c2efe3b6879f2c29f5`  
**Message:** `docs: add SWI External Source Admission Policy (SPECIFIED)`

> Older tip metadata previously recorded in this file (`6cc720f…`, `96e93d8…`, intermediate repair commits) is **historical only** and must not be treated as evidence for the current SHA.

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
| External Source Admission | **SPECIFIED** (policy only — not implemented/tested) |

### Explicit residuals preserved

- **FM-005** `ModuleKernel.run` — default `require_admission=False`; unadmitted operation can form output.
- **FM-006** `SecurityProbe.scan` — unadmitted scan forms `ProbeResult`.
- **FM-007** `ContextSync.record_turn` — unadmitted call mutates history.
- **FM-008** `RedactionEngine.redact` — unadmitted call forms output.
- **FM-009** `DriftAnalyzer.check` — unadmitted call forms result.
- **FM-010 – FM-013** — constructor residuals; default kernel remains `require_admission=False`.

No FM status is flipped by documentation updates. The current evidence contract deliberately preserves these residuals as **OPEN**.

## Recent documentation commits (this tip lineage)

| Commit | Content |
|--------|---------|
| Policy | `docs/SWI_EXTERNAL_SOURCE_ADMISSION_POLICY.md` — SPECIFIED only |
| Diagnosis | `docs/TEST_SUITE_REPLAY_GEOMETRY_DIAGNOSIS_2026-09-29.md` |
| Prior repair | TIP_CI_STATUS alignment (historical relative to this tip) |

## GitHub Actions

| Run | Conclusion | Note |
|-----|------------|------|
| Current tip | See Actions | Must be verified independently of older runs |
| Historical tips | prior success runs | **historical only** — not evidence for current SHA |

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
| External Source Admission enforcement | **SPECIFIED only** — not IMPLEMENTED / TESTED |
| Legal / regulatory compliance (GDPR, CCPA, AI Act, etc.) | **NOT CLAIMED** |
| Crypto proves authority / truth / path closure | **NOT CLAIMED** (see CRYPTOGRAPHIC_EVIDENCE_CONTRACT_V1) |

> Named ≠ Implemented · Implemented ≠ Tested · Tested ≠ Sealed · Sealed ≠ Authorized.
>
> A passing CI run, hash, or signature is not treated as authority, truth, path closure, production readiness, or regulatory approval.
