#!/usr/bin/env python3
"""
SWI V1 — Module 00–10 Extraction and Setup

Extract under Resource Integrity Policy (bounded). Does NOT authorize SWI.
PROVEN=NO SEALED=NO AUTHORIZED=NO PRODUCTION_AUTHORIZED=NO
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

try:
    from security.archive_integrity import (
        ACCEPTED_WITHIN_POLICY,
        ResourceLimits,
        extract_zip_bounded,
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from security.archive_integrity import (
        ACCEPTED_WITHIN_POLICY,
        ResourceLimits,
        extract_zip_bounded,
    )

SCRIPT_DIR = Path(__file__).resolve().parent

DEFAULT_ARCHIVES = [
    SCRIPT_DIR / "swi_v1_part1_source.zip",
    SCRIPT_DIR / "SWI_v1_part1_source.zip",
    SCRIPT_DIR / "SWI_V1_Part1_Source.zip",
    SCRIPT_DIR / "swi_v1_part1_source.ZIP",
]

REQUIRED_FILES = [
    "README.md",
    "SETUP_GUIDE.md",
    "INSTALLATION.md",
    "requirements.txt",
    ".env.example",
    "config/swi_config.yaml",
    "swi_core/__init__.py",
    "swi_core/module00_trainer.py",
    "swi_core/module01_node_scanner.py",
    "swi_core/module02_security_probe.py",
    "swi_core/module03_context_sync.py",
    "swi_core/module04_encryption_handler.py",
    "swi_core/module05_redaction_engine.py",
    "swi_core/module06_drift_analyzer.py",
    "swi_core/module07_memory_validator.py",
    "swi_core/module08_access_auth.py",
    "swi_core/module09_audit_logger.py",
    "swi_core/module10_external_sandbox.py",
    "test_swi_core.py",
]

OPTIONAL_ROOT_FILES = ["LICENSE"]


def info(message: str) -> None:
    print(f"[INFO] {message}")


def success(message: str) -> None:
    print(f"[PASS] {message}")


def warning(message: str) -> None:
    print(f"[WARN] {message}")


def error(message: str) -> None:
    print(f"[ERROR] {message}")


def section(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract, normalise, verify, and test SWI Modules 00–10."
    )
    parser.add_argument("archive", nargs="?", type=Path)
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("--no-extract", action="store_true")
    return parser.parse_args()


def find_archive(argument: Path | None) -> Path | None:
    if argument is not None:
        candidate = argument.expanduser()
        if not candidate.is_absolute():
            candidate = SCRIPT_DIR / candidate
        candidate = candidate.resolve()
        if not candidate.is_file():
            error(f"ZIP archive not found: {candidate}")
            return None
        if candidate.suffix.lower() != ".zip":
            error(f"Supplied file is not a ZIP archive: {candidate}")
            return None
        return candidate
    for candidate in DEFAULT_ARCHIVES:
        if candidate.is_file():
            return candidate
    return None


def inspect_archive(archive: Path) -> bool:
    info(f"Inspecting archive: {archive}")
    try:
        with zipfile.ZipFile(archive, "r") as zip_file:
            names = zip_file.namelist()
    except zipfile.BadZipFile:
        error("The supplied file is not a valid ZIP archive.")
        return False
    except OSError as exc:
        error(f"Could not read the archive: {exc}")
        return False
    if not names:
        error("The ZIP archive is empty.")
        return False
    success(f"Archive contains {len(names)} entries.")
    return True


def is_safe_zip_member(member_name: str) -> bool:
    try:
        root = SCRIPT_DIR.resolve()
        target = (SCRIPT_DIR / member_name).resolve()
        target.relative_to(root)
    except (OSError, ValueError):
        return False
    return True


def validate_archive_paths(archive: Path) -> bool:
    try:
        with zipfile.ZipFile(archive, "r") as zip_file:
            unsafe = [n for n in zip_file.namelist() if not is_safe_zip_member(n)]
    except (zipfile.BadZipFile, OSError) as exc:
        error(f"Could not inspect archive paths: {exc}")
        return False
    if unsafe:
        error("Unsafe ZIP paths detected. Extraction stopped.")
        for name in unsafe[:10]:
            print(f"       - {name}")
        return False
    success("Archive paths passed safety validation.")
    return True


def extract_archive(archive: Path) -> bool:
    """Extract under Resource Integrity Policy — no ZipFile.extractall()."""
    section("EXTRACTING SOURCE")
    if not validate_archive_paths(archive):
        return False
    info("Extracting SWI source archive (bounded resource policy)...")
    staging = SCRIPT_DIR / ".tmp_swi_extract"
    if staging.exists():
        shutil.rmtree(staging, ignore_errors=True)
    limits = ResourceLimits(
        max_compressed_bytes=50 * 1024 * 1024,
        max_entry_expanded_bytes=25 * 1024 * 1024,
        max_cumulative_expanded_bytes=100 * 1024 * 1024,
        max_entries=5000,
        max_nesting_depth=0,
        max_seconds=120.0,
    )
    result = extract_zip_bounded(archive, staging, limits=limits)
    if result.outcome != ACCEPTED_WITHIN_POLICY:
        error(f"Bounded extraction rejected: {result.outcome} — {result.reason}")
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        return False
    try:
        for item in staging.iterdir():
            target = SCRIPT_DIR / item.name
            if item.is_dir():
                if not target.exists():
                    shutil.move(str(item), str(target))
                else:
                    for child in item.rglob("*"):
                        rel = child.relative_to(item)
                        dest = target / rel
                        if child.is_dir():
                            dest.mkdir(parents=True, exist_ok=True)
                        elif not dest.exists():
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(child), str(dest))
            elif not target.exists():
                shutil.move(str(item), str(target))
    except OSError as exc:
        error(f"Staging promotion failed: {exc}")
        return False
    finally:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
    success("Archive extracted under resource policy. AUTHORIZED=NO")
    return normalise_extracted_layout()


def find_directory(name: str) -> Path | None:
    direct = SCRIPT_DIR / name
    if direct.is_dir():
        return direct
    try:
        matches = [
            p for p in SCRIPT_DIR.rglob(name)
            if p.is_dir() and ".git" not in p.parts
        ]
    except OSError:
        return None
    return matches[0] if matches else None


def find_file(name: str) -> Path | None:
    direct = SCRIPT_DIR / name
    if direct.is_file():
        return direct
    try:
        matches = [
            p for p in SCRIPT_DIR.rglob(name)
            if p.is_file() and ".git" not in p.parts
        ]
    except OSError:
        return None
    return matches[0] if matches else None


def relative_to_script(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(SCRIPT_DIR.resolve()))
    except ValueError:
        return str(path)


def move_to_root(source: Path, destination: Path) -> bool:
    try:
        source_resolved = source.resolve()
        destination_resolved = destination.resolve()
    except OSError as exc:
        error(f"Could not resolve path: {exc}")
        return False
    if source_resolved == destination_resolved:
        return True
    if destination.exists():
        warning(f"Destination exists; left untouched: {relative_to_script(destination)}")
        return True
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
    except OSError as exc:
        error(f"Could not move {relative_to_script(source)}: {exc}")
        return False
    success(f"Placed: {relative_to_script(destination)}")
    return True


def normalise_extracted_layout() -> bool:
    section("NORMALISING REPOSITORY STRUCTURE")
    swi_core = find_directory("swi_core")
    if swi_core is None:
        error("Could not find swi_core/ after extraction.")
        return False
    root_swi_core = SCRIPT_DIR / "swi_core"
    if swi_core.resolve() != root_swi_core.resolve():
        if not move_to_root(swi_core, root_swi_core):
            return False
    else:
        success("swi_core/ is already in the correct location.")
    test_file = find_file("test_swi_core.py")
    if test_file is None:
        error("test_swi_core.py was not found in the extracted archive.")
        return False
    root_test_file = SCRIPT_DIR / "test_swi_core.py"
    if test_file.resolve() != root_test_file.resolve():
        if not move_to_root(test_file, root_test_file):
            return False
    else:
        success("test_swi_core.py is already in the correct location.")
    for filename in ["README.md", "SETUP_GUIDE.md", "INSTALLATION.md", "requirements.txt", ".env.example", *OPTIONAL_ROOT_FILES]:
        source = find_file(filename)
        if source is None:
            if filename in OPTIONAL_ROOT_FILES:
                continue
            warning(f"{filename} was not found.")
            continue
        destination = SCRIPT_DIR / filename
        if source.resolve() != destination.resolve():
            if not move_to_root(source, destination):
                return False
    config_dir = SCRIPT_DIR / "config"
    try:
        config_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        error(f"Could not create config/: {exc}")
        return False
    config_file = find_file("swi_config.yaml")
    if config_file is None:
        warning("swi_config.yaml was not found.")
    else:
        destination = config_dir / "swi_config.yaml"
        if config_file.resolve() != destination.resolve():
            if not move_to_root(config_file, destination):
                return False
        else:
            success("config/swi_config.yaml is in the correct location.")
    return True


def verify_required_files() -> bool:
    section("VERIFYING REPOSITORY STRUCTURE")
    missing = []
    for relative_path in REQUIRED_FILES:
        path = SCRIPT_DIR / relative_path
        if path.is_file():
            print(f"  [OK]   {relative_path}")
        else:
            print(f"  [MISS] {relative_path}")
            missing.append(relative_path)
    print()
    if missing:
        error(f"{len(missing)} required file(s) are missing.")
        return False
    success("All required files are present.")
    return True


def install_dependencies() -> bool:
    section("INSTALLING DEPENDENCIES")
    requirements = SCRIPT_DIR / "requirements.txt"
    if not requirements.is_file():
        error("requirements.txt was not found.")
        return False
    command = [sys.executable, "-m", "pip", "install", "-r", str(requirements)]
    try:
        result = subprocess.run(command, cwd=SCRIPT_DIR, check=False)
    except OSError as exc:
        error(f"Could not start pip: {exc}")
        return False
    if result.returncode != 0:
        error(f"Dependency installation failed with exit code {result.returncode}.")
        return False
    success("Dependencies installed successfully.")
    return True


def main() -> int:
    args = parse_arguments()
    if not args.no_extract:
        archive = find_archive(args.archive)
        if archive is None:
            warning("No archive found; verifying existing tree only.")
        else:
            if not inspect_archive(archive):
                return 1
            if not extract_archive(archive):
                return 1
    if not verify_required_files():
        return 1
    if args.install:
        if not install_dependencies():
            return 1
    if not args.skip_tests:
        section("RUNNING TESTS")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-q"],
                cwd=SCRIPT_DIR,
                check=False,
            )
        except OSError as exc:
            error(f"Could not run pytest: {exc}")
            return 1
        if result.returncode != 0:
            error(f"Tests failed with exit code {result.returncode}.")
            return 1
        success("Tests completed. AUTHORIZED=NO")
    print("PROVEN=NO SEALED=NO AUTHORIZED=NO PRODUCTION_AUTHORIZED=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
