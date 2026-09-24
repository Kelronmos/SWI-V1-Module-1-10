# SWI-WORKFLOW-002

**Property ID:** SWI-WORKFLOW-002  
**Name:** No Durable Side-Effect Before Admission  
**Formal:** `~admitted => auditWrites = 0`  
**Class:** Safety invariant  
**Model:** SWIWorkflow001 (gated)  
**Method:** TLA+ / TLC  
**Status:** SPECIFIED (awaiting first TLC run)

## Natural-language meaning

Rejection (or any state before admission) must not produce the relevant durable side effect counted by `auditWrites`.

## Assumptions

- `auditWrites` is incremented only inside the gated `Form` action.

## Expected result

`PROVEN_ON_MODEL`

## Non-claims

Same as SWI-WORKFLOW-001. Model-level only.
