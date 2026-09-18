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

- not tamper-proof storage  
- external anchoring  
- factual truth of remembered content  
- not semantic understanding of scars  
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

Permitted contracts only; no automatic authority. See V2 SCAR/Firefly index for deferred design.

---

## 5. Distinction from nearby components

| Component | Role | Not |
|-----------|------|-----|
| **SCAR / ScarStore** | Structured failure records + local integrity | Truth, Firefly, M11 admission |
| **M07** | In-process hash-chain memory validator | Durable disk log (that is M09) |
| **M09** | Disk-backed audit log | SCAR store |
| **Continuity Lock** | Bounded state tags | SCAR lessons |

---

## 6. Status freeze

Do not expand SCAR claims without: contract → tests → CI → limitations update.
