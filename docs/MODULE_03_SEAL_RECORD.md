# MODULE 03 — CONTEXT SYNC — SEAL RECORD

| Field | Value |
|-------|--------|
| **Status** | **KERNEL-ENFORCED** · local suite PASS · **CI pending** independent witness |
| **Implementation** | `swi_core/module03_context_sync.py` |
| **Trainer** | `halted_by_module_03_kernel` on contract failure |
| **Tests** | `test/test_context_sync_kernel.py` (10) + existing functional tests |
| **Preserved** | `stale = gap > threshold`; first-turn gap 0; OOO flags; append on success |
| **Not halt** | `stale=True` / `out_of_order=True` alone |
| **CI** | UNVERIFIED until Actions green on this commit chain |

## Seal language

> Module 03 has a kernel-enforced type/shape contract around temporal gap reporting. Stale and out-of-order remain flags. Content truth and clock honesty are not claimed.

Next: confirm CI → mark CI VERIFIED → then Module 06 is eligible under Part 3 order.
