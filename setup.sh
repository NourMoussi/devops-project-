#!/bin/bash
# ============================================
# Task Manager API - Setup Script (Linux/Mac)
# ============================================
# Description: Automated setup script for development environment
# Platform: Linux/macOS (Bash)
# ============================================

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  Task Manager API - Setup Script${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Check Python installation
echo -e "${YELLOW}[1/5] Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Found: $PYTHON_VERSION${NC}"
    
    # Check if Python version is 3.9+
    VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if (( $(echo "$VERSION < 3.9" | bc -l) )); then
        echo -e "${RED}✗ Error: Python 3.9+ required, found $VERSION${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Error: Python3 not found. Please install Python 3.9+${NC}"
    exit 1
fi

echo ""

# Create virtual environment
echo -e "${YELLOW}[2/5] Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}! Virtual environment already exists, skipping...${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created successfully${NC}"
fi

echo ""

# Activate virtual environment
echo -e "${YELLOW}[3/5] Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

echo ""

# Upgrade pip
echo -e "${YELLOW}[4/5] Upgrading pip...${NC}"
python -m pip install --upgrade pip --quiet
echo -e "${GREEN}✓ pip upgraded successfully${NC}"

echo ""

# Install dependencies
echo -e "${YELLOW}[5/5] Installing dependencies from requirements.txt...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ All dependencies installed successfully${NC}"

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${GREEN}  Setup Complete! 🎉${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "${NC}  1. Activate the virtual environment:${NC}"
echo -e "${CYAN}     source venv/bin/activate${NC}"
echo ""
echo -e "${NC}  2. Run the application (when ready):${NC}"
echo -e "${CYAN}     python app.py${NC}"
echo ""
echo -e "${NC}  3. Run tests (when ready):${NC}"
echo -e "${CYAN}     pytest tests/${NC}"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
echo ""
