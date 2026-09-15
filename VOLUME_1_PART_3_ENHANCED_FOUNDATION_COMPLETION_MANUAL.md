# THE SWI ARCHITECTURE — VOLUME 1 PART 3 (ENHANCED)
## FOUNDATION COMPLETION, VERIFICATION & SEALING MANUAL
### Modules 00–10 with Step-by-Step Rebuild Procedures

**Author:** Keletso Ronald Mosidila — Trusts Motion, Botswana  
**Date:** September 15, 2026  
**Status:** Foundation Sealing (Seal 1 → Seal 5)  

---

## EXECUTIVE SUMMARY

This manual provides **procedural authority** for completing the SWI foundation (Modules 00–10).

### Current State
- **Module 02:** SEALED (kernel + trainer halt + local + CI)
- **Module 05:** KERNEL-ENFORCED (structured PII only; awaiting CI confirmation)
- **Modules 01, 03, 04, 06, 07, 08, 09, 10:** Implemented; not kernel-migrated
- **Module 00:** Trainer; awaits downstream seals

### Migration Order (LOCKED)
```
02 SEALED ✅
   ↓
05 KERNEL-ENFORCED
   ↓
03 NEXT → 06 → 07 → 09 → 01 → 04 → 08 → 10
   ↓
00 Trainer (final integration)
   ↓
SEAL 5 GATE → Modules 11-19 Unblocked
```

### Seal Levels
| Level | Meaning | Prerequisite |
|-------|---------|---|
| Seal 1 | Reconstruction exists | Code + tests in repo |
| Seal 2 | Core automated tests pass | pytest passing locally |
| Seal 3 | Kernel pilot passes | Module kernel injection working |
| Seal 4 | Adversarial & boundary testing | Attack scenarios tested |
| Seal 5 | Independent verification | Third-party review + clean CI pass |

**Rule:** Do not advance to Modules 11–19 until Seal 5 is achieved for all 00–10.

---

## PART A: POLICY & GOVERNANCE

### A.1 Authority Hierarchy

```
Code (source of truth)
  ↓
Automated Tests (proves code works)
  ↓
Reproducible Results (can run again with same outcome)
  ↓
Documentation (explains what code does)
  ↓
Architectural Material (why decisions were made)
```

**Rule:** Never document → assume → implement. Only: code → test → result → document.

### A.2 Six Questions Before Every Module

Before starting kernel migration on any module, ask:

1. **Does the source code exist?** (If no → stop; implement first)
2. **Do the tests pass locally?** (If no → debug locally first; don't blame CI)
3. **What is this module's bounded claim?** (If unclear → update DECISION.md first)
4. **What are the boundary conditions?** (If unmapped → add to INSPECTION.md first)
5. **How will the kernel wrap this module?** (If unclear → review kernel_template.py)
6. **Can we prove it halts correctly?** (If no → test harness not ready)

**If any answer is no or unclear, that module is not ready for kernel migration. Skip to next module.**

### A.3 Development Discipline

**One logical change per commit.** For each module:

```
[M03-01] Implement M03 ContextSync kernel pre-check
[M03-02] Add boundary tests for staleness window
[M03-03] Document Module 03 kernel decision
[M03-04] CI validation for M03 kernel
```

Not:
```
[M03-all] Implement kernel, tests, docs, CI all at once ← Too large; impossible to review
```

---

## PART B: STEP-BY-STEP REBUILD PROCEDURE

### B.1 Pre-Rebuild Verification

**Do this once before starting any module:**

```bash
# 1. Clone clean repo
git clone <swi-repo> swi-foundation-rebuild
cd swi-foundation-rebuild

# 2. Baseline tests
git checkout main
python3 -m pytest test_swi_core.py -q
# Expected: all pass or only expected failures

# 3. Baseline CI
git log --oneline | head -5
# Verify last commit passed CI

# 4. Check current seal status
cat docs/IMPLEMENTATION_STATUS.md
# Verify: Module 02 SEALED, Module 05 KERNEL-ENFORCED
```

---

### B.2 Rebuild Sequence (Detailed)

#### MILESTONE 1: Module 02 (Already SEALED — Verify Only)

**Action:** Confirm Module 02 seal is still valid.

```bash
# Step 1: Review seal evidence
cat docs/MODULE_02_SEAL_RECORD.md

# Step 2: Run Module 02 tests
python3 -m pytest test/test_security_probe_kernel.py -v

# Step 3: Run adversarial tests
python3 -m pytest test/adversarial/test_security_probe_boundaries.py -v

# Step 4: Verify CI passed
git log --oneline docs/MODULE_02_SEAL_RECORD.md | head -1
# Note the commit; check GitHub Actions passed on that commit

# Step 5: Sign-off (if all passing)
echo "M02 Seal verified: $(date)" >> logs/seal_audit.log

# Status: ✅ SEALED (no action needed)
```

---

#### MILESTONE 2: Module 05 (Kernel-Enforced — Harden Only)

**Action:** Harden existing M05 kernel; don't rebuild.

```bash
# Step 1: Review existing kernel evidence
cat docs/MODULE_05_SEAL_RECORD.md

# Step 2: Run M05 kernel tests
python3 -m pytest test/test_redaction_kernel.py -v

# Step 3: Check M05 CI status
# On GitHub: Actions tab → filter by "module05" → last run should show ✅

# Step 4: If M05 CI fails, investigate
python3 -m pytest test/test_redaction_kernel.py::test_pii_redaction_email -vvv
# Debug the failure locally before touching CI

# Step 5: Harden evidence (add documentation if missing)
# Ensure MODULE_05_SEAL_RECORD.md is complete:
#   - Bounded claims ✅
#   - Test results ✅
#   - Adversarial tests ✅
#   - Known limitations ✅

# Step 6: Mark CI pass
# Update docs/MODULE_05_SEAL_RECORD.md:
#   "CI Status: ✅ PASS (Actions run abc123def789)"

# Status: ✅ KERNEL-ENFORCED + HARDENED
```

---

#### MILESTONE 3: Module 03 (Context Sync — KERNEL MIGRATION NEXT)

**This is the critical next module. Follow exactly:**

```bash
# Pre-check: Six questions
# 1. Source code exists? YES (swi_core/module03_context_sync.py)
# 2. Tests pass locally? RUN:
python3 -m pytest test/test_context_sync_kernel.py -v
#   → Expected: Tests exist and pass
# 3. Bounded claim clear? YES (see MODULE_03_DECISION.md)
# 4. Boundary conditions mapped? YES (see MODULE_03_INSPECTION.md)
# 5. Kernel wrap strategy? YES (review kernel_module03.py template)
# 6. Can prove halt? YES (test suite ready)

# STEP 1: Understand current implementation
python3 << 'EOF'
import sys
sys.path.insert(0, '.')
from swi_core.module03_context_sync import ContextSync
from swi_core.config_loader import load_config

config = load_config('config/swi_config.yaml')
ctx_sync = ContextSync(config)

# Print current contract
print("ContextSync contract:")
print(f"  - Timestamp tolerance: {ctx_sync.staleness_threshold} seconds")
print(f"  - Accepted time deltas: X-1/X/X+1 (configurable)")
print(f"  - Halt on: timestamp drift > threshold")
EOF

# STEP 2: Inspect kernel injection points
cat swi_core/module03_context_sync.py | grep -n "def run\|def check\|def validate"

# STEP 3: Create kernel wrapper
cat > swi_core/kernel_module03.py << 'EOF'
from swi_core.module_kernel import ModuleKernel
import time

class ContextSyncKernel(ModuleKernel):
    """Verify ContextSync boundaries: timestamp staleness detection."""
    
    def pre_run(self, context):
        self.timestamp_before = time.time()
        self.logger.info(f"M03 pre-check: timestamp={self.timestamp_before}")
    
    def post_run(self, result, exception=None):
        timestamp_after = time.time()
        staleness = timestamp_after - self.timestamp_before
        
        # If staleness exceeded threshold, should have halted
        if staleness > self.get_threshold():
            if exception is None:
                raise KernelViolation("Staleness exceeded but no halt")
        
        self.logger.info(f"M03 post-check: staleness={staleness}s → OK")
EOF

# STEP 4: Inject kernel into module
# Edit swi_core/module03_context_sync.py:
#   Add at top: from swi_core.kernel_module03 import ContextSyncKernel
#   Add in run(): self.kernel.pre_run(...) and self.kernel.post_run(...)

# STEP 5: Test kernel
python3 -m pytest test/test_context_sync_kernel.py::test_kernel_detects_staleness -vvv

# STEP 6: Document findings
# Update docs/MODULE_03_INSPECTION.md with kernel test results

# STEP 7: Run full test suite
python3 -m pytest test_swi_core.py -q

# STEP 8: Commit
git add swi_core/kernel_module03.py swi_core/module03_context_sync.py docs/MODULE_03_*
git commit -m "[M03-kernel] Implement ContextSync kernel; staleness boundary"

# STEP 9: Validate in clean environment
git clone . /tmp/swi-test-m03
cd /tmp/swi-test-m03
python3 -m pytest test/test_context_sync_kernel.py -v

# STEP 10: Update IMPLEMENTATION_STATUS.md
# Change: "03 Context Sync | Implemented | not kernel-migrated"
# To:     "03 Context Sync | **KERNEL-ENFORCED** | timestamps ≥ X-1/X/X+1"

# Status: ✅ MODULE 03 KERNEL-ENFORCED
```

---

#### MILESTONE 4: Modules 06, 07, 09, 01, 04, 08, 10 (Repeat Pattern)

For each remaining module, follow the Module 03 pattern:

```bash
for module_id in 06 07 09 01 04 08 10; do
    echo "=== MILESTONE: Module $module_id ==="
    
    # Pre-check: Six questions
    # 1. Source code exists?
    [ -f "swi_core/module0${module_id}_*.py" ] || (echo "FAIL: Source missing"; exit 1)
    
    # 2. Tests pass locally?
    python3 -m pytest test/test_module0${module_id}_kernel.py -q || (echo "FAIL: Tests"; exit 1)
    
    # 3-6: Documented in MODULE_0X_DECISION.md/INSPECTION.md
    # (Automated check would verify these files exist and are complete)
    
    # MAIN WORK: Kernel injection (follow Module 03 pattern)
    # 1. Review implementation
    # 2. Identify injection points
    # 3. Create kernel_moduleXX.py
    # 4. Wire into moduleXX.py
    # 5. Test
    # 6. Document
    # 7. Commit
    # 8. Validate in clean environment
    # 9. Update IMPLEMENTATION_STATUS.md
done
```

**Time estimate:** 2–3 hours per module (investigate + test + document)

---

#### MILESTONE 5: Module 00 Trainer (Final Integration)

**Only after Modules 01–10 are kernel-enforced.**

```bash
# Step 1: Verify all 01–10 have kernels
grep "KERNEL-ENFORCED\|SEALED" docs/IMPLEMENTATION_STATUS.md | wc -l
# Should output: 10 (all modules)

# Step 2: Verify halt propagation
python3 -m pytest test/test_trainer_kernel_halt.py -v

# Step 3: Integration test (Trainer + all kernels)
python3 -m pytest test/test_trainer_all_kernels_integration.py -v

# Step 4: Adversarial: try to swallow halt
python3 -m pytest test/adversarial/test_trainer_swallow_halt.py -v

# Step 5: Document integration
# Update MODULE_00_TRAINER_SEAL_RECORD.md with integration evidence

# Step 6: Commit
git add test/test_trainer_all_kernels_integration.py docs/MODULE_00_TRAINER_SEAL_RECORD.md
git commit -m "[M00-integrate] Trainer integrates with all downstream kernels"

# Status: ✅ MODULE 00 SEALED
```

---

### B.3 Rebuild Checklist (Per Module)

```
Module: _____ (00-10)

PRE-CHECK:
  [ ] Source code exists
  [ ] Tests pass locally
  [ ] Bounded claim documented
  [ ] Boundary conditions mapped
  [ ] Kernel strategy defined
  [ ] Halt behavior testable

IMPLEMENTATION:
  [ ] Review implementation code
  [ ] Identify kernel injection points
  [ ] Create kernel_moduleXX.py
  [ ] Wire kernel into moduleXX.py
  [ ] Add pre-check and post-check

TESTING:
  [ ] Kernel tests pass locally
  [ ] Adversarial tests pass
  [ ] Full test suite passes
  [ ] Coverage acceptable (>80%)

DOCUMENTATION:
  [ ] SEAL_RECORD updated
  [ ] INSPECTION results documented
  [ ] Limitations noted
  [ ] Commit message clear

VALIDATION:
  [ ] Test in clean environment
  [ ] CI/CD automation configured
  [ ] Independent review (if available)
  [ ] Update IMPLEMENTATION_STATUS.md

COMMIT & PUSH:
  [ ] One logical change per commit
  [ ] Commit message follows standard
  [ ] CI pipeline passing
  [ ] Ready for next module
```

---

## PART C: EVIDENCE EXECUTION & VERIFICATION

### C.1 The Golden Rule

**CODE → TEST → RESULT → DOCUMENT**

Never reverse this order:

❌ DOCUMENT → ASSUME → IMPLEMENTED  
✅ IMPLEMENT → TEST → DOCUMENT → SEAL

### C.2 Test Result Collection

For each module, collect:

1. **Local test results** (pytest output)
2. **Adversarial test results** (boundary testing)
3. **Clean environment reproduction** (fresh clone, full test run)
4. **CI log output** (GitHub Actions / GitLab CI)
5. **Code review notes** (if independent reviewer involved)

Store in `docs/MODULE_0X_SEAL_RECORD.md`:

```markdown
## Evidence Collection

### Local Tests (Machine: Ubuntu 24.04, Python 3.11)
```
pytest test/test_moduleXX_kernel.py -v
[PASTE FULL OUTPUT HERE]
```

### CI Run
GitHub Actions Run: https://github.com/Kelronmos/SWI-V1-Module-1-10/actions/runs/[RUN_ID]
Status: ✅ PASS

### Adversarial Tests
[PASTE OUTPUT]
```

### C.3 Vocabulary (States)

Use consistent terminology:

| State | Meaning | Action |
|-------|---------|--------|
| **PLANNED** | Designed but not implemented | Do the implementation |
| **IMPLEMENTED** | Code written | Run tests |
| **TESTED** | Tests pass locally | Validate in CI |
| **VERIFIED** | Tests pass in clean environment | Submit for review |
| **SEALED** | Independent review passed | Advance to next module |

**Module progression:** PLANNED → IMPLEMENTED → TESTED → VERIFIED → SEALED

---

## PART D: FOUNDATION SEAL 5 CRITERIA

### D.1 Seal 5 Gate (Required for Modules 11-19)

To achieve Seal 5, **all of the following** must be true:

```
✅ Modules 00–10 all SEALED
✅ All kernel migrations complete
✅ All tests passing in CI
✅ All SEAL_RECORD/DECISION/INSPECTION/MIGRATION docs complete
✅ No known security issues
✅ No known architectural debt
✅ Independent technical review (if available)
✅ Reproducible build verified
✅ Rollback procedure documented and tested
✅ Monitoring & logging verified
```

### D.2 Seal 5 Checklist

```
SEAL 5 READINESS CHECKLIST
==========================

Module 00 (Trainer)
  [ ] SEALED
  [ ] Kernel migration complete (if applicable)
  [ ] All tests passing
  [ ] CI automation verified

Module 01 (Node Scanner)
  [ ] SEALED
  ... (same as above)

Module 02 (Security Probe)
  [ ] SEALED ✅ (already)

Module 03 (Context Sync)
  [ ] SEALED
  ... (same as above)

Module 04 (Encryption)
  [ ] SEALED
  ... (same as above)

Module 05 (Redaction)
  [ ] SEALED ✅ (already)

Module 06 (Drift Analyzer)
  [ ] SEALED
  ... (same as above)

Module 07 (Memory Validator)
  [ ] SEALED
  ... (same as above)

Module 08 (Access Auth)
  [ ] SEALED
  ... (same as above)

Module 09 (Audit Logger)
  [ ] SEALED
  ... (same as above)

Module 10 (External Sandbox)
  [ ] SEALED
  ... (same as above)

CROSS-MODULE:
  [ ] All kernel halts propagate correctly
  [ ] All module dependencies satisfied
  [ ] No circular dependencies
  [ ] Audit trail complete and immutable
  [ ] Performance acceptable
  [ ] Scalability assessed

DOCUMENTATION:
  [ ] All 40+ module docs complete
  [ ] Part 1, Part 2, Part 3 finalized
  [ ] Rebuild procedures tested
  [ ] Rollback procedures tested

SIGN-OFF:
  [ ] Author (Keletso R. Mosidila): _______________
  [ ] Independent Reviewer (if applicable): _______
  [ ] Date: _______

GATE STATUS: [ ] OPEN (continue to Modules 11-19)
             [ ] BLOCKED (resolve above items first)
```

---

## PART E: KNOWN LIMITATIONS & FUTURE WORK

### Current Limitations (Acceptable for Seal 5)

| Limitation | Impact | Target for Modules 11+ |
|-----------|--------|---|
| Sequential-only execution | Slow (5-10s for M00-M10) | Parallel execution with fall-back |
| No auto-recovery on soft halt | Hard stop on any failure | Graceful degradation mode |
| No module hot-reload | Can't update during runtime | Blue-green deployment for M11+ |
| No caching between runs | Reinitialize every run | State preservation + cache for M11+ |
| No simulation mode | Can't test "what-if" | Safe sandbox simulation for M11+ |

### Acceptable Trade-Offs

These are **features**, not bugs:

- **Fail-closed design:** Slow but safe
- **Sequential execution:** Deterministic but not parallel
- **No recovery:** Forces operators to fix root cause, not symptom

---

## APPENDIX: QUICK REFERENCE

### Module Status at a Glance

```
00 Trainer        🔲 Pending kernels 01-10
01 Node Scanner   🔲 Ready for kernel
02 Security Probe ✅ SEALED
03 Context Sync   🔲 Ready for kernel (NEXT AFTER M05)
04 Encryption     🔲 Ready for kernel
05 Redaction      ✅ KERNEL-ENFORCED (awaiting CI)
06 Drift Analyzer 🔲 Ready for kernel
07 Memory Valid.  🔲 Ready for kernel
08 Access Auth    🔲 Ready for kernel
09 Audit Logger   🔲 Ready for kernel
10 Ext. Sandbox   🔲 Ready for kernel
```

### File Structure

```
swi-foundation-rebuild/
├── swi_core/
│   ├── module00_trainer.py          ← Orchestrator
│   ├── module01_node_scanner.py
│   ├── module02_security_probe.py   ← M02 SEALED
│   ├── kernel_module02.py           ✅
│   ├── module03_context_sync.py
│   ├── kernel_module03.py           (to be created)
│   ... (repeat for 04-10)
│   ├── module_kernel.py             ← Kernel base class
│   └── config_loader.py
├── test/
│   ├── test_swi_core.py             ← Main test suite
│   ├── test_moduleXX_kernel.py      (per module)
│   └── adversarial/
│       ├── test_security_probe_boundaries.py
│       ├── test_redaction_boundaries.py
│       └── (more per module)
├── docs/
│   ├── MODULE_00_TRAINER_SEAL_RECORD.md (new)
│   ├── MODULE_00_TRAINER_DECISION.md     (new)
│   ├── MODULE_00_TRAINER_INSPECTION.md   (new)
│   ├── MODULE_00_TRAINER_MIGRATION.md    (new)
│   ├── MODULE_02_SEAL_RECORD.md     ✅ (existing)
│   ├── MODULE_03_SEAL_RECORD.md     (new)
│   ... (repeat for 01, 04-10)
│   ├── IMPLEMENTATION_STATUS.md     ← Update status here
│   ├── VOLUME_1_PART_2_ENHANCED_KERNEL_REBUILD.md      (new)
│   └── VOLUME_1_PART_3_ENHANCED_FOUNDATION_COMPLETION.md (this file)
└── .github/workflows/
    └── ci.yml                       ← CI automation
```

---

## SUMMARY

1. **Start:** Module 02 already SEALED ✅
2. **Confirm:** Module 05 kernel → CI pass ✅
3. **Migrate:** Module 03 → 06 → 07 → 09 → 01 → 04 → 08 → 10 (6–8 hours per module)
4. **Integrate:** Module 00 (final; 2–3 hours)
5. **Seal:** Achieve Seal 5 (formal review + sign-off)
6. **Release:** Unblock Modules 11–19

**Total estimated time:** 60–80 hours (2 weeks at 30 hrs/week)

---

## SIGN-OFF

| Role | Name | Status | Date |
|------|------|--------|------|
| Lead Architect | Keletso R. Mosidila | ✅ Ready | 2026-09-15 |
| Implementation Lead | (TBD) | 🔲 Pending | — |
| Independent Reviewer | (TBD) | 🔲 Pending | — |
| Release Gate | (TBD) | 🔲 Pending | — |

---

**End of Part 3 (Enhanced)**
