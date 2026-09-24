# SWI-WORKFLOW-002

**Property ID:** SWI-WORKFLOW-002  
**Name:** No Durable Side-Effect Before Admission  
**Formal:** `~admitted => auditWrites = 0`  
**Class:** Safety invariant  
**Model:** SWIWorkflowV47 (gated)  
**Method:** TLA+ / TLC  
**Status:** SPECIFIED

## Non-claims

Model-level only. Does not prove production side-effect behavior.
