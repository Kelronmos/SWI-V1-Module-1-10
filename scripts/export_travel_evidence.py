#!/usr/bin/env python3
"""Export FoundationEvidenceEnvelope JSON for two-checkout travel tests.

Run from a V1 checkout with PYTHONPATH=. or installed package layout.
Does not require V2.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

# Allow running from repo root without install
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from swi_core.foundation_evidence import envelope_to_dict, export_foundation_evidence  # noqa: E402
from swi_core.module00_trainer import Trainer  # noqa: E402


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

    with tempfile.TemporaryDirectory() as td:
        trainer = Trainer(str(Path(td) / "audit.log"))
        result = trainer.process(args.text)
        env = export_foundation_evidence(result, evidence_id=args.evidence_id)
        payload = envelope_to_dict(env)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")), encoding="utf-8")
    print(f"EXPORTED {out} evidence_id={args.evidence_id} integrity={payload['integrity_reference'][:16]}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
