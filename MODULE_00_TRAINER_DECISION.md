# MODULE 00: THE TRAINER — ARCHITECTURAL DECISION RECORD

**Decision:** Trainer as orchestration scaffold, not security boundary  
**Authority:** Keletso Ronald Mosidila, SWI Architecture  
**Date:** September 15, 2026  
**Status:** Proposed  

---

## 1. CONTEXT

The SWI foundation (Modules 00–10) requires a master orchestrator that:
- Initializes all modules in a deterministic order
- Manages configuration loading
- Captures and propagates halt signals from security kernels
- Provides logging and audit trails

**Question:** Should the Trainer itself be a security boundary, or a passive orchestrator?

---

## 2. DECISION

**The Trainer is a passive orchestrator, not a security boundary.**

### Rationale

1. **Single Responsibility**
   - Trainer's job: coordinate module startup and halt propagation
   - Security validation: delegated to M02 (Security Probe), M03 (Context Sync), M05 (Redaction), etc.
   - Mixing responsibilities = harder to test, harder to audit

2. **Fail-Closed Design**
   - Trainer cannot know what is "correct" for each module to validate
   - Instead: Trainer **trusts but verifies** downstream kernels
   - If M02/M05/etc. halt → Trainer halts immediately; no override

3. **Auditability**
   - A passive orchestrator is easier to inspect
   - All state changes come from modules, not from Trainer logic
   - Code review surface area is smaller

4. **Testability**
   - Trainer can be tested with mock modules
   - No need to simulate 10 security domains simultaneously
   - Each module's kernel is tested independently

---

## 3. ALTERNATIVES CONSIDERED

### Alternative A: Trainer as Active Validator
**"Trainer should inspect all module outputs before allowing them to proceed."**

**Pros:**
- Central policy enforcement point
- Single place to log all decisions

**Cons:**
- ❌ Trainer would need to understand M02, M03, M05, M06… validation logic
- ❌ Would require Trainer to be kernel-wrapped itself
- ❌ Circular dependency: M00 validates M02, but M00 depends on M02?
- ❌ Each module change requires Trainer change
- **Rejected:** Violates separation of concerns

### Alternative B: Trainer as Message Bus
**"Trainer should be a publish-subscribe event broker."**

**Pros:**
- Loosely coupled modules
- Asynchronous execution possible

**Cons:**
- ❌ Adds complexity (queues, threading, ordering)
- ❌ Fails the "fail-closed" principle (async = harder to reason about halts)
- ❌ Audit trail becomes non-deterministic
- **Rejected:** Over-engineered for current scope (Modules 00–10)

### Alternative C: Trainer as Distributed Coordinator
**"Trainer should spawn parallel module execution."**

**Pros:**
- Faster initialization

**Cons:**
- ❌ Race conditions in halt propagation
- ❌ Shared state management becomes complex
- ❌ Testing becomes exponentially harder
- ❌ "Fail-closed" is very hard to guarantee with parallelism
- **Rejected:** Premature optimization; Modules 11–46 will need this later, design for then

---

## 4. CHOSEN DESIGN

**Trainer as Sequential Orchestrator + Halt Receptor**

```
┌─ Trainer (M00) ─────────────┐
│                              │
│  1. Load config              │
│  2. Instantiate M01–M10      │
│  3. Call M02.run() ──────┐   │
│                          │   │
│                    (halt signal)
│                          │   │
│                          ▼   │
│                    M02 Kernel ─── VIOLATION
│                          │       │
│                          └─────→ trainer.halt()
│  4. STOP ◄──────────────────────┘
│  5. Log: "M02 kernel halt"
│  6. Raise HaltException
│
└──────────────────────────────┘
```

**Key properties:**
1. Deterministic ordering (sequential = easier to reason about)
2. Fail-closed (first halt stops everything)
3. Clear audit trail (all state changes logged in order)
4. Testable (mock modules for unit tests)

---

## 5. IMPLEMENTATION

**File:** `swi_core/module00_trainer.py`

```python
class Trainer:
    """Master orchestrator for SWI foundation."""

    def __init__(self, config_path: str):
        self.config = load_config(config_path)
        self.modules = {}
        self.halt_queue = queue.Queue()
        self.logger = setup_logger("trainer")

    def run(self):
        """Execute modules 01–10 in sequence; halt on kernel signal."""
        try:
            self._initialize_modules()
            for module_id in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                self.logger.info(f"Running Module {module_id}")
                module = self.modules[module_id]
                result = module.run()  # ← Kernel halt caught here
                
                # Check if any downstream halt occurred
                if not self.halt_queue.empty():
                    halt = self.halt_queue.get()
                    self.logger.error(f"HALT: {halt.reason}")
                    raise HaltException(halt)
        except HaltException as e:
            self.logger.critical(f"SWI Foundation halt: {e}")
            # Propagate to caller; never swallow
            raise
```

---

## 6. IMPLICATIONS

### For Module 00 Kernel Wrapping
**Module 00 does NOT need its own kernel** because:
- It is not a threat boundary
- It does not make security decisions
- It only relays decisions from other modules

### For Testing
- Unit tests: Mock M01–M10, inject halt signals
- Integration tests: Run with M02/M05 real kernels; verify halts propagate
- Adversarial tests: Try to bypass halt → should always fail

### For Future Modules (11–46)
- Each new module follows same pattern: does its job, signals halt if violated
- Trainer does not change

---

## 7. TRADE-OFFS

| Property | Value | Rationale |
|----------|-------|-----------|
| **Speed** | Sequential (slower) | Fail-closed design prioritizes safety |
| **Coupling** | Tight (all modules loaded upfront) | Easier to audit; simpler halt propagation |
| **Parallelism** | None (now) | Design for Modules 11+ later |
| **Extensibility** | High (add modules without changing Trainer logic) | Each module is self-contained |

---

## 8. DECISION RATIONALE SUMMARY

| Criterion | Why Passive Orchestrator Wins |
|-----------|---|
| **Safety** | Fail-closed halt propagation is simpler, more auditable |
| **Auditability** | No hidden validation logic in Trainer; policy belongs to modules |
| **Testability** | Can mock individual modules independently |
| **Maintainability** | Module changes don't cascade to Trainer |
| **Alignment with SWI philosophy** | Trainer as "dumb relay" fits CEK principle of "explicit boundaries" |

---

## 9. OPEN QUESTIONS

1. **Should Trainer validate module ordering?**
   - Current: Assumes correct order. Future: Add validation if module dependencies declared.

2. **Should Trainer support module skip/override?**
   - Current: No. Future: Maybe, for testing simulation mode.

3. **Should Trainer auto-restart on soft failures?**
   - Current: No (fail-closed). This is a feature, not a limitation.

---

## 10. APPROVAL & SIGN-OFF

| Role | Status | Notes |
|------|--------|-------|
| Architecture Review | 🔲 Pending | Awaiting independent review |
| Implementation | ✅ Done | Code matches decision |
| Testing | ✅ Started | Unit tests passing |
| Seal 5 Gate | 🔲 Pending | After all 00-10 kernels complete |

---

## 11. RELATED DOCUMENTS

- `MODULE_00_TRAINER_SEAL_RECORD.md` — Evidence of kernel integration
- `MODULE_00_TRAINER_INSPECTION.md` — Code review findings
- `MODULE_00_TRAINER_MIGRATION.md` — Kernel injection procedure
