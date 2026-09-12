#!/usr/bin/env python3
"""
SWI V1 — Module 00–10 Extraction and Setup

Purpose
-------
Extract the currently reproducible SWI Modules 00–10 reference
implementation, normalise the repository layout, verify required files,
optionally install dependencies, and run the actual automated tests.

This script does NOT claim to reconstruct the complete SWI architecture.

Expected repository structure
----------------------------

    SWI-V1-Module-1-10/
    ├── README.md
    ├── SETUP_GUIDE.md
    ├── INSTALLATION.md
    ├── requirements.txt
    ├── .env.example
    ├── config/
    │   └── swi_config.yaml
    ├── swi_core/
    │   ├── __init__.py
    │   ├── module00_trainer.py
    │   ├── module01_node_scanner.py
    │   ├── module02_security_probe.py
    │   ├── module03_context_sync.py
    │   ├── module04_encryption_handler.py
    │   ├── module05_redaction_engine.py
    │   ├── module06_drift_analyzer.py
    │   ├── module07_memory_validator.py
    │   ├── module08_access_auth.py
    │   ├── module09_audit_logger.py
    │   └── module10_external_sandbox.py
    └── test_swi_core.py

Usage
-----

    python3 extract_and_setup.py

    python3 extract_and_setup.py archive.zip

    python3 extract_and_setup.py --install

    python3 extract_and_setup.py --install archive.zip

    python3 extract_and_setup.py archive.zip --install

    python3 extract_and_setup.py --skip-tests

Exit status
-----------

    0 = successful verification
    1 = verification/setup/test failure
    2 = invalid command-line usage
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


# ============================================================================
# CONFIGURATION
# ============================================================================

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

OPTIONAL_ROOT_FILES = [
    "LICENSE",
]


# ============================================================================
# OUTPUT HELPERS
# ============================================================================

def info(message: str) -> None:
    """Print an informational message."""
    print(f"[INFO] {message}")


def success(message: str) -> None:
    """Print a successful operation message."""
    print(f"[PASS] {message}")


def warning(message: str) -> None:
    """Print a warning message."""
    print(f"[WARN] {message}")


def error(message: str) -> None:
    """Print an error message."""
    print(f"[ERROR] {message}")


def section(title: str) -> None:
    """Print a section heading."""
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


# ============================================================================
# COMMAND-LINE ARGUMENTS
# ============================================================================

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Extract, normalise, verify, and test the SWI "
            "Modules 00–10 reference implementation."
        )
    )

    parser.add_argument(
        "archive",
        nargs="?",
        type=Path,
        help=(
            "Optional source ZIP archive. If omitted, known archive "
            "names are searched in the repository root."
        ),
    )

    parser.add_argument(
        "--install",
        action="store_true",
        help="Install dependencies from requirements.txt before testing.",
    )

    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip pytest execution after structural verification.",
    )

    parser.add_argument(
        "--no-extract",
        action="store_true",
        help=(
            "Do not extract an archive. Verify the existing repository "
            "structure and optionally run tests."
        ),
    )

    return parser.parse_args()


# ============================================================================
# ARCHIVE DISCOVERY
# ============================================================================

def find_archive(argument: Path | None) -> Path | None:
    """
    Locate the source ZIP archive.

    If an explicit archive path is supplied, it takes precedence.

    Otherwise the known archive names in the repository root are checked.
    """

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


# ============================================================================
# ARCHIVE INSPECTION
# ============================================================================

def inspect_archive(archive: Path) -> bool:
    """Confirm that the source file is a readable, non-empty ZIP archive."""

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

    indicators = [
        "swi_core",
        "test_swi_core.py",
        "module00_trainer.py",
        "module10_external_sandbox.py",
    ]

    found = []

    for indicator in indicators:
        if any(indicator in name for name in names):
            found.append(indicator)

    if found:
        info("Detected implementation content:")

        for item in found:
            print(f"       - {item}")
    else:
        warning(
            "The archive does not appear to contain the expected "
            "SWI implementation paths."
        )

    return True


# ============================================================================
# ZIP PATH SAFETY
# ============================================================================

def is_safe_zip_member(member_name: str) -> bool:
    """
    Check that a ZIP member cannot escape the repository directory.

    This prevents paths such as:

        ../../outside_file

    from being extracted outside the repository.
    """

    try:
        root = SCRIPT_DIR.resolve()
        target = (SCRIPT_DIR / member_name).resolve()

        target.relative_to(root)

    except (OSError, ValueError):
        return False

    return True


def validate_archive_paths(archive: Path) -> bool:
    """Validate every ZIP member before extraction."""

    try:
        with zipfile.ZipFile(archive, "r") as zip_file:
            unsafe = [
                name
                for name in zip_file.namelist()
                if not is_safe_zip_member(name)
            ]

    except (zipfile.BadZipFile, OSError) as exc:
        error(f"Could not inspect archive paths: {exc}")
        return False

    if unsafe:
        error("Unsafe ZIP paths detected. Extraction stopped.")

        for name in unsafe[:10]:
            print(f"       - {name}")

        if len(unsafe) > 10:
            print(f"       ... and {len(unsafe) - 10} more")

        return False

    success("Archive paths passed safety validation.")
    return True


# ============================================================================
# ARCHIVE EXTRACTION
# ============================================================================

def extract_archive(archive: Path) -> bool:
    """Extract the source archive into the repository directory."""

    section("EXTRACTING SOURCE")

    if not validate_archive_paths(archive):
        return False

    info("Extracting SWI source archive...")

    try:
        with zipfile.ZipFile(archive, "r") as zip_file:
            zip_file.extractall(SCRIPT_DIR)

    except (zipfile.BadZipFile, OSError) as exc:
        error(f"Extraction failed: {exc}")
        return False

    success("Archive extracted.")

    return normalise_extracted_layout()


# ============================================================================
# FILE / DIRECTORY SEARCH
# ============================================================================

def find_directory(name: str) -> Path | None:
    """
    Find a directory below the repository root.

    The .git directory is excluded.
    """

    direct = SCRIPT_DIR / name

    if direct.is_dir():
        return direct

    try:
        matches = [
            path
            for path in SCRIPT_DIR.rglob(name)
            if path.is_dir() and ".git" not in path.parts
        ]

    except OSError:
        return None

    return matches[0] if matches else None


def find_file(name: str) -> Path | None:
    """
    Find a file below the repository root.

    The .git directory is excluded.
    """

    direct = SCRIPT_DIR / name

    if direct.is_file():
        return direct

    try:
        matches = [
            path
            for path in SCRIPT_DIR.rglob(name)
            if path.is_file() and ".git" not in path.parts
        ]

    except OSError:
        return None

    return matches[0] if matches else None


# ============================================================================
# PATH NORMALISATION
# ============================================================================

def relative_to_script(path: Path) -> str:
    """Return a readable path relative to the repository root."""

    try:
        return str(path.resolve().relative_to(SCRIPT_DIR.resolve()))
    except ValueError:
        return str(path)


def move_to_root(source: Path, destination: Path) -> bool:
    """
    Move an extracted file or directory to the expected location.

    Existing destinations are deliberately left untouched.
    """

    try:
        source_resolved = source.resolve()
        destination_resolved = destination.resolve()

    except OSError as exc:
        error(f"Could not resolve path: {exc}")
        return False

    if source_resolved == destination_resolved:
        return True

    if destination.exists():
        warning(
            "Destination already exists; leaving existing path untouched: "
            f"{relative_to_script(destination)}"
        )
        return True

    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))

    except OSError as exc:
        error(
            f"Could not move {relative_to_script(source)}: {exc}"
        )
        return False

    success(f"Placed: {relative_to_script(destination)}")

    return True


def normalise_extracted_layout() -> bool:
    """
    Normalise the extracted archive into the current repository structure.

    Important:

        swi_core/

    is the current implementation directory.

    The obsolete:

        src/

    structure is not recreated.
    """

    section("NORMALISING REPOSITORY STRUCTURE")

    # ------------------------------------------------------------------
    # swi_core/
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # test_swi_core.py
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Root documentation/configuration files
    # ------------------------------------------------------------------

    root_files = [
        "README.md",
        "SETUP_GUIDE.md",
        "INSTALLATION.md",
        "requirements.txt",
        ".env.example",
        *OPTIONAL_ROOT_FILES,
    ]

    for filename in root_files:
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

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

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
            success(
                "config/swi_config.yaml is in the correct location."
            )

    return True


# ============================================================================
# REPOSITORY STRUCTURE VERIFICATION
# ============================================================================

def verify_required_files() -> bool:
    """Verify that all required repository files exist."""

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

        for item in missing:
            print(f"       - {item}")

        return False

    success(
        "All required implementation, test, configuration, "
        "and documentation files are present."
    )

    return True


# ============================================================================
# DEPENDENCY INSTALLATION
# ============================================================================

def install_dependencies() -> bool:
    """
    Install dependencies from requirements.txt.

    This is performed only when --install is supplied.
    """

    section("INSTALLING DEPENDENCIES")

    requirements = SCRIPT_DIR / "requirements.txt"

    if not requirements.is_file():
        error("requirements.txt was not found.")
        return False

    info("Installing Python dependencies...")

    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-r",
        str(requirements),
    ]

    try:
        result = subprocess.run(
            command,
            cwd=SCRIPT_DIR,
            check=False,
        )

    except OSError as exc:
        error(f"Could not start pip: {exc}")
        return False

    if result.returncode != 0:
        error(
            "Dependency installation failed with exit code "
            f"{result.returncode}."
        )
        return False

    success("Dependencies installed successfully.")

    return True


# ============================================================================
# PYTEST AVAILABILITY
# ============================================================================

def check_pytest_available() -> bool:
    """Check whether pytest is available in the current environment."""

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "--version",
            ],
            cwd=SCRIPT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

    except OSError as exc:
        error(f"Could not check pytest: {exc}")
        return False

    if result.returncode != 0:
        warning(
            "pytest is not available in the current Python environment."
        )
        return False

    version = result.stdout.strip()

    if version:
        info(version)

    return True


# ============================================================================
# TEST EXECUTION
# ============================================================================

def run_tests() -> bool:
    """
    Run the actual SWI automated test suite.

    PASS means pytest returned exit code 0.

    FAIL means pytest returned a non-zero exit code.

    No result is fabricated.
    """

    section("RUNNING AUTOMATED TESTS")

    test_file = SCRIPT_DIR / "test_swi_core.py"

    if not test_file.is_file():
        error("test_swi_core.py does not exist.")
        return False

    if not check_pytest_available():
        error(
            "pytest is unavailable. "
            "Install dependencies or run with --install."
        )
        return False

    command = [
        sys.executable,
        "-m",
        "pytest",
        "test_swi_core.py",
        "-v",
        "--tb=short",
    ]

    info("Executing:")
    print("       " + " ".join(command))

    try:
        result = subprocess.run(
            command,
            cwd=SCRIPT_DIR,
            check=False,
        )

    except OSError as exc:
        error(f"Could not start pytest: {exc}")
        return False

    print()

    if result.returncode == 0:
        success("pytest completed successfully.")
        return True

    error(
        f"pytest failed with exit code {result.returncode}."
    )

    return False


# ============================================================================
# LOG DIRECTORY
# ============================================================================

def ensure_logs_directory() -> bool:
    """Create the logs directory used by the reference pipeline."""

    logs_dir = SCRIPT_DIR / "logs"

    try:
        logs_dir.mkdir(parents=True, exist_ok=True)

    except OSError as exc:
        error(f"Could not create logs/: {exc}")
        return False

    success("logs/ directory is available.")

    return True


# ============================================================================
# PYTHON SOURCE COMPILE CHECK
# ============================================================================

def compile_source() -> bool:
    """
    Compile the SWI Python source files without executing them.

    This catches syntax errors independently of pytest.
    """

    section("PYTHON SOURCE COMPILE CHECK")

    source_files = sorted(
        (SCRIPT_DIR / "swi_core").glob("*.py")
    )

    if not source_files:
        error("No Python source files found in swi_core/.")
        return False

    command = [
        sys.executable,
        "-m",
        "compileall",
        "-q",
        str(SCRIPT_DIR / "swi_core"),
    ]

    try:
        result = subprocess.run(
            command,
            cwd=SCRIPT_DIR,
            check=False,
        )

    except OSError as exc:
        error(f"Could not run compileall: {exc}")
        return False

    if result.returncode != 0:
        error("Python source compilation failed.")
        return False

    success(
        f"Python compilation passed for {len(source_files)} source file(s)."
    )

    return True


# ============================================================================
# SUMMARY
# ============================================================================

def print_summary(
    *,
    structure_ok: bool,
    compile_ok: bool,
    tests_ok: bool | None,
) -> None:
    """Print a final verification summary."""

    section("SWI VERIFICATION SUMMARY")

    print(
        f"  Repository structure : "
        f"{'PASS' if structure_ok else 'FAIL'}"
    )

    print(
        f"  Python compilation   : "
        f"{'PASS' if compile_ok else 'FAIL'}"
    )

    if tests_ok is None:
        print("  Automated tests      : SKIPPED")
    else:
        print(
            f"  Automated tests      : "
            f"{'PASS' if tests_ok else 'FAIL'}"
        )

    print()

    if structure_ok and compile_ok and tests_ok is not False:
        success("SWI setup verification completed successfully.")
    else:
        error("SWI setup verification completed with failures.")


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    """Run the complete setup and verification process."""

    args = parse_arguments()

    section("SWI V1 — MODULE 00–10 SETUP AND VERIFICATION")

    info(f"Repository root: {SCRIPT_DIR}")
    info(f"Python: {sys.executable}")
    info(f"Python version: {sys.version.split()[0]}")

    # ------------------------------------------------------------------
    # Existing repository mode
    # ------------------------------------------------------------------

    if args.no_extract:
        info("Archive extraction disabled (--no-extract).")

        structure_ok = verify_required_files()

        if not structure_ok:
            print_summary(
                structure_ok=False,
                compile_ok=False,
                tests_ok=None,
            )
            return 1

    # ------------------------------------------------------------------
    # Archive mode
    # ------------------------------------------------------------------

    else:
        archive = find_archive(args.archive)

        if archive is None:
            if args.archive is not None:
                error("The supplied archive could not be found.")
                return 1

            warning(
                "No source ZIP was found in the repository root."
            )

            info(
                "If the repository is already extracted, "
                "use --no-extract."
            )

            info(
                "Example: python3 extract_and_setup.py --no-extract"
            )

            return 1

        if not inspect_archive(archive):
            return 1

        if not extract_archive(archive):
            return 1

        structure_ok = verify_required_files()

        if not structure_ok:
            print_summary(
                structure_ok=False,
                compile_ok=False,
                tests_ok=None,
            )
            return 1

    # ------------------------------------------------------------------
    # Compile source
    # ------------------------------------------------------------------

    compile_ok = compile_source()

    if not compile_ok:
        print_summary(
            structure_ok=structure_ok,
            compile_ok=False,
            tests_ok=None,
        )
        return 1

    # ------------------------------------------------------------------
    # Dependencies
    # ------------------------------------------------------------------

    if args.install:
        if not install_dependencies():
            print_summary(
                structure_ok=structure_ok,
                compile_ok=compile_ok,
                tests_ok=None,
            )
            return 1
    else:
        info(
            "Dependency installation not requested. "
            "Use --install if needed."
        )

    # ------------------------------------------------------------------
    # Logs
    # ------------------------------------------------------------------

    if not ensure_logs_directory():
        print_summary(
            structure_ok=structure_ok,
            compile_ok=compile_ok,
            tests_ok=None,
        )
        return 1

    # ------------------------------------------------------------------
    # Tests
    # ------------------------------------------------------------------

    if args.skip_tests:
        warning("Automated tests skipped (--skip-tests).")
        tests_ok = None
    else:
        tests_ok = run_tests()

    # ------------------------------------------------------------------
    # Final result
    # ------------------------------------------------------------------

    print_summary(
        structure_ok=structure_ok,
        compile_ok=compile_ok,
        tests_ok=tests_ok,
    )

    if not structure_ok or not compile_ok:
        return 1

    if tests_ok is False:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
