# MODULE 02 — SECURITY PROBE — SEAL RECORD

| Field | Value |
|-------|--------|
| **STATUS** | **SEALED** |
| **Meaning of SEALED** | Bounded **enforcement** evidence only — **not** complete detection or cybersecurity |

## Seal language (canonical)

> Kernel-enforced heuristic probe; tested contract enforcement and Trainer halt. Detection coverage is **not** complete.

## Two control signals (do not conflate)

| Condition | Pipeline effect |
|-----------|-----------------|
| **Contract failure** (`ModuleKernelError`) | **HALT** — `halted_by_module_02_kernel`; M05/M06 not run |
| **Heuristic risk** (`ProbeResult.blocked`) | **`allowed=False`** — pipeline may still return `PipelineResult`; M06 skipped when blocked |

## Evidence map

| Area | Location |
|------|----------|
| Implementation | `swi_core/module02_security_probe.py` |
| Kernel | `swi_core/module_kernel.py` + scan() pre/post |
| Contract tests | `test/test_security_probe_kernel.py` |
| Adversarial / boundaries | `test/adversarial/test_security_probe_boundaries.py` |
| Trainer halt | `test/test_trainer_kernel_halt.py` |
| Config threshold | `config_loader` + Trainer config tests |
| verify.sh | Module 02 kernel + related steps |

## CI witness (suite includes M02)

M02 implementation landed earlier on main; ongoing independent confirmation is any green full-suite CI that runs pytest + (on 3.12) verify.sh.

| Field | Example witness |
|-------|-----------------|
| Run | [#26](https://github.com/Kelronmos/SWI-V1-Module-1-10/actions/runs/34789422861) (complete tip after M02/M03/M05 kernel path) |
| Later green | [#29](https://github.com/Kelronmos/SWI-V1-Module-1-10/actions/runs/34790281579) on `2247f28` |
| Matrix | Python 3.10 / 3.11 / 3.12 — PASS on cited successful runs |

## Known limitations (not reopen criteria)

- Pattern/heuristic only — paraphrase and novel jailbreaks can miss  
- False positives on legitimate security discussion  
- Threshold/weights not empirically calibrated  
- Not non-bypassable; not universal AI safety  

**Do not** add patterns or change default 0.5 during foundation completion without a new evidence package.

## Foundation

M02 SEALED · M03 SEALED · M05 SEALED · M06 MIGRATE (not executed) · 11–19 BLOCKED
