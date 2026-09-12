# SWI V1 Module 1-10 — Setup & Configuration Guide

## Overview

This guide walks you through extracting the ZIP file, understanding the
current configuration surface, and running the test suite.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)
- 500 MB available disk space (minimum)

## Step 1: Extract the ZIP File

The repository contains `swi_v1_part1_source.zip`, which contains the
source code.

### Option A: Extract via Command Line

```bash
# Navigate to the repository directory
cd SWI-V1-Module-1-10

# Extract the ZIP file
unzip swi_v1_part1_source.zip

# This creates the following structure, flat in the current directory
# (there is no swi_v1_part1_source/ subfolder):
#   swi_core/
#     __init__.py
#     module00_trainer.py
#     module01_node_scanner.py
#     ...through module10_external_sandbox.py
#   test_swi_core.py
```

### Option B: Extract Programmatically

```python
import zipfile

zip_path = 'swi_v1_part1_source.zip'
extract_path = '.'

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

print("Extraction complete!")
```

## Step 2: Environment Setup

### Create a Virtual Environment

```bash
python3 -m venv swi_env

# On macOS/Linux:
source swi_env/bin/activate
# On Windows:
swi_env\Scripts\activate
```

### Install Dependencies

```bash
pip install --upgrade pip setuptools wheel

# requirements.txt is at the repo root, not inside the ZIP
pip install -r requirements.txt
```

## Step 3: Configuration — current status

`config/swi_config.yaml` and `.env.example` already ship with the repo.
**Neither is currently read by any module** — there is no YAML loader
and no `os.environ`/`dotenv` call anywhere in `swi_core`. They document
the intended settings surface, but every module is configured through
constructor arguments only (see the examples in Step 7). Treat them as
a design reference, not a working config file, until a loader exists.

If you want a local `.env` for your own notes:

```bash
cp .env.example .env
```

It will not affect runtime behavior yet.

## Step 4: Directory Structure Setup

The only directories the code actually needs at runtime are `logs/`
(required — see the `AuditLogger` note in Step 7) and `.swi_temp/`
(used by the sandbox for temp files):

```bash
mkdir -p logs .swi_temp
chmod 755 logs .swi_temp
```

## Step 5: Verify Installation

```bash
python3 --version
pip list
python3 -m pytest --version
```

### Test Basic Import

Create `test_import.py` at the repo root (next to `swi_core/`):

```python
#!/usr/bin/env python3
"""Verify SWI module imports."""

import sys

try:
    from swi_core.module00_trainer import Trainer
    from swi_core.module02_security_probe import SecurityProbe
    print("✓ swi_core imports successfully")
    print("\nSWI system is ready for testing!")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
```

Run it from the repo root:

```bash
python3 test_import.py
```

## Step 6: Run Tests

```bash
# Run from the repo root — test_swi_core.py lives there, not in a
# swi_v1_part1_source/ subfolder
python3 -m pytest test_swi_core.py -v

# With coverage
python3 -m pytest test_swi_core.py -v --cov=swi_core --cov-report=term

# Run a single test (tests are plain functions, not classes —
# use its exact name from `pytest --collect-only` or the list below)
python3 -m pytest test_swi_core.py::test_security_probe_flags_instruction_override -v
```

### Generate Test Report

```bash
python3 -m pytest test_swi_core.py --cov=swi_core --cov-report=html

open htmlcov/index.html        # macOS
xdg-open htmlcov/index.html    # Linux
start htmlcov/index.html       # Windows
```

## Step 7: Quick Start Examples

These match the actual classes and method names in `swi_core` as of
this ZIP. Run them from the repo root so `swi_core` is importable.

### Example 1: Security Probe (Module 02)

```python
from swi_core.module02_security_probe import SecurityProbe

probe = SecurityProbe(block_threshold=0.5)
result = probe.scan("Your input text here")
print(f"Blocked: {result.blocked}")
print(f"Risk score: {result.risk_score}")
print(f"Triggered patterns: {result.triggered}")
```

### Example 2: Redaction Engine (Module 05)

```python
from swi_core.module05_redaction_engine import RedactionEngine

redactor = RedactionEngine()
result = redactor.redact("Contact me at john@example.com or 555-123-4567")
print(result.redacted_text)
print(result.matches)   # list of RedactionMatch, one per masked item
```

### Example 3: Encryption Handler (Module 04)

```python
from swi_core.module04_encryption_handler import EncryptionHandler

handler = EncryptionHandler()   # generates a random key if none given
payload = handler.encrypt(b"Secret message")
decrypted = handler.decrypt(payload)
print(decrypted)
```

### Example 4: External Sandbox (Module 10)

```python
from swi_core.module10_external_sandbox import ExternalSandbox

sandbox = ExternalSandbox(timeout_seconds=30, memory_bytes=512 * 1024 * 1024)
result = sandbox.run("print('Hello from sandbox')")
print(result)
```

### Example 5: Orchestrated Pipeline (Module 00)

```python
import os
os.makedirs("logs", exist_ok=True)   # AuditLogger requires this to exist first

from swi_core.module00_trainer import Trainer

trainer = Trainer(audit_log_path="logs/audit.jsonl")
result = trainer.process("Your input here")
print(result.allowed, result.reason)
```

## Step 8: Troubleshooting

### Issue: ModuleNotFoundError: No module named 'swi_core'

```bash
source swi_env/bin/activate
# Run Python from the repo root, or add it explicitly:
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: FileNotFoundError when creating a Trainer or AuditLogger

`AuditLogger` opens its log file immediately on construction and does
not create missing parent directories:

```bash
mkdir -p logs
```

### Issue: Tests Fail

```bash
python3 -m pytest test_swi_core.py -v -s
pip install -r requirements.txt --upgrade
rm -rf .pytest_cache __pycache__
```

## Step 9: Configuration Validation

This script only checks that expected files/directories exist — it
does not validate that anything in `swi_config.yaml` is actually
applied at runtime, because nothing reads it yet (see Step 3).

```python
#!/usr/bin/env python3
"""Check that expected SWI setup files/directories are present."""

import yaml
import os

def validate_config():
    errors = []
    warnings = []

    config_path = 'config/swi_config.yaml'
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                yaml.safe_load(f)
            print(f"✓ Configuration file parses: {config_path}")
            warnings.append("Note: this file is not yet read by swi_core at runtime")
        except Exception as e:
            errors.append(f"Configuration file error: {e}")
    else:
        errors.append(f"Configuration file not found: {config_path}")

    for dir_name in ['logs', '.swi_temp']:
        if os.path.isdir(dir_name):
            print(f"✓ Directory exists: {dir_name}")
        else:
            errors.append(f"Missing directory: {dir_name}")

    if os.path.exists('.env'):
        print("✓ Environment file exists: .env")
    else:
        warnings.append("No local .env (optional — copy from .env.example if wanted)")

    if errors:
        print("\n❌ ERRORS:")
        for e in errors:
            print(f"  - {e}")
        return False

    if warnings:
        print("\n⚠️  NOTES:")
        for w in warnings:
            print(f"  - {w}")

    print("\n✅ Setup files present.")
    return True

if __name__ == '__main__':
    validate_config()
```

## Next Steps

1. **Explore Modules**: Review the source in `swi_core/`
2. **Run Tests**: `python3 -m pytest test_swi_core.py -v`
3. **Check Limitations**: Each module's docstring states what it does
   and does not do — read those before relying on a module
4. **Build Examples**: Try the Step 7 snippets against your own input
5. **Contribute**: Submit issues or improvements through GitHub

## Support

- README.md for the architectural overview
- `test_swi_core.py` for real, working usage examples
- GitHub Issues for questions or bug reports

## Core Principle

> "Don't claim what hasn't been built. Don't claim what hasn't been
> tested. Don't hide what the implementation cannot do."

---

**Version:** 1.0.1
**Author:** Keletso Ronald Mosidila
