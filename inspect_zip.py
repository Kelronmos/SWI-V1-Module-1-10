#!/usr/bin/env python3
"""Inspect ZIP archive contents and extract under Resource Integrity Policy.

Does NOT authorize, seal, or prove SWI.
PROVEN=NO SEALED=NO AUTHORIZED=NO PRODUCTION_AUTHORIZED=NO
"""
from __future__ import annotations

import sys
from pathlib import Path

from security.archive_integrity import (
    ACCEPTED_WITHIN_POLICY,
    ResourceLimits,
    extract_zip_bounded,
    inspect_zip_bounded,
)


def inspect_zip(zip_path: str | Path) -> bool:
    """List inspection result under policy (no extract)."""
    zip_path = Path(zip_path)
    print(f"\n{'='*70}")
    print(f"INSPECTING (bounded): {zip_path}")
    print(f"{'='*70}\n")

    result = inspect_zip_bounded(zip_path)
    print(f"Outcome: {result.outcome}")
    if result.reason:
        print(f"Reason:  {result.reason}")
    print(f"Entries: {result.entries_seen}")
    print("AUTHORIZED = NO")
    return result.outcome == ACCEPTED_WITHIN_POLICY


def extract_zip(zip_path: str | Path, extract_to: str | Path = ".") -> bool:
    """Extract ZIP under resource and path policy (no extractall)."""
    zip_path = Path(zip_path)
    extract_to = Path(extract_to)
    print(f"\n{'='*70}")
    print(f"EXTRACTING (bounded): {zip_path} -> {extract_to}")
    print(f"{'='*70}\n")

    result = extract_zip_bounded(zip_path, extract_to, limits=ResourceLimits())
    print(f"Outcome: {result.outcome}")
    if result.reason:
        print(f"Reason:  {result.reason}")
    print(f"Bytes written: {result.bytes_written}")
    print(f"Cleanup OK:    {result.cleanup_ok}")
    print("AUTHORIZED = NO")
    return result.outcome == ACCEPTED_WITHIN_POLICY


def find_files(directory: str | Path = ".", max_depth: int = 4) -> None:
    """Recursively list files under directory (read-only display)."""
    directory = Path(directory)
    print(f"\n{'='*70}")
    print(f"STRUCTURE (max depth {max_depth}):")
    print(f"{'='*70}\n")

    for root, dirs, files in os_walk_safe(directory):
        try:
            depth = len(Path(root).relative_to(directory).parts)
        except ValueError:
            continue
        if depth > max_depth:
            dirs.clear()
            continue
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("__pycache__", "node_modules")]
        indent = "  " * depth
        print(f"{indent}{Path(root).name}/")
        subindent = "  " * (depth + 1)
        for file in sorted(files):
            if not file.startswith("."):
                print(f"{subindent}{file}")


def os_walk_safe(directory: Path):
    import os

    return os.walk(directory)


if __name__ == "__main__":
    zip_file = Path("swi_v1_part1_source.zip")
    if not zip_file.is_file():
        print(f"Archive not found: {zip_file}")
        sys.exit(1)

    if inspect_zip(zip_file):
        # Extract to a dedicated subdirectory — never implicit repo root without intent
        dest = Path(".tmp_extract_inspect")
        if extract_zip(zip_file, dest):
            find_files(dest)
            print("\nExtraction finished within policy. AUTHORIZED=NO\n")
            sys.exit(0)
        print("\nExtraction rejected or failed. AUTHORIZED=NO\n")
        sys.exit(1)
    print("\nInspection rejected. AUTHORIZED=NO\n")
    sys.exit(1)
