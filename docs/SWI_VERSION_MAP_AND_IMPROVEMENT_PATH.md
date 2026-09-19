# SWI Version Map and Improvement Path

**Date:** 2026-09-19  
**Purpose:** Honest inventory of what exists, what does not, and the only safe order of improvement.  
**Rule:** Readiness % never overrides a failed critical gate. No mock, no simulation of security boundaries, no certification language without executable evidence.

---

## 1. What actually exists (public + private)

| Label | Repository / artifact | Language | Role | Sealed / Ready status |
|-------|----------------------|----------|------|------------------------|
| **V1 (public)** | [SWI-V1-Module-1-10](https://github.com/Kelronmos/SWI-V1-Module-1-10) | Python | Foundation + Modules 00–11, ScarStore, evidence export | M02/M03/M05/M06 **SEALED**; Foundation Seal 5 **NOT READY** |
| **V1-Canonical** | SWI-V1-Canonical (private) | — | Restricted development; public sanitised material stays in V1 public | Private; not a public mirror of sensitive controls |
| **V2** | [SWI-V2-Modules-11-22](https://github.com/Kelronmos/SWI-V2-Modules-11-22) | Python | Continuation layer; depends on V1 Foundation Evidence Contract | **M11 SEALED**; M12–22 OPEN / BLOCKED by prior seal |
| **V3** | — | — | **Does not exist** as a public numbered volume | NOT PRESENT |
| **V4** | Historical ZIP / research prototype (2026-06-20) | TypeScript / Node | Research only; crypto SIMULATED; DO_NOT_DEPLOY | RESEARCH_PROTOTYPE only |
| **V5** | — | — | **Does not exist** as a public numbered volume | NOT PRESENT |
| Umbrella | Structured-Workflow-Intelligence | mixed | R&D platform umbrella | Not a sealed volume |
| Other | SWI_V103_API_Foundation, structured-workflow-intelligence-rust, swi-firefly-memory, SWI-Node-Access-Boundary, etc. | Rust / TS / Python | Side experiments / stage demonstrators | Each carries its own limitations; none replace V1/V2 seals |

---

## 2. Lessons that apply to every version

Taken from `docs/V4_LESSONS_AND_EVIDENCE_DISCIPLINE.md` and the live V1/V2 doctrine:

1. **No simulated crypto next to certification language.**  
2. **A mock is not a test.** Planned / Experimental / Mock items are NOT_PROVEN.  
3. **UI is not proof.** Truth Kernel = what survives when the UI is removed.  
4. **Compliance mapping ≠ legal compliance.** Framework references only; legal conclusion = NOT_DETERMINED.  
5. **Rejected request must leave zero formation** and unchanged protected-state / audit hashes where required.  
6. **Tip CI is a hard gate.** Do not expand claims while CI is red.  
7. **Do not invent volume numbers.** Open V3 or V5 only when real modules, tests, and evidence exist.

---

## 3. Improvement path (ordered, evidence-first)

### Phase A — Protect the existing foundation (V1)

```text
A1  Keep tip CI green after every push
A2  Maintain UNIVERSAL_GATE_ENTRYPOINT_MAP.md (already present)
A3  Finish adversarial coverage for every state-forming path
    (missing / wrong module / wrong commit / stale / forged / replay / direct module)
A4  Authority boundary: keep IMPLEMENTED/TESTED; only seal after full evidence
A5  Foundation Seal 5 path — only when prerequisites are green
A6  Packaging / wheel only after installed-wheel re-proves the same security properties
```

### Phase B — Controlled V2 development

```text
B1  M11 remains SEALED; do not reopen
B2  M12 only under controlled gates (claim → implement → test → evidence)
B3  pre-R / bidirectional return remains DESIGN only until AUTHORIZED + adversarial PROVEN
B4  SCAR → Firefly remains policy-frozen / NOT AUTHORIZED until real tests exist
B5  Two-checkout travel CI must stay green for any cross-repo claim
```

### Phase C — Do not fabricate V3 / V5

```text
C1  V3 and V5 do not exist as public volumes today
C2  If a future volume is opened:
      - Start with a clear contract (formation invariant, admission, evidence schema)
      - Implement → test → observe → hash → report
      - Seal only after the same standard used for M02–M06 / M11
C3  Never promote a research ZIP (V4-style) into a numbered volume without stripping all simulated crypto and all certification language
```

### Phase D — V4 material (historical only)

```text
D1  Treat the June 2026 V4 package as a negative example and lesson source only
D2  Do not import its TypeScript tree into V1 or V2 runtime
D3  Do not regenerate its certification PDFs or S9 reports as current evidence
D4  Keep the eight permanent MISTAKE comments in V4_LESSONS_AND_EVIDENCE_DISCIPLINE.md
```

---

## 4. Concrete next actions (executable, no new architecture claims)

1. **V1**  
   - Re-run `python -m pytest -q` and `./scripts/verify.sh` on the current tip.  
   - Confirm GitHub Actions green for commit `2bab827b…` (and any subsequent tip).  
   - Update this map and TIP_CI_STATUS if the tip moves again.

2. **V2**  
   - Keep M11 seal record authoritative.  
   - Any M12 work must land behind explicit tests and evidence receipts.

3. **Cross-cutting**  
   - Any new documentation that mentions “V3”, “V4”, or “V5” must point back to this map.  
   - Any framework mapping (EU AI Act, NIST, UNESCO, Botswana law) remains technical reference only.

---

## 5. Status vocabulary (do not weaken)

| Term | Meaning |
|------|--------|
| PASS | Executable test produced the expected result |
| FAIL | Executable test produced an unexpected result |
| NOT_PROVEN | Insufficient executable evidence for the claim |
| BLOCKED | Prerequisite failure prevents valid verification |
| NOT_APPLICABLE | Explicitly out of scope |
| SEALED | Defined cryptographic + architectural seal procedure succeeded |
| PROPOSED / DESIGN | Exists on paper only; not admitted as verified architecture |

Never use COMPLIANT or CERTIFIED as a test result.

---

This map is documentation. It becomes stronger only when the corresponding tests and receipts exist on the live tips of V1 and V2.
