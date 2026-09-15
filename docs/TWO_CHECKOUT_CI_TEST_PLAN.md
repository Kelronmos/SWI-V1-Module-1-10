# Two-Checkout CI Travel Test Plan

**Status:** PLAN + producer script · CI_VERIFIED only when V2 Actions is green  

## V2 CI shape (preferred)

Implemented on V2 as **two jobs**:

1. **produce** — checkout V1 only → `export_travel_evidence.py` → artifact `evidence.json`  
2. **admit** — checkout V2 only → download artifact → assert `import swi_core` fails → admit → reject tampers

See V2: `.github/workflows/two_checkout_travel.yml`

## Producer (this repo)

```bash
PYTHONPATH=. python scripts/export_travel_evidence.py --out evidence.json
```

## Seal language

Two-checkout green is required for M11 seal **eligibility** on V2; it does not auto-seal M11 and does not complete Foundation Seal 5.

Until V2 tip is green: **LIVE TWO-CHECKOUT — PENDING**
