# Two-Checkout CI Travel Test Plan

**Status:** PLAN + producer script · **not** CI-verified until Actions runs green on both tips  
**Date:** 15 September 2026

## Goal

Prove:

> A **clean V1 checkout** can produce serialized foundation evidence that a **separate clean V2 checkout** admits via M11 — with no shared process, no `import` of V1 into V2, and no ambient state.

```text
[Checkout A: SWI-V1-Module-1-10]
  Trainer → export_foundation_evidence → JSON file
                    │
                    │  artifact / workspace file
                    ▼
[Checkout B: SWI-V2-Modules-11-22]
  load JSON → M11 → AdmittedInput → Kernel gate
```

## Non-goals

- V2 depending on the V1 Python package
- M10 as handoff
- CRTG / signatures (still DESIGN PENDING)
- Declaring Foundation Seal 5

## Prerequisites

| Item | Requirement |
|------|-------------|
| Python | 3.10+ (match CI matrix when wired) |
| V1 deps | `requirements.txt` in V1 clone |
| V2 deps | `requirements.txt` in V2 clone (`cryptography` ok; not needed for pure JSON admit) |
| Isolation | Two directories; delete after run |

## Manual procedure (developer machine)

```bash
ROOT=$(mktemp -d)
git clone --depth 1 https://github.com/Kelronmos/SWI-V1-Module-1-10.git "$ROOT/v1"
git clone --depth 1 https://github.com/Kelronmos/SWI-V2-Modules-11-22.git "$ROOT/v2"

python3 -m venv "$ROOT/venv-v1" && "$ROOT/venv-v1/bin/pip" install -q -r "$ROOT/v1/requirements.txt"
python3 -m venv "$ROOT/venv-v2" && "$ROOT/venv-v2/bin/pip" install -q -r "$ROOT/v2/requirements.txt"

# Produce
"$ROOT/venv-v1/bin/python" "$ROOT/v1/scripts/export_travel_evidence.py" \
  --out "$ROOT/evidence.json"

# Consume (must exit 0)
"$ROOT/venv-v2/bin/python" "$ROOT/v2/scripts/admit_travel_evidence.py" \
  --in "$ROOT/evidence.json"

# Negative: tamper then expect non-zero
python3 -c "import json;p='$ROOT/evidence.json';d=json.load(open(p));d['payload']['allowed']=not d['payload']['allowed'];json.dump(d,open(p,'w'))"
"$ROOT/venv-v2/bin/python" "$ROOT/v2/scripts/admit_travel_evidence.py" --in "$ROOT/evidence.json" \
  && exit 1 || true

echo "TWO_CHECKOUT_TRAVEL: PASS (local)"
```

Use `scripts/run_two_checkout_travel.sh` when both repos are siblings, or the CI workflow below.

## CI design (recommended)

### Option A — V2 workflow checks out V1 (preferred for admit-side proof)

Workflow on **V2** repo:

1. Checkout V2 (self)
2. Checkout V1 into `../SWI-V1-Module-1-10` or `vendor/v1` path (read-only)
3. Setup Python × matrix (3.10, 3.11, 3.12)
4. `pip install -r requirements.txt` (V2) and V1 requirements in a second venv **or** sequential venvs
5. Run V1 `scripts/export_travel_evidence.py` → `evidence.json` (artifact)
6. Run V2 `scripts/admit_travel_evidence.py --in evidence.json` → must exit 0
7. Mutate payload in evidence.json → admit must exit non-zero
8. Upload `evidence.json` as CI artifact (unsigned; not a secret)

### Option B — V1 workflow produces artifact; V2 workflow downloads

Harder without shared artifacts across private/public repos; Option A is simpler.

### CI pass criteria

| Check | Expected |
|-------|----------|
| Export succeeds | exit 0, valid JSON |
| Admit valid | exit 0, prints ADMITTED |
| Admit after payload tamper | exit ≠ 0 |
| Admit after integrity field wipe | exit ≠ 0 |
| No `import swi_core` / `import swi_v2` from the other tree in admit path | grep / review |

## Evidence record template

```text
TWO_CHECKOUT_TRAVEL_RESULT
Date:
V1 commit:
V2 commit:
Python:
Export: PASS/FAIL
Admit valid: PASS/FAIL
Admit tampered: PASS/FAIL (must fail closed)
CI run URL:
Status: LOCAL_ONLY | CI_VERIFIED
```

Until CI_VERIFIED: report **LIVE TWO-CHECKOUT — PENDING**.

## Attack cases (minimum)

1. Valid V1 export → ACCEPT  
2. Corrupted payload → REJECT  
3. Wrong integrity_reference → REJECT  
4. Missing field → REJECT  
5. Unsupported schema version → REJECT  
6. Invalid verification_status → REJECT  
7. Raw non-envelope JSON → REJECT  

## Relation to Seal 5

This plan is **necessary** for Foundation Bridge strength; it is **not sufficient** alone for Seal 5 (M07/M09/M00, adversarial suite, claim audit still required).
