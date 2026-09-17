# V1 Contract Test Layer (V4.7 alignment)

## Separation

| Layer | Proves |
|-------|--------|
| pytest + schema | CLAIM → CONTRACT (schema behaviour) |
| Existing test harness | Implementation behaviour where present |
| Independent V4.7 verifier | TEST/CI → EVIDENCE → SEAL → AUDIT |

## Non-claims

- Enum values restrict mode *names*; determinism requires behavioural tests.
- Schema pass ≠ sealed ≠ factual truth.
- Tests do not invent `validate_module_input`; they validate the schema contract.

## Dependency

`jsonschema>=4` required for these tests (add to requirements when applying).

## Gate

M12 remains blocked until M11 survives the full independent verifier chain.
