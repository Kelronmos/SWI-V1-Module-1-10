# SWI MODULES 00–10: INTEGRATION DEPENDENCY MATRIX

**Authority:** Keletso Ronald Mosidila, SWI Architecture  
**Date:** September 15, 2026  
**Purpose:** Map all module dependencies, kernel injection points, and halt propagation  

---

## 1. DEPENDENCY GRAPH (Text Representation)

```
                       ┌──────────────────────────┐
                       │  CONFIG & STARTUP        │
                       │  (config/swi_config.yaml)│
                       └───────────┬──────────────┘
                                   │
                       ┌───────────▼──────────────┐
                       │  M00: TRAINER            │
                       │  (Orchestrator)          │
                       │  Instantiates M01–M10    │
                       │  Receives halt signals   │
                       └──┬──┬──┬──┬──┬──┬──┬──┬──┬─┘
                          │  │  │  │  │  │  │  │  │
          ┌───────────────┴──┘  │  │  │  │  │  │  └──────────┐
          │                      │  │  │  │  │  │             │
    ┌─────▼────────┐       ┌─────▼──┴──┬──┘  │  │             │
    │ M01: Node    │       │ M02: Sec  │     │  │             │
    │ Scanner      │       │ Probe     │     │  │             │
    │              │       │ [SEALED]  │     │  │             │
    │ Scans        │       │           │     │  │             │
    │ environment  │       │ Detects   │     │  │             │
    │              │       │ injection │     │  │             │
    └──────────────┘       └─────┬─────┘     │  │             │
                                 │ (halt)    │  │             │
                           ┌─────▼────────┐  │  │             │
                           │ M03: Context │  │  │             │
                           │ Sync         │  │  │             │
                           │              │  │  │             │
                           │ Validates    │  │  │             │
                           │ timestamps   │  │  │             │
                           └─────┬────────┘  │  │             │
                                 │ (halt)    │  │             │
                           ┌─────▼────────┐  │  │             │
                           │ M04: Encrypt │  │  │             │
                           │              │  │  │             │
                           │ Wraps comms  │  │  │             │
                           │ (AES-256)    │  │  │             │
                           └─────┬────────┘  │  │             │
                                 │ (halt)    │  │             │
                           ┌─────▼────────┐  │  │             │
                           │ M05: Redact  │  │  │             │
                           │ [KERNEL]     │  │  │             │
                           │              │  │  │             │
                           │ PII→redact   │  │  │             │
                           └─────┬────────┘  │  │             │
                                 │ (halt)    │  │             │
                           ┌─────▼────────┐  │  │             │
                           │ M06: Drift   │  │  │             │
                           │ Analyzer     │  │  │             │
                           │              │  │  │             │
                           │ Tolerance    │  │  │             │
                           │ boundary     │  │  │             │
                           └─────┬────────┘  │  │             │
                                 │ (halt)    │  │             │
                           ┌─────▼────────┐  │  │             │
                           │ M07: Memory  │  │  │             │
                           │ Validator    │  │  │             │
                           │              │  │  │             │
                           │ Scar         │  │  │             │
                           │ integrity    │  │  │             │
                           └─────┬────────┘  │  │             │
                                 │ (halt)    │  │             │
                           ┌─────▼────────┐  │  │             │
                           │ M08: Access  │  │  │             │
                           │ Auth         │  │  │             │
                           │              │  │  │             │
                           │ Identity     │  │  │             │
                           │ anchor       │  │  │             │
                           └─────┬────────┘  │  │             │
                                 │ (halt)    │  │             │
                           ┌─────▼────────┐  │  │             │
                           │ M09: Audit   │  │  │             │
                           │ Logger       │  │  │             │
                           │              │  │  │             │
                           │ Immutable    │  │  │             │
                           │ flight rec.  │  │  │             │
                           └─────┬────────┘  │  │             │
                                 │ (halt)    │  │             │
                           ┌─────▼────────┐  │  │             │
                           │ M10: Ext     │  │  │             │
                           │ Sandbox      │  │  │             │
                           │              │  │  │             │
                           │ Air-gap      │  │  │             │
                           │ shield       │  │  │             │
                           └─────┬────────┘  │  │             │
                                 │ (halt)    │  │             │
                                 │◄──────────┴──┴─────────────┘
                           ┌─────▼────────────────────┐
                           │  M00: Collect all halts  │
                           │  Propagate to caller     │
                           │  Raise HaltException     │
                           └──────────────────────────┘
```

---

## 2. MODULE DEPENDENCY TABLE

| Module | Purpose | Dependencies | Dependents | Kernel Status | Halt Propagates? |
|--------|---------|---|---|---|---|
| **M00** | Trainer/Orchestrator | Config, M01–M10 | None | No (relay only) | ✅ YES (from M01–M10) |
| **M01** | Node Scanner | Config, environment | M02–M10 | Pending | ✅ Can halt |
| **M02** | Security Probe | Config | M03–M10 | SEALED ✅ | ✅ YES (prompt injection) |
| **M03** | Context Sync | Config | M04–M10 | Pending | ✅ Can halt (staleness) |
| **M04** | Encryption | Config | M05–M10 | Pending | ✅ Can halt |
| **M05** | Redaction | Config | M06–M10 | KERNEL ✅ | ✅ YES (PII exposure) |
| **M06** | Drift Analyzer | Config | M07–M10 | Pending | ✅ Can halt (tolerance) |
| **M07** | Memory Validator | Config, M09 | M08–M10 | Pending | ✅ Can halt (scar) |
| **M08** | Access Auth | Config, M09 | M09–M10 | Pending | ✅ Can halt (auth) |
| **M09** | Audit Logger | Config | M10 | Pending | ✅ Can halt (log full) |
| **M10** | External Sandbox | Config, M09 | None | Pending | ✅ Can halt (sandbox escape) |

---

## 3. KERNEL INJECTION POINTS

Each module has specific places where kernel wrapping occurs:

### M01: Node Scanner
```python
# swi_core/module01_node_scanner.py
class NodeScanner:
    def run(self):
        # PRE-CHECK: Kernel validates config exists
        self.kernel.pre_run(self.config)
        
        try:
            # CORE LOGIC: Scan environment
            nodes = self.scan_environment()
            
            # POST-CHECK: Kernel verifies scan completed
            self.kernel.post_run(nodes)
            return nodes
        except Exception as e:
            self.kernel.post_run(exception=e)
            raise
```

### M02: Security Probe (SEALED)
```python
# swi_core/module02_security_probe.py
class SecurityProbe:
    def run(self):
        self.kernel.pre_run(self.config)
        
        try:
            # Probe for injection attacks
            attacks = self.detect_attacks()
            
            # KERNEL DECISION: If attacks detected, halt
            if attacks:
                self.kernel.raise_halt(f"Detected {len(attacks)} attacks")
            
            self.kernel.post_run(attacks)
            return attacks
        except KernelHalt:
            raise  # Propagate halt upward
```

### M03: Context Sync
```python
# swi_core/module03_context_sync.py
class ContextSync:
    def run(self):
        self.kernel.pre_run(self.config)
        
        try:
            # Validate timestamps (X-1, X, X+1)
            state = self.synchronize_context()
            
            # KERNEL DECISION: If timestamps stale, halt
            if self.check_staleness() > self.threshold:
                self.kernel.raise_halt("Context timestamps stale")
            
            self.kernel.post_run(state)
            return state
        except KernelHalt:
            raise
```

### M05: Redaction (KERNEL-ENFORCED)
```python
# swi_core/module05_redaction_engine.py
class RedactionEngine:
    def run(self):
        self.kernel.pre_run(self.config)
        
        try:
            # Redact PII
            result = self.redact_pii()
            
            # KERNEL DECISION: If PII leaked, halt immediately
            if self.detect_pii_exposure():
                self.kernel.raise_halt("PII exposure boundary crossed")
            
            self.kernel.post_run(result)
            return result
        except KernelHalt:
            raise
```

**Pattern repeats for M04, M06–M10.**

---

## 4. HALT PROPAGATION CHAIN

When any module halts:

```
M02 kernel.raise_halt("prompt_injection")
  │
  └─→ raises KernelHalt exception
      │
      └─→ M02.run() catches and re-raises
          │
          └─→ M00 (Trainer) catches KernelHalt
              │
              └─→ Logs: "M02 kernel halt: prompt_injection"
                  │
                  └─→ Appends to audit_log (immutable)
                      │
                      └─→ Raises HaltException to caller
                          │
                          └─→ Caller must handle or system stops
```

**Rule:** Never swallow a halt. Once raised, it must propagate to the top level.

---

## 5. SHARED RESOURCES & CROSS-MODULE DEPENDENCIES

### Config (Shared by All Modules)

```yaml
# config/swi_config.yaml (source of truth for all modules)

# M02 Security Probe config
security_probe:
  attack_patterns: [injection_types_file]
  tolerance: "heuristic"

# M03 Context Sync config
context_sync:
  staleness_threshold: 30  # seconds
  time_deltas: [-1, 0, 1]  # X-1/X/X+1

# M04 Encryption config
encryption:
  algorithm: "AES-256"
  key_rotation_days: 90

# M05 Redaction config
redaction:
  pii_patterns: [email, phone, credit_card, bw_omang]
  preserve_patterns: none  # No "safe" PII

# M07 Memory Validator config
memory_validator:
  max_scar_size_mb: 256

# M09 Audit Logger config
audit_logger:
  max_log_size_mb: 1024
  log_path: "./logs/audit.jsonl"
```

**Update mechanism:**
1. ConfigLoader reads swi_config.yaml once at startup
2. All modules get reference to config
3. No module modifies config (read-only)
4. Changes require restart

### Audit Log (Written by M09, Read by M00)

```python
# All modules write to shared audit log via M09
logs = [
    {"timestamp": 1694784000, "module": 2, "event": "run_started"},
    {"timestamp": 1694784001, "module": 2, "event": "attack_detected", "count": 1},
    {"timestamp": 1694784001, "module": 2, "event": "halt_raised", "reason": "prompt_injection"},
    # Trainer sees this halt entry and raises exception
]
```

---

## 6. EXECUTION SEQUENCE (Happy Path, No Halts)

```
Time  Event
────  ────────────────────────────────────────────────────
0ms   M00 Trainer starts
10ms  M01 Node Scanner
      └─ Pre-check: ✅
      └─ Scan environment: ✅
      └─ Post-check: ✅
20ms  M02 Security Probe (SEALED)
      └─ Pre-check: ✅
      └─ Detect attacks: ✅ (none found)
      └─ Post-check: ✅
30ms  M03 Context Sync
      └─ Pre-check: ✅
      └─ Check timestamps: ✅ (within tolerance)
      └─ Post-check: ✅
40ms  M04 Encryption Handler
      └─ Pre-check: ✅
      └─ Wrap comms: ✅
      └─ Post-check: ✅
50ms  M05 Redaction Engine (KERNEL)
      └─ Pre-check: ✅
      └─ Redact PII: ✅
      └─ Detect exposure: ✅ (no PII found)
      └─ Post-check: ✅
60ms  M06 Drift Analyzer
      └─ Pre-check: ✅
      └─ Analyze drift: ✅ (within tolerance)
      └─ Post-check: ✅
70ms  M07 Memory Validator
      └─ Pre-check: ✅
      └─ Validate scar: ✅ (integrity OK)
      └─ Post-check: ✅
80ms  M08 Access Auth
      └─ Pre-check: ✅
      └─ Validate auth: ✅
      └─ Post-check: ✅
90ms  M09 Audit Logger
      └─ Pre-check: ✅
      └─ Write logs: ✅
      └─ Post-check: ✅
100ms M10 External Sandbox
      └─ Pre-check: ✅
      └─ Run sandbox: ✅ (no escape)
      └─ Post-check: ✅
110ms M00 Trainer collects all results
      └─ All modules complete; no halts
      └─ Return success
```

---

## 7. EXECUTION SEQUENCE (Halt Scenario)

```
Time  Event
────  ────────────────────────────────────────────────────
...
30ms  M03 Context Sync
      └─ Pre-check: ✅
      └─ Check timestamps: ❌ STALE (drift > 30s)
      └─ Kernel decision: HALT
      └─ raise_halt("Context timestamps stale")
      └─ raises KernelHalt
      
31ms  M03 exception handler catches KernelHalt
      └─ Logs: "M03 kernel halt"
      └─ Re-raises KernelHalt
      
32ms  M00 Trainer.run() catches exception
      └─ Identifies: KernelHalt from M03
      └─ Logs: "Foundation halt at M03: Context timestamps stale"
      └─ Appends to audit_log (immutable)
      └─ Raises HaltException to caller
      
33ms  Caller (test harness / main script) catches HaltException
      └─ Shutdown protocol activated
      └─ Clean up resources
      └─ Return error code
      
M04–M10 never execute (halt stops at M03)
```

---

## 8. DEPENDENCY VALIDATION CHECKLIST

Before starting any module kernel migration, verify:

```
[ ] Config file has all required sections
[ ] Config values are within acceptable ranges
[ ] Previous module completed successfully
[ ] Halt propagation chain is unbroken (M01 → M00)
[ ] Audit log is writable (M09)
[ ] All test files exist
[ ] All documentation files exist
[ ] No circular dependencies
```

---

## 9. CROSS-MODULE TESTING MATRIX

| Test Name | Modules Involved | Purpose | Status |
|-----------|---|---|---|
| `test_bootstrap` | M00, Config | Verify trainer loads config | ✅ Pass |
| `test_sequential_execution` | M00, M01–M10 | Verify modules run in order | ✅ Pass |
| `test_m02_halt_propagates` | M02 → M00 | Verify security halt reaches trainer | ✅ Pass |
| `test_m05_halt_propagates` | M05 → M00 | Verify redaction halt reaches trainer | ✅ Pass |
| `test_all_halts_propagate` | M01–M10 → M00 | Verify each module's halt works | 🔲 Pending (all modules) |
| `test_no_halt_swallowing` | M00 | Adversarial: try to suppress halt | ✅ Pass |
| `test_audit_log_immutable` | M09 | Verify logs can't be tampered | ✅ Pass |
| `test_config_readonly` | All | Verify modules don't modify config | ✅ Pass |

---

## 10. FAULT INJECTION SCENARIOS

To validate robustness, inject these faults:

### Fault A: M02 Forced Halt
```python
def test_m02_forced_halt():
    m02 = SecurityProbe(config)
    m02.kernel.force_halt("test_injection")
    
    trainer = Trainer(config)
    with pytest.raises(HaltException):
        trainer.run()
```

### Fault B: M05 Detects PII
```python
def test_m05_pii_boundary():
    config["test_data"] = "test@example.com"
    m05 = RedactionEngine(config)
    
    with pytest.raises(KernelHalt):
        m05.run()
```

### Fault C: Halt Disappears (Catch & Don't Re-raise)
```python
def test_adversarial_swallow_halt():
    trainer = Trainer(config)
    m02 = trainer.modules[2]
    
    original_run = m02.run
    def swallow_halt():
        try:
            return original_run()
        except KernelHalt:
            return None  # Swallow halt
    
    m02.run = swallow_halt
    
    # Test framework should catch this
    # (Can't hide a halt if audit log is immutable)
    # Trainer.run() will fail at post-check
```

---

## 11. PERFORMANCE TARGETS

| Metric | Target | Acceptable Range |
|--------|--------|---|
| M01 Node Scanner | < 50ms | 30–70ms |
| M02 Security Probe | < 100ms | 50–150ms |
| M03 Context Sync | < 30ms | 20–50ms |
| M04 Encryption | < 40ms | 30–60ms |
| M05 Redaction | < 60ms | 40–80ms |
| M06 Drift Analyzer | < 25ms | 15–40ms |
| M07 Memory Validator | < 35ms | 20–50ms |
| M08 Access Auth | < 20ms | 10–30ms |
| M09 Audit Logger | < 50ms | 30–70ms |
| M10 External Sandbox | < 100ms | 50–150ms |
| **Total (all 10)** | < 600ms | 400–800ms |

**Rationale:** Each module is bounded; total is predictable.

---

## 12. SIGN-OFF

| Role | Name | Status |
|------|------|--------|
| Architecture Review | Keletso R. Mosidila | ✅ Ready |
| Dependency Verification | (TBD) | 🔲 Pending |
| CI Integration | (TBD) | 🔲 Pending |

---

**End of Integration Dependency Matrix**
