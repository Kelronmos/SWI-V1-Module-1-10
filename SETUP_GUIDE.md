SWI V1 Module 1-10 — Setup & Configuration Guide
Overview
This guide walks you through extracting the ZIP file, understanding the
current configuration surface, and running the test suite.
Prerequisites
Python 3.8 or higher
pip (Python package manager)
Git (for version control)
500 MB available disk space (minimum)
Step 1: Extract the ZIP File
The repository contains swi_v1_part1_source.zip, which contains the
source code.
Option A: Extract via Command Line
Bash
Option B: Extract Programmatically
Python
Step 2: Environment Setup
Create a Virtual Environment
Bash
Install Dependencies
Bash
Step 3: Configuration — current status
config/swi_config.yaml and .env.example already ship with the repo.
Neither is currently read by any module — there is no YAML loader
and no os.environ/dotenv call anywhere in swi_core. They document
the intended settings surface, but every module is configured through
constructor arguments only (see the examples in Step 7). Treat them as
a design reference, not a working config file, until a loader exists.
If you want a local .env for your own notes:
Bash
It will not affect runtime behavior yet.
Step 4: Directory Structure Setup
The only directories the code actually needs at runtime are logs/
(required — see the AuditLogger note in Step 7) and .swi_temp/
(used by the sandbox for temp files):
Bash
Step 5: Verify Installation
Bash
Test Basic Import
Create test_import.py at the repo root (next to swi_core/):
Python
Run it from the repo root:
Bash
Step 6: Run Tests
Bash
Generate Test Report
Bash
Step 7: Quick Start Examples
These match the actual classes and method names in swi_core as of
this ZIP. Run them from the repo root so swi_core is importable.
Example 1: Security Probe (Module 02)
Python
Example 2: Redaction Engine (Module 05)
Python
Example 3: Encryption Handler (Module 04)
Python
Example 4: External Sandbox (Module 10)
Python
Example 5: Orchestrated Pipeline (Module 00)
Python
Step 8: Troubleshooting
Issue: ModuleNotFoundError: No module named 'swi_core'
Bash
Issue: FileNotFoundError when creating a Trainer or AuditLogger
AuditLogger opens its log file immediately on construction and does
not create missing parent directories:
Bash
Issue: Tests Fail
Bash
Step 9: Configuration Validation
This script only checks that expected files/directories exist — it
does not validate that anything in swi_config.yaml is actually
applied at runtime, because nothing reads it yet (see Step 3).
Python
Next Steps
Explore Modules: Review the source in swi_core/
Run Tests: python3 -m pytest test_swi_core.py -v
Check Limitations: Each module's docstring states what it does
and does not do — read those before relying on a module
Build Examples: Try the Step 7 snippets against your own input
Contribute: Submit issues or improvements through GitHub
Support
README.md for the architectural overview
test_swi_core.py for real, working usage examples
GitHub Issues for questions or bug reports
Core Principle
"Don't claim what hasn't been built. Don't claim what hasn't been
tested. Don't hide what the implementation cannot do."
Version: 1.0.1
Author: Keletso Ronald Mosidila
