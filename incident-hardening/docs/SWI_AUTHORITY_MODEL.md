# SWI Authority Model (Incident Hardening)

## Separated concepts (must not collapse)

| Concept | Meaning | Does NOT mean |
|---------|---------|----------------|
| OBSERVATION | Measured fact about environment/runtime | Authority |
| EVALUATION | PASS / FAIL / UNKNOWN on a condition | APPROVED |
| DECISION | Policy outcome (DENY / APPROVE candidate) | Execution |
| ADMISSION | Scoped, hashed, time-bounded grant | Unlimited execution |
| AUTHORIZATION | Principal + target + operation + env + scope | Credential possession |
| EXECUTION | Actual resource operation | Prior APPROVED alone |
| EVIDENCE | Tamper-evident record | Truth or seal |

## Deny-by-default

UNKNOWN → DENY  
MISSING → DENY  
INVALID → DENY  
NULL scope/target/policy → DENY  

## Invariants (incident track)

- INC-01 UNKNOWN ≠ APPROVED
- INC-02 PASS ≠ AUTHORIZATION
- INC-03 MODEL_CLAIM ≠ AUTHORIZATION
- INC-04 CREDENTIAL_POSSESSION ≠ AUTHORIZATION
- INC-05 RESOURCE_REACHABILITY ≠ AUTHORIZATION
- INC-06 SCOPE_CHANGE invalidates admission
- INC-07 BOUNDARY_CHANGE invalidates admission
- INC-08 DENY must reach enforcement point
- INC-09 Side channel ≠ authority
- INC-10 Execution after DENY ⇒ FAIL

## Weight / role / version / module

Descriptive only. Never acquire authority by ordering or label.
