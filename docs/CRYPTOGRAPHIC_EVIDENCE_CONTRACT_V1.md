# SWI V1 Cryptographic Evidence Contract

**Contract:** `canonicalization_v0`  
**Implementation:** `swi_core/evidence_artifact.py` (Steps 126–150 boundary)  
**Baseline foundation:** `13d0d433ceb1203c81871ca0c4dbebada59b1f4b`  
**Status:** IMPLEMENTED / TESTED (bounded)

---

## Pipeline

```text
canonicalization_v0 → SHA-256 → optional maze link → optional Ed25519 → artifact
```

No second SHA-256 helper, canonicalizer, or evidence-artifact class.

---

## Evidence artifact authority boundary

| Question | Answered by `verify_fm_evidence_artifact`? |
|----------|--------------------------------------------|
| Does `evidence_hash` match material under `canonicalization_v0`? | **Yes** |
| Was the event factually true? | **No** |
| Was the actor authorized / maze authority granted? | **No** |
| Is the formation path closed / sealed? | **No** |
| Is Universal Gate proven? | **No** |
| Is the law / regulation satisfied? | **No** |

### What `evidence_hash` proves

Artifact integrity: covered fields match the stored digest under `canonicalization_v0`.  
Material **excludes** `evidence_hash` and `signature`.

### Why `signature: null` is legitimate

Signatures are optional binding. Absence does not invalidate integrity.

### Why a valid signature does not close an FM path

Path status is governed by `docs/formation_path_inventory.json` + enforcement tests — not by crypto fields.

### Why FM-005…009 remain OPEN

Attack artifacts record observations (`privileged_operation_performed` may be true) while `maze_authority_granted` stays false and inventory status stays **OPEN** until architecture boundary work lands.

### Why Universal Gate remains NOT_PROVEN

Integrity of observations ≠ coverage of every privileged formation path.

```text
Evidence integrity:  artifact hash matches material
Evidence authority:  NOT PROVIDED BY THIS ARTIFACT
Path closure:        NOT PROVIDED BY THIS ARTIFACT
Legal compliance:    NOT PROVIDED BY THIS ARTIFACT
```

---

## Status freeze (Steps 126–150 do not change)

| Item | Status |
|------|--------|
| Security Maze | PARTIAL / NOT SEALED |
| FM-005…009 | OPEN |
| Universal Gate | NOT_PROVEN |
| Foundation Seal 5 | NOT_READY |
| CRTG / production keys / HSM | NOT_IMPLEMENTED |
