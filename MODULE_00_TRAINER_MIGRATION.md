# MODULE 00: THE TRAINER — KERNEL MIGRATION PROCEDURE

**Module:** The Trainer (M00 Master Orchestrator)  
**Procedure:** Kernel integration + halt relay hardening  
**Authority:** Keletso Ronald Mosidila, SWI Architecture  
**Date:** September 15, 2026  
**Status:** PROCEDURE DEFINED; EXECUTION PENDING M02/M05/M03–M10 kernels  

---

## 1. MIGRATION DECISION

**Should Module 00 be kernel-wrapped?**

### Answer: No active kernel wrapping needed (today).

**Reasoning:**
- Trainer is not a threat boundary; it is a relay for halt signals
- No input validation that could fail
- No security decisions made by Trainer itself
- All validation delegated to downstream modules (M02, M05, etc.)

**However:** Trainer's **halt propagation itself** must be verified to never swallow signals.

This is tested in `test_trainer_kernel_halt.py` (see INSPECTION.md), not via kernel injection.

---

## 2. WHEN TRAINER KERNEL WRAPPING WOULD BE NEEDED

Kernel wrapping becomes necessary only if:

1. **Trainer starts making security decisions** (e.g., "allow/deny module startup")
2. **New threat model emerges** (e.g., adversary tries to hide halt signals)
3. **Parallelism added** (race conditions in halt propagation)
4. **Configuration tampering** becomes in-scope

**None of these apply to M00 v1.0.**

---

## 3. HALT RELAY HARDENING (Alternative to Kernel Wrapping)

Instead of kernel wrapping, M00's halt propagation is hardened through:

### 3.1 Immutable Halt Queue

**Current:** Standard `queue.Queue()`

**Hardened:** Switch to immutable event log (see implementation below)

```python
from swi_core.module_kernel import ImmutableLog

class TrainerHalted(ImmutableLog):
    """Immutable halt event; cannot be forged or suppressed."""
    
    def __init__(self, module_id: int, reason: str, timestamp: float):
        self.module_id = module_id
        self.reason = reason
        self.timestamp = timestamp
        self.hash = hashlib.sha256(
            f"{module_id}:{reason}:{timestamp}".encode()
        ).hexdigest()
```

**Deployment:** Swap `queue.Queue()` → `ImmutableLog()` in `Trainer.__init__`

### 3.2 Tamper-Detection on Halt Propagation

Add verification before raising HaltException:

```python
def run(self):
    """Execute modules; halt on kernel signal."""
    try:
        self._initialize_modules()
        for module_id in self.module_order:
            module = self.modules[module_id]
            module.run()  # Any kernel halt here will propagate up
            
            # Verify no halt signals were swallowed
            if self.halt_log.has_new_halts():
                for halt in self.halt_log.get_new_halts():
                    # Verify halt signature (M02/M05 signed it)
                    if not verify_halt_signature(halt):
                        self.logger.critical(f"TAMPERED HALT: {halt}")
                        raise SecurityViolation("Halt tampered with")
                    
                    # Propagate immediately
                    raise HaltException(halt)
    except HaltException:
        raise  # Never swallow
```

### 3.3 Immutable Audit Trail

All halt events logged to immutable audit log:

```python
# Inside Trainer.run()
self.audit_log.append({
    "event": "halt_received",
    "module": module_id,
    "reason": halt.reason,
    "timestamp": time.time(),
    "action": "raised_HaltException",
})
```

---

## 4. MIGRATION PROCEDURE (If Future Kernel Wrapping Needed)

If you decide to add active kernel wrapping to M00, follow this procedure:

### Phase 1: Design Kernel Contract

```python
# kernel_module00_contract.py
"""
Trainer kernel contract:
1. Halt signals from downstream modules (M02/M05/M03–M10) must propagate
2. No halt signal can be swallowed or modified
3. All halt events must be logged in order
4. Config validation must complete before module initialization
"""
```

### Phase 2: Implement Kernel Wrapper

```python
# swi_core/kernel_module00.py
from swi_core.module_kernel import ModuleKernel

class TrainerKernel(ModuleKernel):
    """Verify Trainer's halt propagation contract."""
    
    def pre_run(self, config):
        """Before Trainer.run(): snapshot configuration + halt count."""
        self.halt_count_before = self.audit_log.count("halt_received")
        self.config_snapshot = hashlib.sha256(
            json.dumps(config, sort_keys=True).encode()
        ).hexdigest()
        self.logger.info(f"Trainer pre-check: {self.halt_count_before} halts, config={self.config_snapshot[:8]}")
    
    def post_run(self, result=None, exception=None):
        """After Trainer.run(): verify all halts propagated."""
        halt_count_after = self.audit_log.count("halt_received")
        
        if halt_count_after > self.halt_count_before:
            # Halts occurred during run
            new_halts = halt_count_after - self.halt_count_before
            
            # Verify: if halts occurred, exception must be HaltException
            if exception is None:
                self.logger.critical(f"KERNEL VIOLATION: {new_halts} halt(s) detected, but no exception raised")
                raise KernelViolation("Halt signals swallowed")
            
            if not isinstance(exception, HaltException):
                self.logger.critical(f"KERNEL VIOLATION: Wrong exception type {type(exception)}")
                raise KernelViolation(f"Expected HaltException, got {type(exception)}")
            
            self.logger.info(f"Trainer post-check: All {new_halts} halt(s) propagated correctly")
        else:
            # No halts occurred; execution completed normally
            if isinstance(exception, HaltException):
                self.logger.critical("KERNEL VIOLATION: Exception but no halt in log")
                raise KernelViolation("False HaltException")
            
            self.logger.info("Trainer post-check: No halts; execution completed")
```

### Phase 3: Wire Kernel to Trainer

```python
# swi_core/module00_trainer.py

from swi_core.kernel_module00 import TrainerKernel

class Trainer:
    def __init__(self, config_path: str):
        self.config = load_config(config_path)
        self.kernel = TrainerKernel()
        self.modules = {}
        self.audit_log = ImmutableLog()
    
    def run(self):
        """Execute with kernel wrapping."""
        self.kernel.pre_run(self.config)
        
        exception_to_raise = None
        try:
            self._initialize_modules()
            for module_id in self.module_order:
                module = self.modules[module_id]
                module.run()
        except HaltException as e:
            exception_to_raise = e
        except Exception as e:
            self.logger.critical(f"Unexpected error: {e}")
            exception_to_raise = e
        finally:
            self.kernel.post_run(exception=exception_to_raise)
        
        if exception_to_raise:
            raise exception_to_raise
```

### Phase 4: Test Kernel Contract

```python
# test/test_trainer_kernel_wrapping.py

def test_kernel_detects_swallowed_halt():
    """Kernel should catch if halt signal is swallowed."""
    trainer = Trainer(config)
    
    # Patch to swallow halt
    original_run = trainer.run
    def malicious_run():
        try:
            return original_run()
        except HaltException:
            return None  # Swallow
    
    trainer.run = malicious_run
    
    # Kernel should detect violation
    with pytest.raises(KernelViolation) as exc_info:
        trainer.run()
    
    assert "swallowed" in str(exc_info.value)

def test_kernel_verifies_correct_exception_type():
    """Kernel should reject wrong exception type."""
    trainer = Trainer(config)
    m02 = trainer.modules[2]
    
    # Inject halt, but swallow and raise different exception
    def bad_handler():
        trainer.audit_log.append({"event": "halt_received", ...})
        raise ValueError("Wrong exception")  # Should be HaltException
    
    with pytest.raises(KernelViolation):
        trainer.run()
```

### Phase 5: Validate in CI

```yaml
# .github/workflows/kernel-module00.yml
name: Module 00 Kernel Verification

on: [push, pull_request]

jobs:
  kernel-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Trainer Kernel Tests
        run: |
          pytest test/test_trainer_kernel_wrapping.py -v
          python3 scripts/verify_trainer_kernel.py
```

---

## 5. ROLLBACK PLAN

If kernel wrapping is added and causes issues:

### Rollback Steps

1. **Revert kernel code:**
   ```bash
   git revert <commit-adding-kernel>
   git push origin main
   ```

2. **Restore immutable halt log (fallback):**
   Keep `ImmutableLog` even after removing kernel; it's not expensive.

3. **Validate in CI:**
   ```bash
   make test  # Should pass with pre-kernel version
   ```

4. **Investigation:**
   - Review `kernel_module00.py` for contract violations
   - Check if pre-conditions or post-conditions were too strict
   - Adjust contract if needed

---

## 6. CURRENT STATUS: NOT KERNEL-WRAPPED

**Module 00 today is:**
- ✅ Implemented
- ✅ Unit tested
- ✅ Boundary condition tested
- ✅ Adversarial tested
- 🔲 Kernel wrapped (not needed v1.0)
- 🔲 Seal 5 certified (awaiting other modules' kernels)

**Next step:** After M02, M03, M05–M10 kernels are deployed, revisit M00 for possible hardening.

---

## 7. MIGRATION CHECKLIST (When/If Implementing)

- [ ] Design kernel contract (pre/post conditions)
- [ ] Implement `TrainerKernel` class
- [ ] Wire kernel into `Trainer.run()`
- [ ] Write kernel contract tests
- [ ] Test rollback procedure
- [ ] Validate in clean environment
- [ ] Update documentation (SEAL_RECORD, INSPECTION)
- [ ] CI/CD validation passes
- [ ] Independent review passes
- [ ] Mark as kernel-wrapped in IMPLEMENTATION_STATUS.md

---

## 8. SIGN-OFF

| Phase | Owner | Status | Date |
|-------|-------|--------|------|
| Procedure Design | Keletso R. Mosidila | ✅ Complete | 2026-09-15 |
| Implementation | (On hold) | 🔲 Pending | — |
| Testing | (On hold) | 🔲 Pending | — |
| CI Validation | (On hold) | 🔲 Pending | — |
| Kernel Integration Approval | (Depends on M02/M05/M03–M10) | 🔲 Pending | — |

---

## 9. RELATED DOCUMENTS

- `MODULE_00_TRAINER_SEAL_RECORD.md` — Current evidence (pre-kernel)
- `MODULE_00_TRAINER_DECISION.md` — Why no active kernel needed v1.0
- `MODULE_00_TRAINER_INSPECTION.md` — Testing framework + boundary conditions
- `VOLUME_1_PART_3_ENHANCED_FOUNDATION_COMPLETION.md` — Full migration order
