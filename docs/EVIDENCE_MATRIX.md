# Evidence Matrix

| Claim | Evidence | Status |
|-------|----------|--------|
| Trainer runs multi-module pipeline | `swi_core/module00_trainer.py` + `test_swi_core.py` | tested |
| Config YAML / path / threshold applied | `config_loader` + Trainer + config tests | tested |
| Explicit timestamp into Context Sync | Trainer `process(..., timestamp=)` + tests | tested |
| SecurityProbe heuristic detection | `module02_security_probe.py` + tests | tested |
| Module 02 pre/post kernel enforcement | `module_kernel.py` + `test_module_kernel.py` + `test_security_probe_kernel.py` | tested (pilot) |
| Invalid block_threshold rejected | Construction `ValueError` + test | tested |
| Oversized input rejected | ModuleKernel pre-check + test | tested |
| Memory / audit hash linkage | modules 07/09 + existing tests | tested (tamper-evident) |
| Hardened sandbox | — | **not claimed** |
| CEK / Vector Memory / Alita live | — | **not claimed** |
| Modules 11–19 ready | — | **blocked until Seal 5** |
| CI green on GitHub | Actions run history | **verify in UI** |
