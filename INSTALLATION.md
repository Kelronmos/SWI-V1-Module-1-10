# SWI V1 Module 1-10 - Installation & Extraction Guide

## Quick Start

### 1. Clone or Download the Repository

```bash
git clone https://github.com/Kelronmos/SWI-V1-Module-1-10.git
cd SWI-V1-Module-1-10
```

### 2. Extract the Source ZIP

```bash
# Using Python (recommended - cross-platform)
python3 extract_and_setup.py

# OR using command line
unzip swi_v1_part1_source.zip
```

### 3. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv swi_env

# Activate it
# On Linux/macOS:
source swi_env/bin/activate

# On Windows:
swi_env\Scripts\activate
```

### 4. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

### 5. Verify Installation

```bash
# Check Python version
python3 --version

# Verify packages
pip list

# Run a simple test
python3 -c "import sys; print(f'Python {sys.version}')"
```

## Directory Structure After Extraction

```
SWI-V1-Module-1-10/
├── README.md                          # Project overview
├── SETUP_GUIDE.md                    # Detailed setup guide
├── INSTALLATION.md                   # This file
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment template
├── .gitignore                        # Git ignore rules
├── extract_and_setup.py              # Automated setup script
│
├── config/
│   └── swi_config.yaml              # Main configuration
│
├── logs/                             # Application logs (created after first run)
│   └── audit.jsonl                  # Audit log file
│
├── .swi_temp/                        # Temporary storage (created at runtime)
│
├── swi_v1_part1_source/              # Extracted source code
│   ├── src/
│   │   ├── __init__.py
│   │   ├── module_00.py             # Trainer/Orchestrator
│   │   ├── module_01.py             # Node Scanner
│   │   ├── module_02.py             # Security Probe
│   │   ├── module_03.py             # Context Sync
│   │   ├── module_04.py             # Encryption Handler
│   │   ├── module_05.py             # Redaction Engine
│   │   ├── module_06.py             # Drift Analyzer
│   │   ├── module_07.py             # Memory Validator
│   │   ├── module_08.py             # Access Auth
│   │   ├── module_09.py             # Audit Logger
│   │   └── module_10.py             # External Sandbox
│   │
│   ├── tests/
│   │   ├── test_swi_core.py         # Main test suite
│   │   ├── test_modules_*.py        # Module-specific tests
│   │   └── fixtures/                # Test data
│   │
│   └── requirements.txt              # Source dependencies
│
├── tests/                            # Additional test files
│   └── fixtures/                    # Test fixtures
│
├── docs/                             # Documentation
│
└── examples/                         # Example code
```

## Configuration

### 1. Copy Environment Template

```bash
cp .env.example .env
```

### 2. Edit Configuration

Update these files based on your needs:

- **config/swi_config.yaml** - Module settings and pipeline configuration
- **.env** - Environment variables and paths

### 3. Common Configuration Changes

```yaml
# config/swi_config.yaml

# Security risk threshold (0.0 - 1.0)
modules:
  module_02:
    risk_threshold: 0.7

# Sandbox resource limits
modules:
  module_10:
    timeout_seconds: 30
    memory_limit_mb: 512
    cpu_limit_percent: 50
```

## Running Tests

### Run All Tests

```bash
python3 -m pytest swi_v1_part1_source/tests/test_swi_core.py -v
```

### Run Specific Test Module

```bash
# Test Security Probe (Module 02)
python3 -m pytest swi_v1_part1_source/tests/test_swi_core.py::TestModule02 -v

# Test with coverage
python3 -m pytest swi_v1_part1_source/tests/ --cov=swi_v1_part1_source/src --cov-report=html
```

### Generate Coverage Report

```bash
python3 -m pytest swi_v1_part1_source/tests/ \
  --cov=swi_v1_part1_source/src \
  --cov-report=html \
  --cov-report=term-color

# View report
open htmlcov/index.html
```

## Troubleshooting

### Issue: ModuleNotFoundError

**Cause:** Python path not configured correctly

**Solution:**
```bash
# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/swi_v1_part1_source/src"

# Or use in commands
PYTHONPATH=./swi_v1_part1_source/src python3 -m pytest tests/
```

### Issue: Permission Denied (Logs/Temp)

**Cause:** Directory permissions

**Solution:**
```bash
chmod 755 logs
chmod 755 .swi_temp
```

### Issue: Dependency Installation Fails

**Cause:** Missing system dependencies

**Solution:**
```bash
# Linux (Ubuntu/Debian)
sudo apt-get install python3-dev libffi-dev libssl-dev

# macOS
brew install python3

# Then retry
pip install -r requirements.txt --upgrade
```

### Issue: Virtual Environment Not Activating

**Solution:**
```bash
# Recreate virtual environment
rm -rf swi_env
python3 -m venv swi_env
source swi_env/bin/activate  # Linux/macOS
# or
swi_env\Scripts\activate  # Windows
```

## Using the SWI Pipeline

### Basic Example

```python
import sys
sys.path.insert(0, 'swi_v1_part1_source/src')

from module_00 import Trainer

# Initialize pipeline
trainer = Trainer(config_path='config/swi_config.yaml')

# Process input
result = trainer.process(
    input_text="Your input here",
    timestamp="2026-09-12T08:00:00Z"
)

print(f"Security Risk: {result['risk_score']}")
print(f"Redacted Text: {result['redacted_text']}")
print(f"Audit Entry: {result['audit_id']}")
```

### Individual Module Usage

```python
# Security Probe
from module_02 import SecurityProbe
probe = SecurityProbe(risk_threshold=0.7)
result = probe.check("suspicious input")

# Encryption
from module_04 import EncryptionHandler
encryptor = EncryptionHandler(key_length=32)
encrypted = encryptor.encrypt("secret")

# Audit Logging
from module_09 import AuditLogger
audit = AuditLogger()
audit.log_event({"type": "security_check", "result": "passed"})
```

## Next Steps

1. **Read Documentation**
   - Review README.md for architecture
   - Check SETUP_GUIDE.md for detailed steps
   - Review module limitations in config/swi_config.yaml

2. **Explore Code**
   ```bash
   cd swi_v1_part1_source/src
   ls -la
   ```

3. **Run Tests**
   ```bash
   python3 -m pytest tests/ -v --cov
   ```

4. **Create Examples**
   - Check examples/ directory
   - Build your own integration

5. **Review Limitations**
   - All modules have explicit limitations documented
   - Check config/swi_config.yaml for scope
   - Single-process, local reference implementation only

## Support

- **Documentation:** See README.md and SETUP_GUIDE.md
- **Issues:** GitHub Issues
- **Testing:** Run `pytest` with verbose output
- **Configuration:** Edit config/swi_config.yaml

## Core Principle

> "Don't claim what hasn't been built. Don't claim what hasn't been tested. Don't hide what the implementation cannot do."

All features in this implementation have:
- ✅ Working code
- ✅ Automated tests
- ✅ Documented limitations
- ✅ Explicit scope definition

---

**Version:** 1.0.0  
**Last Updated:** 2026-09-12  
**Author:** Keletso Ronald Mosidila
