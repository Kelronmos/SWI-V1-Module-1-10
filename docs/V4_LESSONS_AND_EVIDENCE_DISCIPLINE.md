# V4 Lessons and Evidence-First Discipline Manual

**Status:** Living reference (documentation only)  
**Anchored repository:** https://github.com/Kelronmos/SWI-V1-Module-1-10  
**Date of extraction / write:** 2026-09-19  
**Source of negative lessons:** `swi-v4_-regulated-platform-intelligence (86).zip` (2026-06-20 research prototype)  
**Governing rule (unchanged):**

> A passing test is evidence for the behavior it actually exercises.  
> It is not evidence for untested architecture.

**Hard invariant (must remain true for every production state-forming path):**

```
formation ⇒ valid AdmissionDecision

rejected request:
  formation_count = 0
  Δprotected_state = 0
  Δunauthorized_side_effects = 0
```

---

## 1. What the V4 package actually was

```text
# OBSERVED FACTS (from extracted files, not claims)
- Date stamp: 2026-06-20
- Self-declared status: RESEARCH_PROTOTYPE
- Crypto: SIMULATED_NON_PRODUCTION
- ZK: SIMULATED
- Consensus: NOT_IMPLEMENTED
- Explicit warning: DO_NOT_DEPLOY
- Language: TypeScript / Node / React / PDFs / firefly indexes
- Many “certification” PDFs and S9 reports
- Feature matrix contains “Mock / Research”, “Planned”, “Experimental”
- UI-heavy (dashboards, heatmaps, SecurityMazeGraph, etc.)
- Certification language present while crypto is marked simulated
```

This is **historical research material**. It is not the current V1 Python foundation and must never be treated as sealed or production evidence.

---

## 2. Mistakes extracted from V4 (commented so they stay visible)

```text
# MISTAKE-01: Simulated cryptography presented near certification language
#   V4: crypto = SIMULATED, yet SWI-CERTIFICATION/ folder + S9 reports exist
#   Rule: Never generate or ship a “certification” artifact while any
#         cryptographic primitive is simulated or mocked.

# MISTAKE-02: Mock / Research features listed as if they were progress
#   V4 matrix: “ZK Proofs = Mock / Research”, “Formal Verification = Planned”
#   Rule: A mock is not a test. A planned item is NOT_PROVEN.
#         Do not count it toward readiness or sealing.

# MISTAKE-03: UI and narrative treated as governance proof
#   V4 TRUTH_KERNEL.md correctly warned about decorative layers,
#   yet the package still shipped heavy dashboard and “AI Court” style assets.
#   Rule: If removing the UI breaks the proof, the architecture is inverted.
#         Truth Kernel = only what survives without UI.

# MISTAKE-04: Compliance mapping without executable evidence
#   V4 claimed alignment with ISO 27001 / 42001 / NIST AI RMF
#   while crypto was simulated and many components experimental.
#   Rule: Mapping is reference only. Never write “compliant” or “certified”
#         from a technical test alone.

# MISTAKE-05: Over-claiming in README / PITCH while system_state said RESEARCH_PROTOTYPE
#   Rule: README status table and system-state JSON must agree.
#         If they disagree, the stronger (more conservative) statement wins.

# MISTAKE-06: Private keys / signatures in the tree or generated on the fly
#   Rule: No production private keys in repository.
#         Test keys must be ephemeral and clearly labelled TEST-ONLY.

# MISTAKE-07: Firefly / drift indexes without corresponding adversarial tests
#   Rule: An index file is not evidence. Evidence is a reproducible test
#         that produces the same hash on a clean checkout.

# MISTAKE-08: “Red-Team” tab that runs simulations
#   Rule: Adversarial tests must execute real rejection paths against the
#         real admission boundary. No simulation of the boundary itself.
```

These eight mistakes are permanent comments. They are never deleted; they are only marked “mitigated” after executable evidence exists on the live V1 tip.

---

## 3. Current V1 reality (must be re-checked on every change)

```text
# LIVE ANCHOR (re-verify before any new claim)
Repository : https://github.com/Kelronmos/SWI-V1-Module-1-10
Tip SHA    : f1f6e266d4ac49698369752e4653b9c11e9a2d73   # as of 2026-09-19
Tip CI     : SUCCESS (run 35342332253)
Local suite: 190 passed (Python 3.12, deps installed)

Sealed     : M02, M03, M05, M06 (bounded contracts)
Implemented/Tested : ScarStore, M11 Continuity Lock, foundation evidence export (unsigned)
Not sealed : Authority boundary (CI-green but not sealed)
Not ready  : Foundation Seal 5
Not present: Bidirectional return path, CRTG, production keys

# Source of truth files inside the repo
docs/TIP_CI_STATUS.md
docs/CURRENT_POSITION.md
docs/GOVERNANCE_LOCK.md
```

Any new work starts from this tip, never from the V4 ZIP.

---

## 4. Discipline rules (non-negotiable)

```text
# RULE-A  No mocks, no simulations of security boundaries
#         Real AdmissionDecision objects only.
#         Real rejection before any formation.

# RULE-B  No “certification”, “compliant”, “sealed”, “production-ready”
#         language unless the exact executable evidence exists and is
#         recorded under the current tip SHA.

# RULE-C  Every claim must map to:
#           CLAIM → SOURCE → TEST → OBSERVED RESULT → STATE SNAPSHOT → HASH

# RULE-D  Rejected request must leave:
#           formation_count == 0
#           protected_state_hash unchanged
#           audit_hash unchanged (where ordinary audit mutation is forbidden)
#           callback_count unchanged
#           event_count unchanged

# RULE-E  Test collection failure is release-blocking.
#         ImportError on security primitives must fail loudly.

# RULE-F  Packaging / wheel / PyPI / GitHub Release may only follow
#         after the installed wheel itself re-demonstrates the same
#         security properties.

# RULE-G  Framework mappings (EU AI Act, NIST, UNESCO, Botswana law, etc.)
#         are technical reference only. Legal conclusion = NOT_DETERMINED.
```

---

## 5. Structured learning → fix path (ordered, evidence-first)

```text
Phase 0 — Freeze baseline (do this first, no code change)
  0.1  Record current V1 tip SHA, branch, Python versions, pyproject.toml
  0.2  Save source-tree hash manifest outside the working tree
  0.3  Confirm tip CI is still green
  0.4  Store evidence under evidence/raw/ with timestamps + SHA

Phase 1 — Inventory formation paths (no new claims)
  1.1  Enumerate every production entry that can form state
       (Trainer.process, ModuleKernel.run, M02–M10 direct calls, factories,
        constructors, callbacks, import-time side effects)
  1.2  Mark each: read-only | state-forming | durable-write | audit-write
  1.3  Produce / maintain docs/UNIVERSAL_GATE_ENTRYPOINT_MAP.md
  1.4  Any path not covered remains NOT_PROVEN

Phase 2 — Harden admission (real objects only)
  2.1  Trainer.process: admission keyword-only, no default, no admitted=True
  2.2  Validate before any counter, memory, audit, filesystem, callback
  2.3  Rejection must raise immediately and leave zero formation
  2.4  ModuleKernel default require_admission=True in production paths
  2.5  Compatibility / bypass mode must be test-only and CI-detected

Phase 3 — Adversarial matrix (real rejection, real state snapshots)
  For every formation path run:
    missing admission
    None
    malformed
    wrong module
    wrong commit
    stale
    claim-only authority
    execution_authority=False
    forged / altered artifact / fake signature / fake seal
    replay
    direct kernel / direct module / factory / callback / subclass
  Capture before/after protected-state hash, audit hash, formation_count
  Assert equality on rejection

Phase 4 — Evidence generation (repo-native, no external generator)
  tools/swi_validation/
    evidence.py      # EvidenceReceipt dataclass
    canonical.py     # deterministic JSON + SHA-256
    snapshot.py      # protected / audit / filesystem snapshots
    runner.py        # execute → observe → receipt
    report_json.py / report_csv.py / report_xlsx.py / report_pdf.py
    manifest.py      # SHA256SUMS
  Status values allowed: PASS | FAIL | NOT_PROVEN | BLOCKED | NOT_APPLICABLE
  Never: COMPLIANT | CERTIFIED

Phase 5 — Self-integrity and replay
  5.1  Mutate one byte of any evidence artifact → hash must mismatch
  5.2  Clean checkout of same tip → re-run → semantic hashes must match
  5.3  CI uploads full evidence package; fails on any security-boundary FAIL

Phase 6 — Only after all of the above are green
  6.1  Consider Foundation Seal 5 path
  6.2  Packaging / wheel / release only if installed wheel re-proves the same
  6.3  Update CURRENT_POSITION.md and TIP_CI_STATUS.md with new tip SHA
```

---

## 6. What is explicitly forbidden going forward

```text
# FORBIDDEN
- Shipping any file that claims “certified”, “compliant”, or “sealed”
  while any required test is red or NOT_PROVEN
- Using the V4 TypeScript tree as a runtime dependency of V1
- Generating certification PDFs from simulated crypto
- Counting mock ZK, planned TLA+, or decorative dashboards as evidence
- Letting test helpers become importable production modules
- Silent try/except ImportError around security primitives
- Treating a previous evidence package as authorization for a new run
  (always re-execute the scenario)
```

---

## 7. Immediate next executable steps on the live V1 tip

```bash
# 1. Confirm tip is still the one documented
git clone https://github.com/Kelronmos/SWI-V1-Module-1-10.git
cd SWI-V1-Module-1-10
git rev-parse HEAD   # must match documented tip or update the docs first

# 2. Real test, no mock
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q          # currently 190 passed
./scripts/verify.sh

# 3. Only then begin Phase 1 inventory of formation paths
#    Record results under evidence/ with commit SHA and timestamp
```

---

## 8. Closing statement (to keep the discipline visible)

The V4 ZIP taught the project what **not** to do: simulated crypto beside certification language, mock features counted as progress, UI treated as proof, and compliance claims without executable evidence.

The current V1 repository already encodes the correction:

- Real Python tests  
- Explicit SEALED / NOT READY / NOT IMPLEMENTED language  
- Tip CI as a hard gate  
- Readiness % never overrides a failed critical gate  

Every future change must stay inside that discipline.  
No mock. No simulation of the admission boundary.  
Implement → test → observe → hash → report.  
Only then claim.

---

This document is itself only a map. It becomes evidence only when the corresponding tests and receipts exist on the live tip of https://github.com/Kelronmos/SWI-V1-Module-1-10.
