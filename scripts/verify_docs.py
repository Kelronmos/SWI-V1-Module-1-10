#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "docs/START_HERE.md",
    "docs/IMPLEMENTATION_STATUS.md",
    "docs/EVIDENCE_MATRIX.md",
    "docs/KNOWN_LIMITATIONS.md",
    "docs/PACKAGE_INDEX.md",
    "docs/00_READ_ME_FIRST.md",
    "docs/MODULE_02_SEAL_RECORD.md",
    "docs/MODULE_03_SEAL_RECORD.md",
    "docs/MODULE_05_SEAL_RECORD.md",
    "docs/MODULE_06_SEAL_RECORD.md",
    "docs/MODULE_06_INSPECTION.md",
    "docs/MODULE_06_DECISION.md",
    "docs/MODULE_06_MIGRATION.md",
    "docs/VOLUME_1_PART_3_FOUNDATION_COMPLETION_MANUAL.md",
    "docs/VOLUME_1_PART_3_ENHANCED_FOUNDATION_COMPLETION_MANUAL.md",
    "docs/MODULE_INTEGRATION_DEPENDENCY_MATRIX.md",
    "docs/MODULE_00_TRAINER_SEAL_RECORD.md",
    "docs/SWI_00-10_DELIVERY_SUMMARY.md",
    "docs/SWI_00-10_UPGRADE_MANIFEST.md",
]


def main() -> None:
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    if missing:
        print("Missing documentation:")
        for p in missing:
            print(f" - {p}")
        raise SystemExit(1)
    print("Documentation structure: PASS")


if __name__ == "__main__":
    main()
