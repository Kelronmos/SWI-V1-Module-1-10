# SWI V4.7 Patch Plan

## Objective

Bring the supplied SWI archive toward the same evidence discipline used by the SWI V1 formal track without pretending that a documentation/model patch closes runtime gaps.

## Safe application order

1. Preserve the original repository/commit.
2. Apply `docs/SWI_V4_7_DISCIPLINE.md`.
3. Apply `docs/SWI_V4_7_SCULPT.md`.
4. Apply `docs/SWI_V4_7_MODULE_MAP.md`.
5. Add the formal model under `verification/tla/v47/`.
6. Add evidence templates under `evidence/swi-v47/`.
7. Add `scripts/swi-v47-check.mjs`.
8. Add the CI workflow only after local checks are reviewed.
9. Reconcile existing claims in `README.md`, `TRUTH_KERNEL.md`, `docs/SWI_SAFETY_THEOREM.md`, and `docs/SECURITY_STATUS.md`.
10. Run the check and record the result against the actual commit SHA.
11. Do not change a component to `SEALED` merely because this patch exists.

## Intentionally not performed

- No frozen V1 implementation rewrite
- No automatic promotion of TESTED to SEALED
- No Universal Gate claim
- No mathematical threshold resolution
- No FM-005 closure
