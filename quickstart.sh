#!/bin/bash
# SWI V1 Module 1-10 - Quick Start Script
# Automated setup and configuration

set -e

echo "========================================="
echo "SWI V1 Module 1-10 - Quick Start Setup"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Step 1: Checking prerequisites...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi
echo -e "${GREEN}✅ Python 3 found: $(python3 --version)${NC}"

echo ""
echo -e "${BLUE}Step 2: Creating virtual environment...${NC}"
if [ ! -d "swi_env" ]; then
    python3 -m venv swi_env
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
fi

echo ""
echo -e "${BLUE}Step 3: Activating virtual environment...${NC}"
source swi_env/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

echo ""
echo -e "${BLUE}Step 4: Upgrading pip...${NC}"
pip install --quiet --upgrade pip
echo -e "${GREEN}✅ Pip upgraded${NC}"

echo ""
echo -e "${BLUE}Step 5: Installing dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip install --quiet -r requirements.txt
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  requirements.txt not found${NC}"
fi

echo ""
echo -e "${BLUE}Step 6: Extracting source code...${NC}"
if [ -f "swi_v1_part1_source.zip" ]; then
    if command -v unzip &> /dev/null; then
        unzip -oq swi_v1_part1_source.zip
        echo -e "${GREEN}✅ Source code extracted${NC}"
    else
        python3 -m zipfile -e swi_v1_part1_source.zip .
        echo -e "${GREEN}✅ Source code extracted (using Python)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  swi_v1_part1_source.zip not found${NC}"
fi
# Extraction is flat: this creates ./swi_core/ and ./test_swi_core.py
# in the current directory -- there is no swi_v1_part1_source/ subfolder.

echo ""
echo -e "${BLUE}Step 7: Creating configuration files...${NC}"
mkdir -p config logs .swi_temp
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ Created .env from template${NC}"
fi
echo -e "${GREEN}✅ Configuration directories created${NC}"

echo ""
echo -e "${BLUE}Step 8: Verifying installation...${NC}"
echo "Python version: $(python3 --version)"
echo "Installed packages:"
pip list --quiet | grep -E "pytest|cryptography|pyyaml" || true

echo ""
echo -e "${BLUE}Step 9: Running verification tests...${NC}"
if [ -f "test_swi_core.py" ] && [ -d "swi_core" ]; then
    if python3 -m pytest test_swi_core.py -v --tb=short; then
        echo -e "${GREEN}✅ Tests executed - all passing${NC}"
    else
        echo -e "${RED}❌ Tests failed - see output above${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ test_swi_core.py or swi_core/ not found - extraction did not complete${NC}"
    exit 1
fi

echo ""
echo "========================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "========================================="
echo ""
echo "📋 Next Steps:"
echo "   1. Activate virtual environment:"
echo "      source swi_env/bin/activate"
echo ""
echo "   2. Run the full test suite (from this directory):"
echo "      python3 -m pytest test_swi_core.py -v"
echo ""
echo "   3. Generate a coverage report:"
echo "      python3 -m pytest test_swi_core.py --cov=swi_core --cov-report=html"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Project overview"
echo "   - SETUP_GUIDE.md - Detailed setup"
echo "   - INSTALLATION.md - Installation steps"
echo ""
echo "🔧 Configuration:"
echo "   - config/swi_config.yaml - module settings reference (not yet read by the code)"
echo "   - .env - environment variable template (not yet read by the code)"
echo ""
echo "Virtual environment: $VIRTUAL_ENV"
echo ""
