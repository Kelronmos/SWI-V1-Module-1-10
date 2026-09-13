#!/usr/bin/env bash
# SWI foundation verification — evidence-oriented report
set -u
FAILED=0

run_check() {
    NAME="$1"
    shift
    echo
    echo "======================================"
    echo "CHECK: $NAME"
    echo "======================================"
    if "$@"; then
        echo "PASS: $NAME"
    else
        echo "FAIL: $NAME"
        FAILED=1
    fi
}

echo "SWI Verification — Modules 00–10 foundation"
echo "==========================================="
echo "Labels: PASS = this check passed here."
echo "        Absence of a row does not prove the capability."
echo

run_check "Repository inventory" python scripts/repository_inventory.py
run_check "Documentation structure" python scripts/verify_docs.py
run_check "Claim language review" python scripts/check_claim_language.py
run_check "Module Kernel unit tests" python -m pytest -q test/test_module_kernel.py
run_check "Module 02 kernel pilot tests" python -m pytest -q test/test_security_probe_kernel.py
run_check "Module 02 boundary/adversarial" python -m pytest -q test/adversarial/test_security_probe_boundaries.py
run_check "Trainer↔02 boundary seal" python -m pytest -q test/test_trainer_kernel_halt.py
run_check "Module 05 kernel tests" python -m pytest -q test/test_redaction_kernel.py
run_check "Trainer↔05 boundary seal" python -m pytest -q test/test_trainer_module05_halt.py
run_check "Module 05 adversarial" python -m pytest -q test/adversarial/test_redaction_boundaries.py
run_check "Trainer config tests" python -m pytest -q test/test_trainer_config.py
run_check "Full suite" python -m pytest -q
run_check "Coverage (swi_core)" python -m pytest --cov=swi_core --cov-report=term-missing -q

echo
echo "======================================"
echo "What this report does NOT prove:"
echo "  - Modules 03–04, 06–10 kernel migration"
echo "  - Universal prompt-injection detection"
echo "  - Complete PII detection"
echo "  - CEK / SAD-DFU / Vector Memory / Sovereign Mesh"
echo "  - Seal 5 (independent rebuild + challenge)"
echo "======================================"

if [ "$FAILED" -eq 0 ]; then
    echo "SWI VERIFICATION RESULT: PASS (foundation checks in this run)"
    exit 0
fi
echo "SWI VERIFICATION RESULT: FAIL"
exit 1
