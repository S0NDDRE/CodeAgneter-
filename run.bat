@echo off
setlocal enabledelayedexpansion

REM AI Code Agent - Windows Startup
REM Simple, direct, no BS

echo.
echo ========================================
echo   AI Code Agent - Chat with Code
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://python.org
    echo (Check "Add Python to PATH" during installation)
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found

REM Create venv
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv >nul 2>&1
)

REM Activate venv
call venv\Scripts\activate.bat >nul 2>&1

REM Install dependencies
if not exist ".installed" (
    echo [*] Installing dependencies (this takes ~30 seconds first time)...
    pip install -q -r requirements.txt
    if errorlevel 1 (
        echo ERROR: pip install failed!
        echo Make sure you have internet and Python is working
        pause
        exit /b 1
    )
    echo. > .installed
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)

echo.
echo [*] Starting AI Code Agent backend...
echo.
echo ========================================
echo Starting server at:
echo   http://localhost:8000
echo.
echo Quit with: Ctrl+C
echo ========================================
echo.

REM Start Python backend
python backend/main.py

pause
