# Canonicalization Specification (Lane B)

**Contract id:** `canonicalization_v0`  
**Status:** IMPLEMENTED → TESTED (not SEALED)  
**Date:** 18 September 2026  

## Rule

```text
same logical covered fields
    → same canonical JSON string
    → same UTF-8 bytes
    → same SHA-256 hex digest
```

## Algorithm

```text
json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)
encode UTF-8
SHA-256 → hex digest
```

Implementation: `swi_core.canonical`

## Foundation integrity material

Covered: `payload`, `foundation_version`, `evidence_schema_version`, `evidence_id`, `source_reference`  

**Excluded:** `created_at`

## Non-claims

- Does not establish factual truth  
- Does not authenticate the sender  
- Does not authorize action  
- `default=str` is documented for non-JSON types; prefer JSON-native values  

## Tests

- `test/test_canonicalization_contract.py`  
- `test/test_canonicalization_integrity.py`  
- `test/test_canonicalization_adversarial.py`  
