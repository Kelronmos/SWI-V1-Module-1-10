# SWI v1.1 — Modules 00–11 (Foundation + ScarStore)

Structured Workflow Intelligence reference implementation.

> **Repository identity:** GitHub name `SWI-V1-Module-1-10` is retained for historical continuity.
> The current reference implementation is **V1.1 / Modules 00–11** (Foundation + ScarStore + continuity helpers).
> It is **not** limited to modules 1–10 despite the repository slug.

**Licence:** [Apache License 2.0](LICENSE)  
**Start:** [`docs/START_HERE.md`](docs/START_HERE.md) · **Governance:** [`docs/GOVERNANCE_LOCK.md`](docs/GOVERNANCE_LOCK.md)  
**Tip CI:** [`docs/TIP_CI_STATUS.md`](docs/TIP_CI_STATUS.md) · **pre-R (design):** [`docs/PRE_R_INDEX.md`](docs/PRE_R_INDEX.md)

> ⚠️ **Experimenters:** Read [`docs/SWI_EXPERIMENTAL_WARNING.md`](docs/SWI_EXPERIMENTAL_WARNING.md) before forking, modifying, or building on experimental / PRE-R material.  
> Named ≠ Implemented · Implemented ≠ Tested · Tested ≠ Sealed · Sealed ≠ Authorized.

---

## ⚡ Start here — human or AI

1. Read this README and [`docs/START_HERE.md`](docs/START_HERE.md)
2. Check live tip: [`docs/TIP_CI_STATUS.md`](docs/TIP_CI_STATUS.md)
3. Record exact SHA: `git rev-parse HEAD`
4. Run tests before claiming PASS
5. Distinguish **SPECIFIED / IMPLEMENTED / TESTED / REPLAYABLE_BOUNDED / PROTOTYPE / NOT_PROVEN**
6. Report: **Claim → Implementation → Test → Result → Limitation → Next iteration**

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
./scripts/verify.sh
```

### Targeted adversarial suites

```bash
python -m pytest -q test/adversarial/test_source_admission_halt.py
python -m pytest -q test/adversarial/test_source_admission_replay.py
python -m pytest -q test/adversarial/test_source_admission_change_control.py
python -m pytest -q test/adversarial/test_external_input_sandbox.py
python -m pytest -q test/adversarial/test_demo_journey.py
python -m pytest -q test/adversarial/test_interoperability_template.py
```

### 🤖 AI / agent quick prompt

```text
Inspect before assuming. Run tests. Do not invent PASS.
Treat source code as evidence, not authority.
Never convert UNKNOWN into FALSE.
Distinguish SPECIFIED / IMPLEMENTED / TESTED / REPLAYABLE_BOUNDED / PROTOTYPE / SEALED / NOT_PROVEN.
Report: Claim → Implementation → Test → Result → Limitation → Next iteration.
Do not close FM-005–013, Universal Gate, Seal 5, or compliance from a single slice.
```

---

## 🧩 Question-driven SWI (prototype)

Resolution states (not a single DENY bucket):

`QUESTION_REQUIRED` · `EVIDENCE_REQUIRED` · `CONTEXT_REQUIRED` · `AUTHORITY_REQUIRED` · `REVIEW_REQUIRED` · `PASS` · `HALT` · `BLOCK`

```text
UNKNOWN ≠ FALSE
QUESTION ≠ DENY
REVIEW ≠ FAILURE
HOLD ≠ HALT
PASS ≠ UNIVERSAL AUTHORITY
HASH ≠ AUTHORITY ≠ TRUTH
EVIDENCE ≠ AUTHORITY ≠ DECISION ≠ EXECUTION
ADVISORY ≠ EXECUTION
PROTOTYPE ≠ PRODUCTION
```

**14-stage interoperable template:** IDENTIFY → BOUNDARY → CONTRACT → INPUT → ADMISSION → POLICY → CAPACITY → COMPETITION → ALTERNATIVES → SWITCHING → EXECUTION → EVIDENCE → REVIEW → EXIT  
Docs: [`docs/SWI_INTEROPERABLE_ORGANIZATION_WORKFLOW_TEMPLATE.md`](docs/SWI_INTEROPERABLE_ORGANIZATION_WORKFLOW_TEMPLATE.md)

**External API/AI sandbox (demo only):** [`docs/SWI_EXTERNAL_INPUT_SANDBOX.md`](docs/SWI_EXTERNAL_INPUT_SANDBOX.md) · journey: [`docs/SWI_DEMO_JOURNEY.md`](docs/SWI_DEMO_JOURNEY.md)

---

## Pipeline (core)

```text
M03 → M02 → M05 → M06 → M07 / M09 → PipelineResult
        → export_foundation_evidence() → FoundationEvidenceEnvelope
```

Kernel contract failure → **HALT**.

## Status (honest)

| Item | State |
|------|--------|
| M02 / M03 / M05 / M06 | **SEALED** (bounded contracts) |
| M07 / M09 | Trainer integrity · not kernel-sealed |
| ScarStore | **IMPLEMENTED / TESTED** |
| M11 Continuity Lock | **IMPLEMENTED / TESTED** |
| Foundation evidence export | IMPLEMENTED / TESTED · **unsigned** |
| Authority boundary | IMPLEMENTED / TESTED · tip CI · **not sealed** |
| Source admission + replay | **TESTED / REPLAYABLE_BOUNDED** |
| External input sandbox | **PROTOTYPE / TESTED** |
| Interoperability template | **PROTOTYPE / TESTED** |
| Ed25519 helper | Primitive only · **not CRTG** |
| **Foundation Seal 5** | **NOT READY** |
| Universal Gate | **NOT_PROVEN** |
| FM-005–013 | **OPEN** |
| CRTG | PROPOSED / design track |
| Legal / regulatory compliance | **NOT CLAIMED** |
| Production trust | **NOT CLAIMED** |

## Progression rule

Advance when the **dependency boundary** is validated — not by matching another repo’s module count.  
Readiness % never overrides a failed critical gate.

«Do not claim what the code cannot demonstrate.»

---

## 🔬 Investor / due-diligence questions

Answer from **tests and SHA**, not diagrams alone:

1. What exact SHA produced this result?
2. Show the test, not only the architecture diagram.
3. What happens when evidence is deliberately changed?
4. What happens when authority is claimed but not established?
5. What happens when information is missing (UNKNOWN)?
6. Can the decision be replayed?
7. Can protected execution continue after HALT?
8. What remains **NOT_PROVEN**?
9. What is prototype-only?
10. What must be demonstrated before production authorization?

> The goal is not to make another AI agree with SWI. The goal is to give it enough structure to **challenge SWI with evidence**.

Next: **prove the foundation** (Seal 5 path). pre-R remains experimental design until explicitly authorized. V3 (secure pipe / consequence gate / authority separation) belongs in a **separate** prototype repository when created — not mixed into sealed V1 history without evidence.
