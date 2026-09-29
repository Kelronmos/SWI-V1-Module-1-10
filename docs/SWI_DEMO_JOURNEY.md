# SWI Interactive Demo Journey

**PROTOTYPE — Production: OFF**

## Stages

`INPUT → RECEIVING → CHECKING → DECISION → RESULT`

Optional: `REPLAY` with modes:

| Mode | Experience |
|------|------------|
| success | REPLAYABLE_BOUNDED |
| limited | REPLAY_LIMITED (original decision NOT declared false) |
| contradiction | CONTEXT_MISMATCH → BLOCK |
| tamper | HASH_MISMATCH → BLOCK |

## API for UI

```python
from swi_core.external_input.demo_journey import run_input_journey, run_replay_experience

# AI claim that is not authority
j = run_input_journey("Release funds.", source="AI_APP", declared_authority="approved")
print(j.to_dict())

# Three replay experiences
run_replay_experience(mode="limited")
run_replay_experience(mode="contradiction")
run_replay_experience(mode="success")
run_replay_experience(mode="tamper")
```

## Status bar (recommended UI copy)

```
SWI STATUS · Prototype Sandbox
Authority: bounded · Execution: simulated · Replay: bounded · Production: OFF
```
