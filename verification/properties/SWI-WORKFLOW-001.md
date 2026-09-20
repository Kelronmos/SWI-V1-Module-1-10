# SWI-WORKFLOW-001

**Property ID:** SWI-WORKFLOW-001  
**Name:** Formation Requires Admission  
**Formal:** `formed => admitted`  
**Class:** Safety invariant  
**Model:** SWIWorkflowV47 (gated)  
**Method:** TLA+ / TLC  
**Status:** SPECIFIED

## Natural-language meaning

In the abstract V4.7 model, every state in which formation has occurred must also have admission.

## Non-claims

- Does not establish that every production formation path implements this model.
- Does not close FM-005.
- Does not establish Universal Gate.
- Does not constitute a mathematical or production seal.
