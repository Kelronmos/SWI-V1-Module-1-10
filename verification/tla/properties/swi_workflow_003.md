# SWI-WORKFLOW-003

**Property ID:** SWI-WORKFLOW-003  
**Name:** Rejected State Cannot Form  
**Formal:** `(phase = "Rejected") => ~formed`  
**Class:** Safety invariant  
**Model:** SWIWorkflow001 (gated)  
**Method:** TLA+ / TLC  
**Status:** SPECIFIED (awaiting first TLC run)

## Natural-language meaning

A rejected phase never carries a formed state.

## Expected result

`PROVEN_ON_MODEL`

## Non-claims

Same as SWI-WORKFLOW-001. Model-level only.
