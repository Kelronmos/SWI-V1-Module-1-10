# G1 → G2 ↓ G3 Status

| Gate | Deliverable | Status |
|------|-------------|--------|
| G1 | Formation registry + CI check | **INVENTORY TESTED** (Gate NOT PROVEN) |
| G2 | Admission-required contract (formal track) | **CONTRACT TESTED**; main `require_admission=False` residual OPEN |
| G3 | Synthetic execution adapter | **SYNTHETIC TESTED**; real adapters NOT IMPLEMENTED |

## Residuals (must stay open)

- Universal Gate = NOT_PROVEN
- FM-005 = OPEN
- SWI-ENFORCEMENT-GAP = OPEN
- T10 = NOT_PROVEN

## Run

```bash
node scripts/check_formation_registry.mjs
node src/verification/admission_contract.test.mjs
node src/verification/execution_adapter.test.mjs
```
