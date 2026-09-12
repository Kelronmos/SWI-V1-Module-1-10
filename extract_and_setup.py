#!/usr/bin/env python3
"""
SWI V1 Module 1-10 - Automated Extraction and Setup Script
Extracts swi_v1_part1_source.zip and configures the environment
"""

import os
import sys
import zipfile
import json
import yaml
from pathlib import Path

def print_step(step_num, description):
    """Print a formatted step header"""
    print(f"\n{'='*70}")
    print(f"Step {step_num}: {description}")
    print(f"{'='*70}")

def extract_zip(zip_path, extract_to='.'):
    """Extract the ZIP file to the target directory"""
    print_step(1, "Extracting ZIP Archive")
    
    if not os.path.exists(zip_path):
        print(f"❌ ERROR: ZIP file not found: {zip_path}")
        return False
    
    try:
        print(f"📦 Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        print(f"✅ Successfully extracted to {extract_to}")
        
        # List extracted contents
        print("\n📂 Extracted structure:")
        for root, dirs, files in os.walk(extract_to):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            level = root.replace(extract_to, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1)
            for file in files[:10]:  # Limit display
                print(f'{subindent}{file}')
            if len(files) > 10:
                print(f'{subindent}... and {len(files) - 10} more files')
        
        return True
    except Exception as e:
        print(f"❌ ERROR during extraction: {e}")
        return False

def create_directory_structure():
    """Create required directories"""
    print_step(2, "Creating Directory Structure")
    
    required_dirs = [
        'src',
        'tests',
        'config',
        'logs',
        '.swi_temp',
        'docs',
        'examples',
        'data',
        'artifacts'
    ]
    
    for dir_name in required_dirs:
        try:
            os.makedirs(dir_name, exist_ok=True)
            print(f"✅ Created/Verified: {dir_name}/")
        except Exception as e:
            print(f"⚠️  Could not create {dir_name}: {e}")
    
    print("\n✅ Directory structure ready")

def create_config_files():
    """Create configuration files"""
    print_step(3, "Creating Configuration Files")
    
    # Main config YAML
    config = {
        'swi': {
            'version': '1.0.0',
            'environment': 'development',
            'author': 'Keletso Ronald Mosidila'
        },
        'pipeline': {
            'enabled_modules': [
                'module_00', 'module_02', 'module_03',
                'module_05', 'module_06', 'module_07', 'module_09'
            ],
            'module_settings': {
                'module_00': {
                    'name': 'Trainer (Orchestrator)',
                    'enabled': True
                },
                'module_02': {
                    'name': 'Security Probe',
                    'risk_threshold': 0.7
                },
                'module_03': {
                    'name': 'Context Sync',
                    'max_age_seconds': 3600
                },
                'module_05': {
                    'name': 'Redaction Engine',
                    'enabled': True
                },
                'module_06': {
                    'name': 'Drift Analyzer',
                    'threshold': 0.8
                },
                'module_07': {
                    'name': 'Memory Validator',
                    'enabled': True
                },
                'module_09': {
                    'name': 'Audit Logger',
                    'log_path': 'logs/audit.jsonl'
                }
            }
        },
        'security': {
            'enable_pii_redaction': True,
            'enable_injection_detection': True,
            'audit_all_operations': True
        },
        'storage': {
            'audit_log': 'logs/audit.jsonl',
            'temp_dir': '.swi_temp'
        },
        'logging': {
            'level': 'INFO',
            'directory': 'logs'
        }
    }
    
    os.makedirs('config', exist_ok=True)
    
    try:
        with open('config/swi_config.yaml', 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        print("✅ Created: config/swi_config.yaml")
    except ImportError:
        # YAML not available, use JSON
        with open('config/swi_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        print("✅ Created: config/swi_config.json (YAML not available)")
    except Exception as e:
        print(f"⚠️  Could not create config: {e}")

def create_env_file():
    """Create .env file"""
    print_step(4, "Creating Environment File")
    
    env_content = """# SWI Environment Configuration
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
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created: .env")
    except Exception as e:
        print(f"⚠️  Could not create .env: {e}")

def create_requirements_file():
    """Create requirements.txt if not present"""
    print_step(5, "Checking Dependencies")
    
    requirements = """pytest>=7.0.0
pytest-cov>=4.0.0
cryptography>=41.0.0
pyyaml>=6.0
python-dotenv>=1.0.0
"""
    
    if not os.path.exists('requirements.txt'):
        try:
            with open('requirements.txt', 'w') as f:
                f.write(requirements)
            print("✅ Created: requirements.txt")
        except Exception as e:
            print(f"⚠️  Could not create requirements.txt: {e}")
    else:
        print("✅ requirements.txt already exists")
    
    print("\n📦 To install dependencies, run:")
    print("   pip install -r requirements.txt")

def verify_installation():
    """Verify the installation"""
    print_step(6, "Verifying Installation")
    
    checks = {
        'README.md': 'Project documentation',
        'config/swi_config.yaml': 'Configuration file',
        '.env': 'Environment variables',
        'logs': 'Logs directory',
        '.swi_temp': 'Temporary directory',
        'requirements.txt': 'Python dependencies'
    }
    
    all_ok = True
    for item, description in checks.items():
        exists = os.path.exists(item)
        status = "✅" if exists else "⚠️"
        print(f"{status} {description}: {item}")
        if not exists and item != '.env':
            all_ok = False
    
    return all_ok

def print_summary():
    """Print final summary"""
    print_step(7, "Setup Complete!")
    
    summary = """
✅ SWI V1 Module 1-10 is now ready to use!

📋 Next Steps:
   1. Activate virtual environment:
      source swi_env/bin/activate  (Linux/macOS)
      swi_env\\Scripts\\activate     (Windows)
   
   2. Install dependencies:
      pip install -r requirements.txt
   
   3. Run tests:
      python3 -m pytest test_swi_core.py -v
   
   4. Start developing:
      - Check src/ for source code
      - Check tests/ for test examples
      - Review config/swi_config.yaml for settings

📚 Documentation:
   - README.md - Project overview
   - SETUP_GUIDE.md - Detailed setup guide
   - SWI_v4.7_Volume1_Part1.docx - Architecture documentation

🔧 Configuration:
   - config/swi_config.yaml - Main configuration
   - .env - Environment variables
   - requirements.txt - Python dependencies

📂 Directories:
   - src/ - Source code
   - tests/ - Test files
   - logs/ - Audit and application logs
   - config/ - Configuration files
   - docs/ - Documentation
   - examples/ - Example code

⚠️  Important:
   • Review README.md for explicit limitations
   • Run tests to verify functionality
   • Check module documentation for scope
   • All modules follow test-driven development

🎯 Core Principle:
   "Don't claim what hasn't been built.
    Don't claim what hasn't been tested.
    Don't hide what the implementation cannot do."
"""
    print(summary)

def main():
    """Main execution"""
    print("\n" + "="*70)
    print("SWI V1 Module 1-10 - Setup and Extraction")
    print("="*70)
    
    # Check if zip exists
    zip_file = 'swi_v1_part1_source.zip'
    if not os.path.exists(zip_file):
        print(f"\n❌ ERROR: {zip_file} not found in current directory")
        print(f"Available files: {os.listdir('.')}")
        sys.exit(1)
    
    # Execute setup steps
    success = True
    
    if not extract_zip(zip_file):
        success = False
    
    if success:
        create_directory_structure()
        
        try:
            create_config_files()
        except Exception as e:
            print(f"⚠️  Config creation issue: {e}")
        
        create_env_file()
        create_requirements_file()
        
        if verify_installation():
            print_summary()
        else:
            print("\n⚠️  Some files are missing, but setup continues...")
            print_summary()

if __name__ == '__main__':
    main()
