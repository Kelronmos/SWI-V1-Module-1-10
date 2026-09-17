# SCAR Status — Canonical Boundary

**Repository:** Kelronmos/SWI-V1-Module-1-10  
**Component family:** Scar / ScarStore / M07 scar integrity  
**Status date:** 17 September 2026  
**Authority:** This document freezes claim language for SCAR. Prefer it over informal discussion.

---

## 1. What SCAR is

SCAR is a **bounded memory / integrity record** component in V1.

It stores structured “Scar” records (lessons from failure signatures) with content addressing and an integrity root. It is **not** the whole SWI memory architecture and **not** a truth engine.

---

## 2. IMPLEMENTED / TESTED

| Item | Location |
|------|----------|
| `Scar` data model | `swi_core/scar.py` |
| `ScarStore` (create, list, prune, integrity root) | `swi_core/scar.py` |
| Content hashing | `Scar.compute_content_hash()` |
| Sovereign vs Functional priority | `ScarClass`, `list_active()` ordering |
| Optional SQLite persistence | `ScarStore(db_path=...)` |
| M07 optional ScarStore attach + `scar_integrity` | `swi_core/module07_memory_validator.py` |
| Behavioural tests | `tests/test_scar_store.py` |

Status language for the above: **IMPLEMENTED / TESTED**.  
Not kernel-sealed. Not Foundation Seal 5. Not independently verified as a distributed system.

**Hash coverage (important):** `content_hash` covers only  
`scar_class | title | description | trigger_context | failure_signature | recommended_response | embedding_model`.  
Fields such as `priority_score`, `status`, `tags`, `metadata`, `created_by` are **not** in the hash.  
`content_hash` valid ≠ entire Scar unchanged.

---

## 3. NOT CLAIMED

SCAR / ScarStore does **not** establish:

- tamper-proof storage  
- external anchoring  
- factual truth of remembered content  
- semantic understanding of scars  
- general-purpose AI memory or retrieval intelligence  
- equivalence with V2 M11  
- equivalence with V1 Continuity Lock  
- Firefly memory architecture  
- durable cross-process guarantees without external anchor  

Integrity root detects silent mutation of **active content hashes in this store**. It is not a global security proof.

---

## 4. Architectural relationship

```text
SCAR → (design) Firefly → M11 / Replay / M12
```

Permitted contracts only; no automatic authority. Do not replace SCAR with Firefly.

---

## 5. Distinction from nearby components

| Component | Role | Not |
|-----------|------|-----|
| **SCAR / ScarStore** | Structured failure records + local integrity | Truth, Firefly, M11 admission |
| **M07** | Hash-chained log + optional Scar integrity check | Durable external ledger |
| **V1 Continuity Lock** | Bounded state tags | Scar store; V2 M11 |
| **V2 M11** | Foundation evidence admission | ScarStore; Firefly |
| **Firefly** | Proposed memory architecture (deferred) | Implemented system |

---

## 6. SCAR → Firefly seam (design on V2)

**Entry point:** `Kelronmos/SWI-V2-Modules-11-22` → **`docs/SCAR_FIREFLY_INDEX.md`**

Includes consume/refuse contract, adapter contract, audit, test spec, teaching guides, build manual.  
**Status:** DESIGN FROZEN — **NO IMPLEMENTATION AUTHORIZED.**

---

## 7. Related documents

- `docs/KNOWN_LIMITATIONS.md`  
- `docs/IMPLEMENTATION_STATUS.md`  
- `swi_core/scar.py`  
- V2: `docs/SCAR_FIREFLY_INDEX.md`  
- V2: `docs/V2_MEMORY_WEB_STATUS.md`  
- V2: `docs/M11_SEAL_RECORD.md`  

---

## 8. Freeze rule

Expanding SCAR claims requires: implementation · tests · limitation revision · status language only after evidence.

«Do not claim what the code cannot demonstrate.»
