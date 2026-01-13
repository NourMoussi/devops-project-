@echo off
REM ============================================
REM Task Manager API - Setup Script (Windows)
REM ============================================
REM Description: Automated setup script for development environment
REM Platform: Windows (Batch)
REM ============================================

echo ========================================
echo   Task Manager API - Setup Script
echo ========================================
echo.

REM Check Python installation
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.9+
    exit /b 1
)
python --version
echo [OK] Python found
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist venv (
    echo [INFO] Virtual environment already exists, skipping...
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        exit /b 1
    )
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo [3/5] Setting up virtual environment...
echo [INFO] Virtual environment will be used for installation
echo.

REM Upgrade pip
echo [4/5] Upgrading pip...
venv\Scripts\python.exe -m pip install --upgrade pip --quiet
if %errorlevel% neq 0 (
    echo [WARNING] Failed to upgrade pip, continuing...
)
echo [OK] pip upgraded
echo.

REM Install dependencies
echo [5/5] Installing dependencies from requirements.txt...
echo [INFO] This may take a few minutes...
venv\Scripts\pip.exe install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    exit /b 1
)
echo [OK] All dependencies installed
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate.bat
echo.
echo   2. Run the application (when ready):
echo      python app.py
echo.
echo   3. Run tests (when ready):
echo      pytest tests/
echo.
echo Happy coding!
echo.
pause
