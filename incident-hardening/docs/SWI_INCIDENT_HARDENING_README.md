# SWI Frontier-AI Incident Hardening

**Objective:** Replay documented 2026 evaluation failure patterns safely and produce
independently verifiable DENY / BLOCK / HALT with `execution_occurred = false`.

**Core rule:** Model capability, credentials, reachability, tools, or model claims
never become authority.

## Track separation

| Track | Purpose |
|-------|--------|
| formal/v47-discipline-patch | Status Engine + TLA+ model safety |
| incident-hardening (this tree) | Enforcement boundary + incident replay |

Formal PROVEN_ON_MODEL ≠ incident suite PASS ≠ SEALED.

## Definition of fixed (not README)

```
condition → SWI detects → DENY/BLOCK/HALT
  → execution gate receives decision
  → actual resource operation rejected
  → tamper-evident evidence
  → replay reproduces result
```

## Residual

`SWI-ENFORCEMENT-GAP = OPEN` until INC-010 proves zero executions after DENY
at a real enforcement adapter.
