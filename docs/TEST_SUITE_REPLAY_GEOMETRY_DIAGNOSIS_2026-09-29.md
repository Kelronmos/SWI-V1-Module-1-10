# SWI V1 — Test Suite / Replay / Geometry Diagnosis & Report

**Report date:** 2026-09-29  
**Live tip at report time:** see `docs/TIP_CI_STATUS.md`  
**Canonical inventory:** `docs/formation_path_inventory.json`

> Named ≠ Implemented · Implemented ≠ Tested · Tested ≠ Sealed · Sealed ≠ Authorized.

---

## 1. Test suite geometry (current structure)

| Location | Role | Notes |
|----------|------|-------|
| `test/` | Primary suite (unit + kernel + adversarial) | Main body |
| `test/adversarial/` | Hostile / boundary / maze / admission attacks | Strongest evidence layer |
| `tests/` | Secondary (schema, scar, continuity, adversarial contracts) | Smaller |
| `test_swi_core.py` | Legacy flat suite (historical 27 tests) | Still present |
| `replay/` | Manifests only | **Scaffold only — not executable replay engine** |
| `evidence/` | Evidence artefacts | Present |
| `pytest.ini` | Collects `tests` + `test` | Markers: unit, contract, adversarial, m00_m10 |

**Replay status:**  
`replay/manifests/` and `replay/swi-v47/` exist as documentation/scaffold.  
There is **no implemented, tested, replayable decision engine** that can take a recorded admission/halt decision, re-execute the same checks, and prove identical outcome under the same evidence hash.  
→ **Replay = NAMED / PARTIAL SCAFFOLD, not IMPLEMENTED / TESTED.**

---

## 2. Formation-path geometry (canonical)

| Path | Status | Meaning |
|------|--------|---------|
| FM-001 – FM-004 | **TESTED** | Trainer, export/sign, SecurityMaze front door protected |
| FM-005 | **OPEN** | `ModuleKernel.run` default `require_admission=False` |
| FM-006 | **OPEN** | `SecurityProbe.scan` unadmitted → forms output |
| FM-007 | **OPEN** | `ContextSync.record_turn` unadmitted → mutates |
| FM-008 | **OPEN** | `RedactionEngine.redact` unadmitted → forms output |
| FM-009 | **OPEN** | `DriftAnalyzer.check` unadmitted → forms result |
| FM-010 – FM-013 | **OPEN** | Constructor residuals (default kernel False) |

**Universal Gate:** NOT_PROVEN  
**Security Maze V1:** NOT SEALED / NOT_READY  
**Foundation Seal 5:** NOT READY  
**Legal/regulatory compliance:** NOT CLAIMED

This geometry is deliberately asymmetric: several privileged paths are gated; several direct/compatibility paths remain open. The inventory correctly records this instead of papering over it.

---

## 3. Diagnosis — what the suite actually proves today

**Proven / TESTED (within scope):**
- Admission required at Trainer.process and foundation export/sign paths
- Security Maze state-machine and several adversarial attacks
- Cryptographic evidence artefact integrity (hash / canonicalization) — **bounded**
- Authority non-escalation (reject laundering of `verified` / `trusted` / `replay_verified` flags)
- Several kernel halt behaviours under controlled conditions
- ScarStore and Module 11 continuity lock (implemented/tested)

**Explicitly OPEN / not proven:**
- Universal path closure (FM-005–013 still form output without maze authority)
- Durable, executable **replay** of admission/halt decisions
- External Source Admission (privacy + open-source licence + architecture HALT) — not present at report time
- Execution-side effect blocking under real adapters (synthetic only in places)
- Any claim that CI pass = Universal Gate proven
- Any legal/regulatory compliance conclusion

**Historical contamination risk (mitigated 2026-09-29):**
- `test_run_log.txt` and old TIP_CI_STATUS correctly marked historical
- TIP_CI_STATUS repaired so auditors no longer see the wrong tip SHA

---

## 4. Required update sequence (honest order)

```
1. SPECIFY   External Source Admission Policy (privacy + OSS + architecture)
2. IMPLEMENT Data models + decision + HALT enforcement (no silent PASS)
3. TEST      New adversarial tests (violation → HALT → zero side-effect)
4. REPLAY    Record → revalidate → same decision under same evidence hash
5. PROVE     Only after tests + replay evidence exist for the bounded scope
6. GEOMETRY  Update formation_path_inventory + TIP_CI_STATUS only after evidence
7. REPORT    Status document that separates SPECIFIED / IMPLEMENTED / TESTED
```

Skipping steps (especially claiming PROVEN or SEALED before replay + side-effect proof) would violate the project’s own discipline.

---

## 5. Immediate actionable items

| Priority | Action | Status after action |
|----------|--------|---------------------|
| P0 | Keep TIP_CI_STATUS aligned with live tip | Done (2026-09-29) |
| P1 | Add `docs/SWI_EXTERNAL_SOURCE_ADMISSION_POLICY.md` | SPECIFIED |
| P2 | Add minimal `swi_core/source_admission/` models + decision + halt | IMPLEMENTED |
| P3 | Add adversarial tests (violation → HALT, zero side-effect) | TESTED (bounded) |
| P4 | Add replay of one recorded HALT decision | REPLAYABLE (bounded) |
| P5 | Update formation inventory only if new paths closed with evidence | Geometry honest |
| P6 | Publish this diagnosis/report | This document |

---

## 6. Report conclusion

- Documentation tip metadata is correct as of this report.
- Test suite is substantial and adversarial in places, but **does not close the Universal Gate**.
- Replay is scaffold only — not yet an executable, tested capability.
- Formation geometry correctly shows FM-005–013 OPEN.
- Privacy + open-source licence HALT boundary is specified in a companion policy document; implementation and tests remain future work.
- No legal/regulatory compliance is claimed — correctly.

**This document does not flip any FM status, does not claim Universal Gate PROVEN, and does not claim Foundation Seal 5 READY.**
