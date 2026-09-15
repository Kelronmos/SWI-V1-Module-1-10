# SWI MODULES 00–10 — UPGRADE PACKAGE ORIENTATION

**Updated:** Tuesday, 15 September 2026  
**Architect:** Keletso Ronald Mosidila — Trusts Motion, Botswana  
**Canonical path:** `docs/` only (root copies are redirects)

---

## Repository truth (do not use the old “Module 03 NEXT” order)

| Module | Status |
|--------|--------|
| **02** Security Probe | **SEALED** |
| **03** Context Sync | **SEALED** |
| **05** Redaction | **SEALED** (structured PII only) |
| **06** Drift Analyzer | **KERNEL-ENFORCED** · local tests passed · **CI seal pending** |
| **00** Trainer | Halt on M02/M03/M05/**M06**; **not** foundation-sealed |
| **01, 04, 07, 08, 09, 10** | Implemented · not kernel-migrated |

### Correct migration order

```text
02 SEALED ✅ → 03 SEALED ✅ → 05 SEALED ✅ → 06 KERNEL (seal after CI)
    → 07 → 09 → 01 → 04 → 08 → 10 → 00 final integration → SEAL 5 → 11–19
```

**Do not** re-migrate Module 03. **Next engineering gate:** confirm M06 CI → seal M06 → inspect Module 07.

---

## Package files (all under `docs/`)

| Document | Purpose |
|----------|---------|
| `docs/PACKAGE_INDEX.md` | Index + status corrections |
| `docs/SWI_00-10_DELIVERY_SUMMARY.md` | Delivery overview |
| `docs/VOLUME_1_PART_3_ENHANCED_FOUNDATION_COMPLETION_MANUAL.md` | Enhanced Part 3 |
| `docs/VOLUME_1_PART_3_FOUNDATION_COMPLETION_MANUAL.md` | Existing foundation manual |
| `docs/MODULE_INTEGRATION_DEPENDENCY_MATRIX.md` | Integration / halt graph |
| `docs/MODULE_00_TRAINER_*.md` | Trainer prep (**not** sealed) |
| `docs/MODULE_02_SEAL_RECORD.md` etc. | Existing seal/evidence records |
| `docs/SWI_00-10_UPGRADE_MANIFEST.md` | Manifest |

---

## Verify

```bash
python -m pip install -r requirements.txt
python -m pytest -q
./scripts/verify.sh
```

## Claims discipline

SEALED = bounded enforcement evidence — **not** complete security, semantic understanding, or universal AI safety.
