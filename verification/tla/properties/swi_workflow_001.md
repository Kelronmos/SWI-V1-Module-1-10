# SWI-WORKFLOW-001

**Property ID:** SWI-WORKFLOW-001  
**Name:** Formation Requires Admission  
**Formal:** `formed => admitted`  
**Class:** Safety invariant  
**Model:** SWIWorkflow001 (gated)  
**Method:** TLA+ / TLC  
**Status:** SPECIFIED (awaiting first TLC run)

## Natural-language meaning

In the abstract model, every state in which formation has occurred must also have admission.

## Assumptions

- Single formation action (`Form`) is enabled only when `phase = "Admitted"` and `admitted = TRUE`.
- No ungated formation actions are present in this model.

## Expected result

`PROVEN_ON_MODEL` when TLC finds no violation of `SafeFormation` under the given constants.

## Non-claims

- Does not establish that every production formation path implements this model.
- Does not close FM-005.
- Does not establish Universal Gate.
- Does not constitute a mathematical or production seal.
