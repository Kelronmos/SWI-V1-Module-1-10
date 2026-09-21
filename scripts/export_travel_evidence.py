#!/usr/bin/env python3
"""Export FoundationEvidenceEnvelope JSON for two-checkout travel tests.

Run from a V1 checkout with PYTHONPATH=. or installed package layout.
Does not require V2.

Requires valid admission for:
  - Trainer.process (module 00)
  - export_foundation_evidence (foundation_export)

Uses test-only admission helpers — not production authority.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from swi_core.foundation_evidence import envelope_to_dict, export_foundation_evidence  # noqa: E402
from swi_core.module00_trainer import Trainer  # noqa: E402
from swi_test_helpers.admission import export_admission, pipeline_admission  # noqa: E402


def _git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=_ROOT, text=True
        ).strip()
    except Exception:
        return "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", required=True, help="Output JSON path")
    p.add_argument(
        "--text",
        default="two-checkout travel sample contact@example.com",
        help="Input text for Trainer.process",
    )
    p.add_argument("--evidence-id", default="v1-two-checkout-travel-001")
    args = p.parse_args()

    commit = _git_head()
    train_adm = pipeline_admission(commit=commit, module="00")
    export_adm = export_admission(commit=commit)

    with tempfile.TemporaryDirectory() as td:
        trainer = Trainer(str(Path(td) / "audit.log"))
        result = trainer.process(args.text, admission=train_adm)
        env = export_foundation_evidence(
            result,
            admission=export_adm,
            expected_commit=commit,
            evidence_id=args.evidence_id,
        )
        payload = envelope_to_dict(env)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")), encoding="utf-8")
    print(
        f"EXPORTED {out} evidence_id={args.evidence_id} "
        f"integrity={payload['integrity_reference'][:16]}... commit={commit[:12]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
