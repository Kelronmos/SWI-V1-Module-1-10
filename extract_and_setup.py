#!/usr/bin/env python3
"""
SWI V1 — Module 00–10 Extraction and Setup

This utility extracts the SWI reference implementation from the source ZIP,
normalises the repository structure, verifies required files, optionally
installs dependencies, and runs the automated test suite.

Expected implementation layout:

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

The script deliberately does not claim that the complete SWI architecture
has been reconstructed. It only prepares and verifies the currently
reproducible Modules 00–10 implementation.
"""

from __future__ import annotations

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


# ============================================================================
# OUTPUT HELPERS
# ============================================================================

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


# ============================================================================
# ARCHIVE DISCOVERY
# ============================================================================

def find_archive() -> Path | None:
    """
    Find the source ZIP.

    If a path is supplied on the command line, use it.

    Otherwise search the repository root for the known archive names.
    """

    if len(sys.argv) > 1:
        argument = sys.argv[1]

        # Ignore optional flags when looking for an archive.
        if not argument.startswith("-"):
            candidate = Path(argument).expanduser().resolve()

            if candidate.is_file() and candidate.suffix.lower() == ".zip":
                return candidate

            error(f"ZIP archive not found: {candidate}")
            return None

    for candidate in DEFAULT_ARCHIVES:
        if candidate.is_file():
            return candidate

    return None


# ============================================================================
# ARCHIVE INSPECTION
# ============================================================================

def inspect_archive(archive: Path) -> bool:
    """
    Confirm that the source file is a readable ZIP archive.
    """

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
# SAFE PATH VALIDATION
# ============================================================================

def is_safe_zip_member(member_name: str) -> bool:
    """
    Prevent ZIP path traversal.

    A malicious ZIP can contain paths such as:

        ../../some_file

    which could otherwise write outside the repository directory.
    """

    try:
        target = (SCRIPT_DIR / member_name).resolve()
        root = SCRIPT_DIR.resolve()

        target.relative_to(root)
        return True

    except ValueError:
        return False


def validate_archive_paths(archive: Path) -> bool:
    """
    Validate ZIP member paths before extraction.
    """

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
# EXTRACTION
# ============================================================================

def extract_archive(archive: Path) -> bool:
    """
    Extract the archive into the repository directory.
    """

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
# FILE/DIRECTORY SEARCH
# ============================================================================

def find_directory(name: str) -> Path | None:
    """
    Find a directory below the repository root.

    .git is excluded from the search.
    """

    direct = SCRIPT_DIR / name

    if direct.is_dir():
        return direct

    try:
        matches = [
            path
            for path in SCRIPT_DIR.rglob(name)
            if path.is_dir()
            and ".git" not in path.parts
        ]

    except OSError:
        return None

    return matches[0] if matches else None


def find_file(name: str) -> Path | None:
    """
    Find a file below the repository root.

    .git is excluded from the search.
    """

    direct = SCRIPT_DIR / name

    if direct.is_file():
        return direct

    try:
        matches = [
            path
            for path in SCRIPT_DIR.rglob(name)
            if path.is_file()
            and ".git" not in path.parts
        ]

    except OSError:
        return None

    return matches[0] if matches else None


# ============================================================================
# MOVE / NORMALISE
# ============================================================================

def move_to_root(source: Path, destination: Path) -> bool:
    """
    Move an extracted file or directory to the expected location.
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
            f"Destination already exists; leaving existing path untouched: "
            f"{destination.relative_to(SCRIPT_DIR)}"
        )
        return True

    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))

    except OSError as exc:
        error(f"Could not move {source}: {exc}")
        return False

    success(
        f"Placed: {destination.relative_to(SCRIPT_DIR)}"
    )

    return True


def normalise_extracted_layout() -> bool:
    """
    Normalise the extracted archive into the repository's current structure.

    The important correction here is:

        swi_core/

    NOT:

        src/

    The automated test file belongs at:

        test_swi_core.py
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
        warning(
            "test_swi_core.py was not found in the extracted archive."
        )
    else:
        root_test_file = SCRIPT_DIR / "test_swi_core.py"

        if test_file.resolve() != root_test_file.resolve():
            if not move_to_root(test_file, root_test_file):
                return False
        else:
            success("test_swi_core.py is already in the correct location.")

    # ------------------------------------------------------------------
    # Root documentation and configuration files
    # ------------------------------------------------------------------

    root_files = [
        "README.md",
        "SETUP_GUIDE.md",
        "INSTALLATION.md",
        "requirements.txt",
        ".env.example",
        "LICENSE",
    ]

    for filename in root_files:
        source = find_file(filename)

        if source is None:
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
        config_dir.mkdir(exist_ok=True)
    except OSError as exc:
        error(f"Could not create config/: {exc}")
        return False

    config_file = find_file("swi_config.yaml")

    if config_file is not None:
        destination = config_dir / "swi_config.yaml"

        if config_file.resolve() != destination.resolve():
            if not move_to_root(config_file, destination):
                return False
        else:
            success("config/swi_config.yaml is in the correct location.")
    else:
        warning("swi_config.yaml was not found.")

    return True


# ============================================================================
# REPOSITORY STRUCTURE VERIFICATION
# ============================================================================

def verify_required_files() -> bool:
    """
    Verify the expected repository structure.
    """

    section("VERIFYING REPOSITORY STRUCTURE")

    missing = []

    for relative_path in REQUIRED_FILES:
        path = SCRIPT_DIR / relative_path

        if path.exists():
            print(f"  [OK]   {relative_path}")
        else:
            print(f"  [MISS] {relative_path}")
            missing.append(relative_path)

    print()

    if missing:
        warning(
            f"{len(missing)} expected file(s) are missing."
        )

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

    This is optional. The script only performs it when --install is supplied.
    """

    section("INSTALLING DEPENDENCIES")

    requirements = SCRIPT_DIR / "requirements.txt"

    if not requirements.exists():
        warning(
            "requirements.txt was not found. "
            "Dependency installation skipped."
        )
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
            f"Dependency installation failed with exit code "
            f"{result.returncode}."
        )
        return False

    success("Dependencies installed successfully.")

    return True


# ============================================================================
# PYTEST AVAILABILITY
# ============================================================================

def check_pytest_available() -> bool:
    """
    Check whether pytest is installed.
    """

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

    info(result.stdout.strip())
    return True


# ============================================================================
# TEST EXECUTION
# ============================================================================

def run_tests() -> bool:
    """
    Run the actual SWI automated test suite.

    No result is fabricated.

    PASS means pytest returned exit code 0.

    FAIL means pytest returned a non-zero exit code.

    MISSING means test_swi_core.py does not exist.
    """

    section("RUNNING AUTOMATED TESTS")

    test_file = SCRIPT_DIR / "test_swi_core.py"

    if not test_file.exists():
        error(
            "test_swi_core.py is missing. "
            "The automated test suite cannot be executed."
        )
        return False

    if not check_pytest_available():
        error(
            "pytest is unavailable. "
            "Install dependencies or install pytest before testing."
        )
        return False

    info("Executing:")
    print()
    print("    python3 -m pytest test_swi_core.py -v")
    print()

    command = [
        sys.executable,
        "-m",
        "pytest",
        "test_swi_core.py",
        "-v",
        "--tb=short",
    ]

    try:
        result = subprocess.run(
            command,
            cwd=SCRIPT_DIR,
            check=False,
        )

    except OSError as exc:
        error(f"Could not execute pytest: {exc}")
        return False

    print()

    if result.returncode == 0:
        success(
            "Automated test suite PASSED."
        )
        return True

    error(
        f"Automated test suite FAILED with exit code "
        f"{result.returncode}."
    )

    return False


# ============================================================================
# LOG DIRECTORY
# ============================================================================

def prepare_logs_directory() -> bool:
    """
    Create the logs directory expected by the audit logger.
    """

    logs_dir = SCRIPT_DIR / "logs"

    try:
        logs_dir.mkdir(exist_ok=True)
    except OSError as exc:
        error(f"Could not create logs/: {exc}")
        return False

    success(
        f"Logs directory ready: {logs_dir.relative_to(SCRIPT_DIR)}"
    )

    return True


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:

    section("SWI V1 — MODULES 00–10 EXTRACTION & VERIFICATION")

    print()
    print("Repository:", SCRIPT_DIR)
    print()

    # ------------------------------------------------------------------
    # Find source archive.
    # ------------------------------------------------------------------

    archive = find_archive()

    if archive is None:

        warning("No source ZIP archive was found.")

        print()
        print("If the repository is already extracted, the script will")
        print("attempt to verify the existing repository structure.")
        print()

        structure_ok = verify_required_files()

        if not structure_ok:
            print()
            error(
                "Repository structure is incomplete and no source "
                "archive was supplied."
            )

            print()
            print("Usage:")
            print(
                "    python3 extract_and_setup.py "
                "/path/to/swi_v1_part1_source.zip"
            )

            return 1

        prepare_logs_directory()

        if "--install" in sys.argv:
            if not install_dependencies():
                return 1

        test_ok = run_tests()

        section("FINAL RESULT")

        if test_ok:
            success(
                "EXISTING REPOSITORY PASSED TEST VERIFICATION."
            )
            return 0

        error(
            "REPOSITORY STRUCTURE IS PRESENT, "
            "BUT TEST VERIFICATION FAILED."
        )
        return 1

    # ------------------------------------------------------------------
    # Inspect archive.
    # ------------------------------------------------------------------

    if not inspect_archive(archive):
        return 1

    # ------------------------------------------------------------------
    # Extract archive.
    # ------------------------------------------------------------------

    if not extract_archive(archive):
        return 1

    # ------------------------------------------------------------------
    # Verify structure.
    # ------------------------------------------------------------------

    structure_ok = verify_required_files()

    if not structure_ok:
        warning(
            "Extraction completed, but the expected repository "
            "structure is incomplete."
        )
        return 1

    # ------------------------------------------------------------------
    # Prepare runtime directory.
    # ------------------------------------------------------------------

    if not prepare_logs_directory():
        return 1

    # ------------------------------------------------------------------
    # Optional dependency installation.
    # ------------------------------------------------------------------

    if "--install" in sys.argv:
        if not install_dependencies():
            return 1
    else:
        info(
            "Dependency installation skipped."
        )
        info(
            "Use --install if dependencies need to be installed."
        )

    # ------------------------------------------------------------------
    # Run tests.
    # ------------------------------------------------------------------

    test_ok = run_tests()

    # ------------------------------------------------------------------
    # Final result.
    # ------------------------------------------------------------------

    section("FINAL RESULT")

    if test_ok:
        success(
            "EXTRACTION AND TEST VERIFICATION PASSED."
        )

        print()
        print(
            "The repository structure is present and the automated "
            "test command returned exit code 0."
        )

        return 0

    error(
        "EXTRACTION COMPLETED, BUT TEST VERIFICATION FAILED."
    )

    print()
    print(
        "Review the pytest output above. "
        "No passing result is claimed when pytest fails."
    )

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
