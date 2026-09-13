#!/usr/bin/env python3
"""Check that required foundation documentation files exist."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "docs/START_HERE.md",
    "docs/IMPLEMENTATION_STATUS.md",
    "docs/EVIDENCE_MATRIX.md",
    "docs/KNOWN_LIMITATIONS.md",
    "docs/TESTING_AND_VERIFICATION.md",
    "docs/VOLUME_1_PART_2_MODULE_KERNEL_REBUILD_MANUAL.md",
    "docs/FOUNDATION_MILESTONE.md",
    "docs/MODULE_05_KERNEL_MIGRATION.md",
    "docs/MODULE_05_EVIDENCE.md",
    "docs/MODULE_05_SEAL_RECORD.md",
    "docs/VOLUME_1_PART_3_FOUNDATION_COMPLETION_MANUAL.md",
]


def main() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        print("Missing documentation:")
        for path in missing:
            print(f" - {path}")
        raise SystemExit(1)
    print("Documentation structure: PASS")


if __name__ == "__main__":
    main()
