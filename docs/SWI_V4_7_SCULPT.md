# SWI V4.7 Sculpt Guide

**Purpose:** Keep documentation, models, and claims aligned with the actual evidence boundary.

## Rules

1. Prefer downgrade over inflation.
2. Keep formal models small and explicit.
3. Separate safety from liveness until fairness is stated.
4. Record full SHA in machine evidence.
5. Never let a filename carry a status claim that the metadata does not support.
6. Treat `PROVEN_ON_MODEL` as the ceiling for pure TLA+ results until a refinement argument exists.
7. Keep FM-005 OPEN until the repository-specific closure criteria are met.
8. Keep mathematical thresholds SOURCE-AMBIGUOUS until interval semantics are resolved.

## First acceptance criteria for the V4.7 formal track

- [ ] SWIWorkflowV47.tla present
- [ ] SWIWorkflowV47.cfg present
- [ ] W1–W3 property docs present
- [ ] Evidence claim templates present
- [ ] Non-claims recorded
- [ ] Local TLC run recorded against a full SHA
- [ ] No premature SEALED or Universal Gate language
