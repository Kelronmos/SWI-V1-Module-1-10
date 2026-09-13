#!/usr/bin/env python3
"""List repository files for contributors (excludes .git / venv / caches)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORE = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache"}


def main() -> None:
    print("SWI REPOSITORY INVENTORY")
    print("=" * 60)
    for path in sorted(ROOT.rglob("*")):
        if any(part in IGNORE for part in path.parts):
            continue
        relative = path.relative_to(ROOT)
        if path.is_dir():
            print(f"[DIR ] {relative}")
        else:
            print(f"[FILE] {relative}")


if __name__ == "__main__":
    main()
