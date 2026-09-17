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

---

## 3. NOT CLAIMED

SCAR / ScarStore does **not** establish:

- tamper-proof storage  
- external anchoring (remote append-only log, consensus, HSM)  
- factual truth of remembered content  
- semantic understanding of scars  
- general-purpose AI memory or retrieval intelligence  
- equivalence with V2 M11 (admission / continuity boundary)  
- equivalence with V1 Continuity Lock (`module11_continuity_lock.py`)  
- Firefly memory architecture  
- durable cross-process guarantees unless SQLite path is used **and** still without external anchor  

Integrity root detects silent mutation of **active content hashes in this store**. It is not a global security proof.

---

## 4. Architectural relationship (permitted contracts, not automatic authority)

```text
                    ┌──────────────┐
                    │  GOVERNANCE  │
                    └──────┬───────┘
                           │
                    ┌──────▼──────┐
                    │   EVIDENCE  │
                    │   BOUNDARY  │
                    └──────┬──────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
           SCAR           M11*         REPLAY
             │             │             │
             └─────────────┼─────────────┘
                           │
                    ┌──────▼──────┐
                    │   FIREFLY   │
                    │   MEMORY    │  (design / deferred)
                    └──────┬──────┘
                           │
                     ┌─────▼─────┐
                     │    M12    │  (contract draft / frozen)
                     └───────────┘
```

\* **M11 in this diagram** means the **V2** continuity/admission boundary (`Kelronmos/SWI-V2-Modules-11-22`), not V1 Continuity Lock.

**Rules:**

- SCAR can **contribute** a memory / integrity record.  
- V2 M11 can enforce **its own** admission conditions.  
- Replay can show **reproducibility under a defined configuration**.  
- Firefly (when designed/implemented) may **preserve and relate** records.  
- **None** of these turns a remembered record into factual truth by itself.  
- **Do not replace SCAR with Firefly.** Connect SCAR into a wider memory web without upgrading what SCAR has proven.

---

## 5. Distinction from nearby components

| Component | Role | Not |
|-----------|------|-----|
| **SCAR / ScarStore** | Structured failure records + local integrity | Truth, Firefly, M11 admission |
| **M07** | Hash-chained log + optional Scar integrity check | Durable external ledger |
| **V1 Continuity Lock** | Bounded state tags across turns | Scar store; V2 M11 |
| **V2 M11** | Foundation evidence admission / post-admission seal | ScarStore; Firefly |
| **ReplayGuard (V2)** | Optional in-memory duplicate rejection | Full replay; durable policy |
| **Firefly** | Proposed memory architecture (deferred) | Implemented system |

---

## 6. SCAR → Firefly seam (design frozen)

The consume/refuse boundary is frozen on V2:

**Canonical contract:**  
`Kelronmos/SWI-V2-Modules-11-22` → `docs/SCAR_FIREFLY_ADAPTER_CONTRACT.md`  
**Status:** DESIGN / PROPOSED — not implemented.

**Firefly may consume (when an adapter exists):** identity, class, status, content hash, integrity-root snapshot, provenance fields — without upgrading status labels.

**Firefly must refuse to infer:** factual truth, global tamper-proofing, M11 admission, replay success, or that SCAR supersedes any other layer.

This is **not** authorization to write Firefly code until the implementation gate in that contract is satisfied.

---

## 7. Related documents

- `docs/KNOWN_LIMITATIONS.md`  
- `docs/IMPLEMENTATION_STATUS.md`  
- `swi_core/scar.py` (module docstring)  
- `swi_core/module07_memory_validator.py`  
- V2: `docs/SCAR_FIREFLY_ADAPTER_CONTRACT.md`  
- V2: `docs/V2_MEMORY_WEB_STATUS.md`  
- V2: `docs/M11_SEAL_RECORD.md`  

---

## 8. Freeze rule

Changes that expand SCAR claims beyond this document require:

1. Updated implementation  
2. Tests that assert the new property  
3. Explicit limitation revision  
4. Status language change only after evidence exists  

«Do not claim what the code cannot demonstrate.»
