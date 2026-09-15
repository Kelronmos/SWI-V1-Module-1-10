# V1 — Cross-Repository Trust Integration

**Repository:** Kelronmos/SWI-V1-Module-1-10  
**Canonical spec:** `docs/CROSS_REPOSITORY_TRUST_SPECIFICATION.md`  
**Status:** **PROPOSED / DESIGN PENDING**

## Role of V1

V1 owns Foundation Seal 5 work (M00–10).  
**CRTG is not injected into M02 / M03 / M05 / M06** at this stage.

Cross-repo trust is an **additional ingress boundary** for material leaving V1 or entering from peers — not a replacement for:

- kernel contracts on sealed modules  
- M07/M09 integrity paths  
- Trainer halt semantics  
- Foundation Evidence Contract (after Seal 5)

## Planned integration point (future)

```text
V1 pipeline result / evidence export
        → signed TaskEnvelope (DESIGN PENDING)
        → peer CRTG / V2 CRTG
        → M11 (V2)
```

## Repository fields (to fill when implementing)

| Field | Value |
|-------|--------|
| Repository identity | `Kelronmos/SWI-V1-Module-1-10` |
| Certificate profile | DESIGN PENDING |
| Key ID / version | DESIGN PENDING |
| Trust policy | DESIGN PENDING |
| Envelope version | DESIGN PENDING |
| Private keys in repo | **Forbidden** |

## Claim discipline

Do **not** state “certificates implemented” or “cross-repo secure” in README until CRTG is code + tests + CI.
