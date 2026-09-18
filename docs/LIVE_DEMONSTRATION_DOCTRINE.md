# Live Demonstration Doctrine

**Date:** 18 September 2026  
**Rule:** Volumes teach. The repository proves.  
**Status:** Governing orientation (not a module seal)

---

## What we are building

SWI turns **learning** (architecture volumes, manuals, exercises) into **live,
working demonstration**: code you can clone, run, test, and challenge.

```text
Volume / manual (intent, pedagogy, history)
        ↓
Implementation in this repository
        ↓
Automated tests
        ↓
CI on a recorded tip
        ↓
Documented limitations
        ↓
LIVE DEMONSTRATION (bounded)
```

A chapter in a volume is **not** a live demonstration until the matching
path exists here and passes tests.

---

## Governing chain

```text
Claim → Implementation → Test → Result → Limitation → Next iteration
```

| Phrase | Meaning here |
|--------|----------------|
| **Tamper-evident** | Alteration can be detected by a verification step — **not** tamper-proof |
| **Tested** | An automated test exercises the claim and passes |
| **SEALED** | Declared acceptance criteria for a **specific** contract/version were met and recorded |
| **Live demo** | Clone → install → pytest (and/or script) reproduces the behaviour on a known SHA |

```text
TESTED ≠ CI-VERIFIED ≠ AUDITED ≠ SEALED ≠ “system is safe”
```

---

## What is live in this repository (V1)

| Area | Live path | How to demonstrate |
|------|-----------|--------------------|
| Foundation pipeline | M03 → M02 → M05 → M06 (+ M07/M09 on path as implemented) | `Trainer.process` + `pytest` |
| Kernel halt | ModuleKernel + Trainer halt reasons | `test/test_trainer_kernel_halt.py` |
| Foundation evidence export | `foundation_evidence.py` + travel script | `scripts/export_travel_evidence.py` |
| Continuity Lock (M11-style state hash) | `module11_continuity_lock.py` | package tests where present |
| Authority boundary (Lane A) | `swi_core/authority.py` | `test/test_authority_non_escalation.py` |
| Structured module input schema | `schemas/m00_m10_schema.json` | `tests/test_m00_m10_schema.py` (needs `jsonschema`) |

**Honest status examples:** M02/M03/M05 sealed under their recorded contracts;
M06 kernel-enforced with CI seal discipline as documented in `START_HERE.md`.

---

## What Volume Part 2 describes (not automatically live here)

Volume 1 Part 2 manuals describe Continuity Lock, Semantic Scrubber, Agentic
Loop, Summarization, Identity Graph, Access Control as **tested reference
designs**. In **this** GitHub tree:

| Module (volume numbering) | In this repo |
|---------------------------|--------------|
| Continuity Lock | Partial — `module11_continuity_lock.py` present |
| Semantic Scrubber (13) | **Not** present as `module13_*` on tip |
| Agentic Loop (14) | **Not** present as `module14_*` on tip |
| Summarization (15/21) | **Not** present as `module15_*` on tip |
| Identity graph (18) | **Not** present as `module18_*` on tip |
| Access control RBAC (19) | **Not** present as `module19_*` on tip |

Do **not** treat the volume PDF/DOCX alone as proof those modules run in this
clone. Promoting a volume chapter to a live demo requires: implement → test →
CI → limitations — same chain as foundation modules.

V2 (`SWI-V2-Modules-11-22`) holds M11 admission, travel CI, authority boundary
CI record, and controlled M12+ gates — separate checkout, serialized evidence
only.

---

## How to run a live demonstration (minimum)

```bash
git clone https://github.com/Kelronmos/SWI-V1-Module-1-10.git
cd SWI-V1-Module-1-10
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
# optional:
./scripts/verify.sh
PYTHONPATH=. python scripts/export_travel_evidence.py --out /tmp/evidence.json
```

Record: **commit SHA**, **pytest result**, **date**. That package is the demo
evidence — not a screenshot of a manual cover.

---

## Authority layers (do not collapse)

```text
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
```

Information may cross a boundary without authority crossing that boundary.
See `docs/AUTHORITY_BOUNDARY_MODEL.md`.

---

## Volume 2 / advanced manuals

SAD-DFU, vector memory, anticipatory ethics, sovereign mesh, and similar
Volume 2 themes remain **design / hypothesis** unless and until this org’s
repositories implement, test, and limit them under the same chain. Cover art
and comprehensive manuals are **not** live demos.

---

## Next iteration (engineering, not prose)

1. Keep foundation seals and travel evidence reproducible on tip.  
2. Lane B — canonicalization (deterministic bytes → stable digest).  
3. Only then promote additional Part 2 modules into this tree with tests.  
4. Never mark SEALED from documentation volume text alone.

**Remember:** we are not building a library of unread claims. We are building
**reproducible demonstrations** of bounded workflow intelligence — structure
first, evidence always, authority by contract, HALT when the next step is not
established.
