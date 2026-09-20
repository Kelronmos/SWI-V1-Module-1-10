# TLA+ Workflow Verification Track

## Purpose

Abstract safety properties for SWI admission-gated workflows.

## Current Properties

| ID | Property | Status |
|----|----------|--------|
| SWI-WORKFLOW-001 | `formed => admitted` | SPECIFIED |
| SWI-WORKFLOW-002 | `~admitted => auditWrites = 0` | SPECIFIED |
| SWI-WORKFLOW-003 | `Rejected => ~formed` | SPECIFIED |

## How to check (local)

Requires TLA+ Toolbox or `tlc2` on the PATH.

```bash
tlcs verification/tla/specs/swi_workflow_001.tla -config verification/tla/models/swi_workflow_001.cfg
```

## Status vocabulary for this track

- `PROVEN_ON_MODEL` — TLC found no violation of the invariant under the stated constants
- `FALSIFIED` — counterexample produced (used for the deliberate ungated model)
- `BOUND_ONLY` — result depends on a finite bound (e.g. MaxTurns)
- `NOT_PROVEN` — not yet checked

## Hard non-claims

Results on this track are **never** automatically:

- production-code proof
- FM-005 closure
- Universal Gate
- mathematical seal
- authorization or execution permission

See `docs/ARTIFACT_NAMING_AND_DIRECTORY_CONVENTIONS.md`.
