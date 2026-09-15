#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${PYTHONPATH:-}:$ROOT"

run_check() {
  local name="$1"
  shift
  echo "==> $name"
  "$@"
}

run_check "Python syntax (compileall)" python -m compileall -q swi_core
run_check "Documentation structure" python scripts/verify_docs.py
run_check "Claim language review" python scripts/check_claim_language.py
run_check "Repository inventory" python scripts/repository_inventory.py
run_check "ModuleKernel unit tests" python -m pytest -q test/test_module_kernel.py
run_check "Module 02 kernel tests" python -m pytest -q test/test_security_probe_kernel.py
run_check "Module 03 kernel tests" python -m pytest -q test/test_context_sync_kernel.py
run_check "Module 06 kernel tests" python -m pytest -q test/test_drift_kernel.py
run_check "Module 05 kernel tests" python -m pytest -q test/test_redaction_kernel.py
run_check "Trainer Module 05 halt" python -m pytest -q test/test_trainer_module05_halt.py
run_check "Module 05 adversarial" python -m pytest -q test/adversarial/test_redaction_boundaries.py
run_check "Trainer persistence integrity" python -m pytest -q test/test_trainer_persistence_integrity.py
run_check "Full pytest suite" python -m pytest -q
echo "VERIFY: PASS"
