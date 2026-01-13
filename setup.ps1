# ============================================
# Task Manager API - Setup Script (Windows)
# ============================================
# Description: Automated setup script for development environment
# Platform: Windows (PowerShell)
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Task Manager API - Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
    $pythonVersion = python --version
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Error: Python not found. Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Create virtual environment
Write-Host "[2/5] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "! Virtual environment already exists, skipping..." -ForegroundColor Yellow
} else {
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Virtual environment created successfully" -ForegroundColor Green
    } else {
        Write-Host "✗ Error: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# Virtual environment note
Write-Host "[3/5] Virtual environment setup complete" -ForegroundColor Yellow
Write-Host "! Using virtual environment for package installation" -ForegroundColor Yellow

Write-Host ""

# Upgrade pip
Write-Host "[4/5] Upgrading pip..." -ForegroundColor Yellow
& ".\venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ pip upgraded successfully" -ForegroundColor Green
} else {
    Write-Host "! Warning: Failed to upgrade pip (continuing anyway)" -ForegroundColor Yellow
}

Write-Host ""

# Install dependencies
Write-Host "[5/5] Installing dependencies from requirements.txt..." -ForegroundColor Yellow
Write-Host "! This may take a few minutes..." -ForegroundColor Yellow
& ".\venv\Scripts\pip.exe" install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ All dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Error: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete! 🎉" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Activate the virtual environment:" -ForegroundColor White
Write-Host "     .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "  2. Run the application (when ready):" -ForegroundColor White
Write-Host "     python app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "  3. Run tests (when ready):" -ForegroundColor White
Write-Host "     pytest tests/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Green
Write-Host ""
