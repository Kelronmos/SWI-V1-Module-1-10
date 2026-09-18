# Authority Boundary Model (V1)

**Status:** DESIGNED → IMPLEMENTED → TESTED → **CI-VERIFIED pending green Actions on this tip**  
**Date:** 18 September 2026  
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
| Authority SHA | `0ee6d349cdd5e023a44954036720380cf7d36d52` |
| Prior CI run | `35325880471` — failure (claim-language; 3.10/3.11 green) |
| Workflow | CI (`ci.yml`) |
| Conclusion | **CI-VERIFIED** only after Actions success on **this** restore tip |

```text
TESTED ≠ CI-VERIFIED ≠ AUDITED ≠ SEALED
```

Lane A is **frozen**. Next: **Lane B — canonicalization** (same meaning → same canonical form → same digest). Canonicalization must not become an authority mechanism.

## Non-claims

Does not seal M00–M10, Foundation Seal 5, CRTG, or factual truth.  
Does not authorize M12 or unrestricted action.
