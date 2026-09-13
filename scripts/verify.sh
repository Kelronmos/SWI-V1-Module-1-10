#!/usr/bin/env bash
set -u
FAILED=0
run_check() {
    NAME="$1"; shift
    echo; echo "======================================"; echo "CHECK: $NAME"; echo "======================================"
    if "$@"; then echo "PASS: $NAME"; else echo "FAIL: $NAME"; FAILED=1; fi
}
run_check "Repository inventory" python scripts/repository_inventory.py
run_check "Documentation structure" python scripts/verify_docs.py
run_check "Claim language review" python scripts/check_claim_language.py
run_check "Tests" python -m pytest -q
run_check "Coverage" python -m pytest --cov=swi_core --cov-report=term-missing -q
echo; echo "======================================"
if [ "$FAILED" -eq 0 ]; then echo "SWI VERIFICATION RESULT: PASS"; exit 0; fi
echo "SWI VERIFICATION RESULT: FAIL"; exit 1
