# Universal-Gate Construction Gate (mandatory)

**Universal Gate status:** **NOT PROVEN** (direct module APIs still default-ungated)  
**Production entrypoints Trainer / export / sign:** **WIRED** (require AdmissionDecision)  
**Wiring tip:** see main after admission gate commits (a408609+)

---

## Immediate status

| Item | State |
|------|--------|
| AdmissionDecision | IMPLEMENTED / TESTED |
| ModuleKernel strict mode | IMPLEMENTED / TESTED |
| ModuleKernel default | still `require_admission=False` |
| Trainer.process admission | **WIRED** — reject before turn/modules/M07/M09 |
| export_foundation_evidence admission | **WIRED** |
| sign_foundation_evidence admission | **WIRED** |
| Direct M02/M03/M05/M06/M07/M09 APIs | **NOT WIRED** (residual surface) |
| Architectural CI AST guard (all paths) | PARTIAL |
| Universal Gate | **NOT PROVEN** |
| Module 10 | PROPOSED / NOT ADMITTED |
| Foundation Seal 5 | NOT READY |

---

## Wired contract

```text
Trainer.process(*, admission)
  → is_valid_for(module="00", commit=expected_commit)
  → else AdmissionRequiredError BEFORE _turn_counter++

export_foundation_evidence(*, admission)
  → is_valid_for(module="foundation_export", ...)

sign_foundation_evidence(*, admission)
  → is_valid_for(module="foundation_sign", ...)
```

Test admissions use explicit `admission_artifact` + `grant_execution=True` via
`test/helpers_admission.py` (**test_only** — not production authority).

---

## Remaining residual bypasses

- `SecurityProbe.scan` / `RedactionEngine.redact` / … without going through Trainer
- `ModuleKernel(require_admission=False)` default inside modules
- No full AST CI fail on every new formation symbol

Until residual surfaces are closed or marked internal-only with enforced policy:

```text
Universal Gate = NOT PROVEN
```

**Do not claim what the code cannot demonstrate.**
