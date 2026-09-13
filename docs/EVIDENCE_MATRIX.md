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
| Trainer↔02 halt (no silent continue) | `test/test_trainer_kernel_halt.py` | tested |
| Module 02 boundary/adversarial | `test/adversarial/test_security_probe_boundaries.py` | tested (documented limits) |
| Hardened sandbox | — | **not claimed** |
| CEK / Vector Memory / Alita live | — | **not claimed** |
| Modules 11–19 ready | — | **blocked until Seal 5** |
| CI green on GitHub | Actions run history | **verify in UI** |
