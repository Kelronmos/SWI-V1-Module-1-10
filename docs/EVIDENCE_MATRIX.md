# Evidence Matrix

| Claim | Evidence | Status |
|-------|----------|--------|
| Trainer multi-module pipeline | `module00_trainer.py` + tests | tested |
| Config YAML / threshold applied | `config_loader` + Trainer tests | tested |
| Explicit timestamp into Context Sync | Trainer + tests | tested |
| SecurityProbe heuristics | `module02_security_probe.py` + tests | tested |
| Module 02 kernel enforcement | `module_kernel.py` + kernel tests | tested (pilot) |
| Invalid block_threshold rejected | Construction `ValueError` + test | tested |
| Oversized input rejected | ModuleKernel pre-check + test | tested |
| Hardened sandbox | — | **not claimed** |
| CEK / Vector Memory / Alita live | — | **not claimed** |
| Modules 11–19 ready | — | **blocked until Seal 5** |
| CI green on GitHub | Actions run history | **verify in UI** |
