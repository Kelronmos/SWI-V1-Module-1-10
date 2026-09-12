# SWI V1 Module 1-10 - Installation & Extraction Guide

## Quick Start

### 1. Clone or Download the Repository

```bash
git clone https://github.com/Kelronmos/SWI-V1-Module-1-10.git
cd SWI-V1-Module-1-10
```

### 2. Extract the Source ZIP

```bash
unzip swi_v1_part1_source.zip
```

This extracts flat into the repo root — it does **not** create a
`swi_v1_part1_source/` subfolder. After extraction you'll have:

```
SWI-V1-Module-1-10/
├── README.md
├── SETUP_GUIDE.md
├── INSTALLATION.md
├── requirements.txt
├── .env.example
├── config/
│   └── swi_config.yaml          # NOTE: currently descriptive only — see below
├── swi_core/                    # the actual package
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
└── test_swi_core.py             # all 22 tests, at repo root
```

There is no `src/`, `tests/`, `docs/`, or `examples/` folder produced by
extraction — earlier drafts of this guide described a layout that the
current ZIP does not produce. If you want that layout, see "Optional:
Matching the described directory layout" at the end of this file.

### 3. Create Virtual Environment

```bash
python3 -m venv swi_env
source swi_env/bin/activate      # Linux/macOS
swi_env\Scripts\activate         # Windows
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Run the Tests

```bash
python3 -m pytest test_swi_core.py -v
```

All 22 tests should pass. This is the actual, current test suite —
run it from the repo root, not from a `swi_v1_part1_source/` path.

## Configuration

`config/swi_config.yaml` documents the intended module settings
(risk thresholds, key lengths, etc.), but **no module currently reads
this file** — none of the `swi_core` classes accept a `config_path` or
load YAML. Settings are passed as constructor arguments instead. Treat
`swi_config.yaml` as a design reference until a loader is written, not
as something you can edit to change runtime behavior yet.

## Using the SWI Pipeline

The examples below match the actual constructors and methods in
`swi_core` as of this ZIP. If you update the source, update this
section too — that's the point of it existing.

### Basic Example — the orchestrated pipeline (Module 00)

`AuditLogger` opens `audit_log_path` for writing as soon as it's
constructed — it does not create missing parent directories, so
create the `logs/` folder first or the constructor raises
`FileNotFoundError`:

```python
import os
os.makedirs("logs", exist_ok=True)

from swi_core.module00_trainer import Trainer

trainer = Trainer(audit_log_path="logs/audit.jsonl")

result = trainer.process("Your input here")

print(f"Allowed: {result.allowed}")
print(f"Reason: {result.reason}")
print(f"Risk score: {result.security.risk_score}")
print(f"Redacted text: {result.redaction.redacted_text}")
```

Note: `Trainer.process()` does not accept a `timestamp` argument. It
calls `ContextSync.record_turn()` with only a turn counter, so
Module 03's staleness/out-of-order detection cannot currently be
exercised through the orchestrated pipeline — only by using
`ContextSync` directly (see below). If your workflow needs real
conversation timestamps checked, that wiring still needs to be added
to `Trainer.process()`.

### Individual Module Usage

```python
# Security Probe (Module 02)
from swi_core.module02_security_probe import SecurityProbe
probe = SecurityProbe(block_threshold=0.5)
result = probe.scan("suspicious input")
print(result.blocked, result.risk_score, result.triggered)

# Context Sync (Module 03) — with an explicit timestamp
from swi_core.module03_context_sync import ContextSync
import datetime
sync = ContextSync(staleness_seconds=1800.0)
result = sync.record_turn(1, timestamp=datetime.datetime.now(datetime.timezone.utc))

# Encryption (Module 04)
from swi_core.module04_encryption_handler import EncryptionHandler
encryptor = EncryptionHandler()          # generates a key if none given
payload = encryptor.encrypt(b"secret")
plaintext = encryptor.decrypt(payload)

# Audit Logging (Module 09)
from swi_core.module09_audit_logger import AuditLogger
audit = AuditLogger(log_path="logs/audit.jsonl")   # log_path is required
audit.log_event({"type": "security_check", "result": "passed"})
```

## Troubleshooting

### ModuleNotFoundError: No module named 'swi_core'

Run Python from the repo root (the directory containing `swi_core/`),
or add it to `PYTHONPATH`:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Dependency Installation Fails

```bash
# Linux (Ubuntu/Debian)
sudo apt-get install python3-dev libffi-dev libssl-dev

# macOS
brew install python3

pip install -r requirements.txt --upgrade
```

## Optional: Matching the described directory layout

If you'd rather have the `src/` + `tests/` structure this guide used
to describe, that's a repo-restructuring decision, not something the
current ZIP does for you. It means: move `swi_core/` to `src/swi_core/`,
move `test_swi_core.py` to `tests/`, and update the imports in
`test_swi_core.py` and every internal `from .moduleNN_*` reference
accordingly, then update the Makefile and this file to match. It's a
deliberate choice, not a bug fix — do it only if you actually want
that layout going forward.

## Core Principle

> "Don't claim what hasn't been built. Don't claim what hasn't been
> tested. Don't hide what the implementation cannot do."

This file follows that principle by describing only what the current
`swi_core` package actually does, at the paths it actually lives at.

---

**Version:** 1.0.1
**Author:** Keletso Ronald Mosidila
