# SWI 00–10 Delivery Summary (location-corrected)

**Canonical path:** `docs/SWI_00-10_DELIVERY_SUMMARY.md`  
Root file is a redirect only.

## Status

- M02, M03, M05: **SEALED**
- M06: **KERNEL-ENFORCED** (await CI before seal)
- M00: orchestration + halt; not foundation-sealed
- Next: **Module 07 inspection** after M06 seal — **not** Module 03

## Install / verify

```bash
pip install -r requirements.txt
python -m pytest -q
./scripts/verify.sh
```

## Doc map

See `docs/00_READ_ME_FIRST.md` and `docs/PACKAGE_INDEX.md`.
