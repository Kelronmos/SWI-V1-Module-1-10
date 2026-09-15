#!/usr/bin/env bash
# Two-checkout travel: requires V1 and V2 clones as siblings or via env.
# Usage:
#   V1_ROOT=../SWI-V1-Module-1-10 V2_ROOT=../SWI-V2-Modules-11-22 ./scripts/run_two_checkout_travel.sh
# Or from a parent directory that contains both clones.
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
V1_ROOT=${V1_ROOT:-$(cd "$SCRIPT_DIR/.." && pwd)}
V2_ROOT=${V2_ROOT:-$(cd "$V1_ROOT/../SWI-V2-Modules-11-22" && pwd)}

if [[ ! -f "$V1_ROOT/scripts/export_travel_evidence.py" ]]; then
  echo "V1 export script missing under $V1_ROOT" >&2
  exit 2
fi
if [[ ! -f "$V2_ROOT/scripts/admit_travel_evidence.py" ]]; then
  echo "V2 admit script missing under $V2_ROOT — clone V2 or set V2_ROOT" >&2
  exit 2
fi

WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT
EVIDENCE="$WORKDIR/evidence.json"

python3 -m venv "$WORKDIR/v1venv"
# shellcheck disable=SC1091
source "$WORKDIR/v1venv/bin/activate"
pip install -q -r "$V1_ROOT/requirements.txt"
PYTHONPATH="$V1_ROOT" python "$V1_ROOT/scripts/export_travel_evidence.py" --out "$EVIDENCE"
deactivate

python3 -m venv "$WORKDIR/v2venv"
# shellcheck disable=SC1091
source "$WORKDIR/v2venv/bin/activate"
pip install -q -r "$V2_ROOT/requirements.txt"
PYTHONPATH="$V2_ROOT" python "$V2_ROOT/scripts/admit_travel_evidence.py" --in "$EVIDENCE"

# Tamper
python -c "import json; p='$EVIDENCE'; d=json.load(open(p)); d['payload']=dict(d['payload']); d['payload']['allowed']=not d['payload'].get('allowed', True); json.dump(d, open(p,'w'))"
if PYTHONPATH="$V2_ROOT" python "$V2_ROOT/scripts/admit_travel_evidence.py" --in "$EVIDENCE"; then
  echo "FAIL: tampered evidence was admitted" >&2
  exit 1
fi
echo "TWO_CHECKOUT_TRAVEL: PASS (tamper rejected)"
