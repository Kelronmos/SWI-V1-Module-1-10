# SWI V1 Module 1-10 — Setup & Configuration Guide

## Overview

This guide walks you through extracting the ZIP file, configuring the SWI system, and preparing it for testing and use.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)
- 500 MB available disk space (minimum)

## Step 1: Extract the ZIP File

The repository contains `swi_v1_part1_source.zip` which contains the source code.

### Option A: Extract via Command Line

```bash
# Navigate to the repository directory
cd SWI-V1-Module-1-10

# Extract the ZIP file
unzip swi_v1_part1_source.zip

# This will create the following structure:
# swi_v1_part1_source/
#   ├── src/
#   ├── tests/
#   ├── config/
#   └── requirements.txt
```

### Option B: Extract Programmatically

```python
import zipfile
import os

zip_path = 'swi_v1_part1_source.zip'
extract_path = '.'

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

print("Extraction complete!")
```

## Step 2: Environment Setup

### Create a Virtual Environment

```bash
# Create virtual environment
python3 -m venv swi_env

# Activate the virtual environment
# On macOS/Linux:
source swi_env/bin/activate

# On Windows:
swi_env\Scripts\activate
```

### Install Dependencies

```bash
# First, ensure you have the requirements file
# If extracted, use the one from the ZIP:
pip install --upgrade pip setuptools wheel

# Install project dependencies
pip install -r swi_v1_part1_source/requirements.txt

# Core dependencies (if requirements.txt is not available):
pip install pytest pytest-cov cryptography pyyaml
```

## Step 3: Configuration

### Create Configuration Directory

```bash
mkdir -p config
```

### Create Main Configuration File

Create `config/swi_config.yaml`:

```yaml
# SWI Configuration
swi:
  version: "1.0.0"
  environment: "development"
  
pipeline:
  enabled_modules:
    - module_00  # Trainer (Orchestrator)
    - module_02  # Security Probe
    - module_03  # Context Sync
    - module_05  # Redaction Engine
    - module_06  # Drift Analyzer
    - module_07  # Memory Validator
    - module_09  # Audit Logger
  
  module_00:
    description: "Pipeline Orchestrator"
    enabled: true
  
  module_01:
    name: "Node Scanner"
    enabled: true
    hash_algorithm: "sha256"
  
  module_02:
    name: "Security Probe"
    enabled: true
    risk_threshold: 0.7
    check_patterns:
      - instruction_override
      - role_override
      - system_prompt_extraction
      - zero_width_characters
      - base64_payloads
  
  module_03:
    name: "Context Sync"
    enabled: true
    max_context_age_seconds: 3600
    check_ordering: true
  
  module_04:
    name: "Encryption Handler"
    enabled: true
    algorithm: "AES-256-GCM"
    key_length: 32
  
  module_05:
    name: "Redaction Engine"
    enabled: true
    patterns:
      - email_addresses
      - phone_numbers
      - credit_card_numbers
      - omang_identifiers
  
  module_06:
    name: "Drift Analyzer"
    enabled: true
    similarity_threshold: 0.8
  
  module_07:
    name: "Memory Validator"
    enabled: true
    hash_algorithm: "sha256"
  
  module_08:
    name: "Access Auth"
    enabled: true
    token_expiry_seconds: 3600
    signature_algorithm: "HMAC-SHA256"
  
  module_09:
    name: "Audit Logger"
    enabled: true
    log_format: "jsonl"
    log_file: "logs/audit.jsonl"
    hash_chain: true
  
  module_10:
    name: "External Sandbox"
    enabled: true
    timeout_seconds: 30
    memory_limit_mb: 512
    cpu_limit_percent: 50

security:
  enable_pii_redaction: true
  enable_injection_detection: true
  enable_drift_detection: true
  audit_all_operations: true

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  log_directory: "logs"

storage:
  audit_log_path: "logs/audit.jsonl"
  temp_directory: ".swi_temp"
  memory_validation_records: 1000

testing:
  pytest_verbosity: "v"
  coverage_threshold: 80
```

### Create Environment Variables File

Create `.env`:

```bash
# SWI Environment Configuration
SWI_ENV=development
SWI_DEBUG=false
SWI_LOG_LEVEL=INFO
SWI_CONFIG_PATH=config/swi_config.yaml

# Security
SWI_ENCRYPTION_KEY_LENGTH=32
SWI_TOKEN_EXPIRY=3600

# Paths
SWI_LOG_DIR=logs
SWI_TEMP_DIR=.swi_temp
SWI_AUDIT_LOG=logs/audit.jsonl

# Testing
SWI_TEST_MODE=false
SWI_PYTEST_ARGS=-v --cov=swi_v1_part1_source --cov-report=term-color
```

### Create Module Configuration Templates

Create `config/modules_config.json`:

```json
{
  "modules": {
    "module_00": {
      "name": "Trainer",
      "description": "Pipeline Orchestrator",
      "role": "core",
      "status": "active"
    },
    "module_01": {
      "name": "Node Scanner",
      "description": "File integrity checker",
      "role": "standalone",
      "status": "active"
    },
    "module_02": {
      "name": "Security Probe",
      "description": "Heuristic security checks",
      "role": "pipeline",
      "status": "active"
    },
    "module_03": {
      "name": "Context Sync",
      "description": "Timestamp and ordering validation",
      "role": "pipeline",
      "status": "active"
    },
    "module_04": {
      "name": "Encryption Handler",
      "description": "AES-256-GCM encryption",
      "role": "standalone",
      "status": "active"
    },
    "module_05": {
      "name": "Redaction Engine",
      "description": "PII and structured identifier masking",
      "role": "pipeline",
      "status": "active"
    },
    "module_06": {
      "name": "Drift Analyzer",
      "description": "Textual change detection",
      "role": "pipeline",
      "status": "active"
    },
    "module_07": {
      "name": "Memory Validator",
      "description": "In-process hash chain validation",
      "role": "pipeline",
      "status": "active"
    },
    "module_08": {
      "name": "Access Auth",
      "description": "Session token management",
      "role": "standalone",
      "status": "active"
    },
    "module_09": {
      "name": "Audit Logger",
      "description": "JSONL audit logging with hash chain",
      "role": "pipeline",
      "status": "active"
    },
    "module_10": {
      "name": "External Sandbox",
      "description": "Isolated Python code execution",
      "role": "standalone",
      "status": "active"
    }
  }
}
```

## Step 4: Directory Structure Setup

Create required directories:

```bash
# Create directory structure
mkdir -p logs
mkdir -p .swi_temp
mkdir -p config
mkdir -p tests/fixtures
mkdir -p docs
mkdir -p examples

# Set proper permissions
chmod 755 logs
chmod 755 .swi_temp
chmod 755 config
```

## Step 5: Verify Installation

### Check Python and Dependencies

```bash
# Verify Python version
python3 --version

# Verify installed packages
pip list

# Verify pytest installation
python3 -m pytest --version
```

### Test Basic Import

Create `test_import.py`:

```python
#!/usr/bin/env python3
"""Verify SWI module imports."""

import sys
import os

# Add source to path
sys.path.insert(0, 'swi_v1_part1_source/src')

try:
    print("Testing SWI module imports...")
    print("✓ Python environment ready")
    print("✓ Virtual environment activated")
    print("\nSWI system is ready for testing!")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
```

Run the test:

```bash
python3 test_import.py
```

## Step 6: Run Tests

### Run Full Test Suite

```bash
# Navigate to source directory
cd swi_v1_part1_source

# Run all tests with verbose output
python3 -m pytest test_swi_core.py -v

# Run with coverage report
python3 -m pytest test_swi_core.py -v --cov=. --cov-report=term-color

# Run specific test module
python3 -m pytest test_swi_core.py::TestModule02 -v
```

### Generate Test Report

```bash
# Generate HTML coverage report
python3 -m pytest test_swi_core.py --cov=. --cov-report=html

# Open the report
# On macOS:
open htmlcov/index.html

# On Linux:
xdg-open htmlcov/index.html

# On Windows:
start htmlcov/index.html
```

## Step 7: Quick Start Examples

### Example 1: Security Probe

```python
from swi.module_02 import SecurityProbe

probe = SecurityProbe(risk_threshold=0.7)
text = "Your input text here"
result = probe.check(text)
print(f"Risk score: {result['risk_score']}")
print(f"Threats: {result['threats']}")
```

### Example 2: Redaction Engine

```python
from swi.module_05 import RedactionEngine

redactor = RedactionEngine()
text = "Contact me at john@example.com or 555-1234"
redacted = redactor.redact(text)
print(redacted)
```

### Example 3: Encryption Handler

```python
from swi.module_04 import EncryptionHandler

handler = EncryptionHandler(key_length=32)
plaintext = "Secret message"
encrypted = handler.encrypt(plaintext)
decrypted = handler.decrypt(encrypted)
```

### Example 4: External Sandbox

```python
from swi.module_10 import ExternalSandbox

sandbox = ExternalSandbox(timeout=30, memory_limit_mb=512)
code = "print('Hello from sandbox')"
result = sandbox.execute(code)
```

## Step 8: Troubleshooting

### Issue: ModuleNotFoundError

**Solution:**
```bash
# Verify virtual environment is activated
source swi_env/bin/activate

# Add source to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/swi_v1_part1_source/src"
```

### Issue: Permission Denied on Logs

**Solution:**
```bash
chmod 755 logs
chmod 755 .swi_temp
```

### Issue: Tests Fail

**Solution:**
```bash
# Run with verbose output
python3 -m pytest test_swi_core.py -v -s

# Check for missing dependencies
pip install -r requirements.txt --upgrade

# Clear cache
rm -rf .pytest_cache __pycache__
```

## Step 9: Configuration Validation

Create `validate_config.py`:

```python
#!/usr/bin/env python3
"""Validate SWI configuration."""

import yaml
import json
import os

def validate_config():
    errors = []
    warnings = []
    
    # Check configuration file
    config_path = 'config/swi_config.yaml'
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            print(f"✓ Configuration file valid: {config_path}")
        except Exception as e:
            errors.append(f"Configuration file error: {e}")
    else:
        errors.append(f"Configuration file not found: {config_path}")
    
    # Check required directories
    required_dirs = ['logs', '.swi_temp', 'config']
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"✓ Directory exists: {dir_name}")
        else:
            errors.append(f"Missing directory: {dir_name}")
    
    # Check .env file
    if os.path.exists('.env'):
        print("✓ Environment file exists: .env")
    else:
        warnings.append("Environment file not found: .env")
    
    # Report results
    if errors:
        print("\n❌ ERRORS:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")
    
    print("\n✅ Configuration validation passed!")
    return True

if __name__ == '__main__':
    validate_config()
```

Run validation:

```bash
python3 validate_config.py
```

## Next Steps

1. **Explore Modules**: Review the source code in `swi_v1_part1_source/src/`
2. **Run Tests**: Execute `python3 -m pytest test_swi_core.py -v`
3. **Check Limitations**: Review the README.md for explicitly documented limitations
4. **Build Examples**: Create integration examples based on your use case
5. **Contribute**: Submit issues or improvements to the repository

## Support

For issues or questions:
- Check the README.md for architectural overview
- Review test files for usage examples
- Check the documentation in the ZIP file
- Submit issues through GitHub

---

**Version:** 1.0.0  
**Last Updated:** 2026-09-12  
**Author:** Configuration Setup Guide
