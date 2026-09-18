# Authority Boundary Model (V1)

**Status:** DESIGNED → IMPLEMENTED → TESTED (not SEALED)  
**Date:** 18 September 2026  
**Contract id:** `authority_boundary_v0`  
**Pair:** Same invariant as V2 `docs/AUTHORITY_BOUNDARY_MODEL.md`

## Invariant

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
```

Information may cross a boundary without authority crossing that boundary.

| Layer | May do | Must not imply |
|-------|--------|----------------|
| Data | Carry information | Truth or authority |
| Evidence | Record tested/observed result | Universal truth; permission to act |
| Admission | Accept under contract | Authorization |
| Authorization | Scoped permission | Unrestricted authority |
| Action | Execute in scope | Authority beyond scope |

## Behaviour (v0)

- Undeclared authority fields → **REJECT** (not silent strip)
- ACTION without authorization → **HALT**
- ACTION outside declared scopes → **REJECT**

Implementation: `swi_core.authority`

## Non-claims

Does not seal M00–M10, Foundation Seal 5, CRTG, or factual truth.  
Does not rewrite historical module seals.

## Next

CI-VERIFIED on tip → optional wiring into Trainer/export path → audit → seal of this helper only.
