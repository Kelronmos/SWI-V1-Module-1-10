# Security Maze V1 Formation Path Inventory

**Machine-readable source:** `docs/formation_path_inventory.json`  
**Loader / discovery:** `swi_core/formation_path_inventory.py`  
**Tests:** `test/adversarial/test_security_maze_path_closure.py`

## Status

| Field | Value |
|-------|--------|
| Construction | PATH-CLOSURE LAYER |
| Universal Gate | **NOT PROVEN** |
| Security Maze Seal | **NOT READY** |
| Foundation Seal 5 | **NOT READY** |

## Contract

```text
FORMATION PATH → DISCOVER → CLASSIFY → PRIVILEGE?
  → MAZE REQUIRED? → TEST / EXPLICIT CLASS → EVIDENCE → REPLAY → STATUS
```

**Forbidden closed combination (enforced in tests):**

```text
privileged = true
maze_required = true
maze_protected = false
status = TESTED     ← illegal as “closed”
```

Open residuals use `status = OPEN`.

**UNKNOWN** must never be treated as PASS.

## Path list (summary)

See JSON for full records. IDs FM-001 … FM-013 cover Trainer, foundation export/sign, Maze, default ModuleKernel, M02–M06 public APIs and constructors.

## Next

Enumerate → classify unknowns → attack → close or keep OPEN → regenerate report.  
Do **not** flip Universal Gate until discovery is trusted and `privileged_unprotected == 0` under a reviewed policy.
