# Authority Boundary Model (V1)

**Status:** DESIGNED → IMPLEMENTED → TESTED → **CI-VERIFIED on tip** · **NOT SEALED**  
**Date:** 19 September 2026  
**Contract id:** `authority_boundary_v0`  
**Pair:** V2 `docs/AUTHORITY_BOUNDARY_MODEL.md` + `swi_v2.kernel.authority`

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

## Evidence gate

| Field | Value |
|-------|--------|
| Repository | Kelronmos/SWI-V1-Module-1-10 |
| Tip (maintenance) | `f1f6e266d4ac49698369752e4653b9c11e9a2d73` |
| Tip CI run | [35342332253](https://github.com/Kelronmos/SWI-V1-Module-1-10/actions/runs/35342332253) — **success** |
| Detail | `docs/TIP_CI_STATUS.md` |
| Workflow | CI (`ci.yml`) |

```text
TESTED ≠ CI-VERIFIED ≠ AUDITED ≠ SEALED
```

Authority is **not** a production trust seal. Canonicalization must not become an authority mechanism. Bidirectional return path is **not** part of V1 (see V2 pre-R design only).

## Non-claims

Does not seal M00–M10, Foundation Seal 5, CRTG, or factual truth.  
Does not authorize M12 or unrestricted action.  
Does not implement a verified return / response gate.
