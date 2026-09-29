#!/usr/bin/env python3
"""Bounded code-mutation pilot for swi_core/interoperability/evaluate.py.

Prefer mutmut when available. This script is a fallback for high-value hand mutants.
Does not claim Security Maze seal or Universal Gate.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "swi_core" / "interoperability" / "evaluate.py"

MUTANTS = [
    (
        "C01",
        "missing stages → PASS",
        "state=ResolutionState.QUESTION_REQUIRED,\n            questions=[f\"Missing stages: {', '.join(missing)}\"],",
        "state=ResolutionState.PASS,\n            questions=[f\"Missing stages: {', '.join(missing)}\"],",
    ),
    (
        "C02",
        "None alternatives → PASS",
        "if tpl.alternative_providers_known is None:\n        return EvaluationResult(\n            state=ResolutionState.QUESTION_REQUIRED,",
        "if tpl.alternative_providers_known is None:\n        return EvaluationResult(\n            state=ResolutionState.PASS,",
    ),
    (
        "C03",
        "market BLOCK → PASS",
        "if tpl.market_allocation_requested:\n        return EvaluationResult(\n            state=ResolutionState.BLOCK,",
        "if tpl.market_allocation_requested:\n        return EvaluationResult(\n            state=ResolutionState.PASS,",
    ),
    (
        "C04",
        "AUTHORITY_REQUIRED → PASS",
        "if tpl.real_world_execution_declared and not tpl.authority_available:\n        return EvaluationResult(\n            state=ResolutionState.AUTHORITY_REQUIRED,",
        "if tpl.real_world_execution_declared and not tpl.authority_available:\n        return EvaluationResult(\n            state=ResolutionState.PASS,",
    ),
    (
        "C05",
        "switching REVIEW → PASS",
        "if tpl.switching_path_known is False:\n        return EvaluationResult(\n            state=ResolutionState.REVIEW_REQUIRED,",
        "if tpl.switching_path_known is False:\n        return EvaluationResult(\n            state=ResolutionState.PASS,",
    ),
]


def run_tests() -> int:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    r = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "test/adversarial/test_interoperability_template.py",
            "test/adversarial/test_interoperability_mutation_replay.py",
            "--tb=no",
        ],
        cwd=str(ROOT),
        env=env,
    )
    return r.returncode


def main() -> int:
    orig = SRC.read_text(encoding="utf-8")
    print("BASELINE", run_tests())
    killed = survived = 0
    try:
        for mid, desc, old, new in MUTANTS:
            if old not in orig:
                print(mid, "INCONCLUSIVE pattern_not_found")
                continue
            SRC.write_text(orig.replace(old, new, 1), encoding="utf-8")
            code = run_tests()
            if code != 0:
                killed += 1
                print(mid, "KILLED", desc)
            else:
                survived += 1
                print(mid, "SURVIVED", desc)
            SRC.write_text(orig, encoding="utf-8")
    finally:
        SRC.write_text(orig, encoding="utf-8")
    print(f"killed={killed} survived={survived}")
    print("Security Maze: NOT_READY | Universal Gate: NOT_PROVEN")
    return 0 if survived == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
