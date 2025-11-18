@echo off
REM AI Code Agent Dashboard - Windows Startup Script

echo.
echo ╔═══════════════════════════════════════════════════╗
echo ║    🤖 AI Code Agent Dashboard - Startup         ║
echo ║       Smart Local Code Assistant                 ║
echo ╚═══════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    echo Add Python to PATH during installation
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% detected
echo.

REM Create venv if it doesn't exist
if not exist "venv" (
    echo → Creating virtual environment...
    python -m venv venv
)

REM Activate venv
echo → Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
if not exist ".venv_installed" (
    echo → Installing dependencies...
    pip install -q -r requirements.txt
    type nul > .venv_installed
    echo ✓ Dependencies installed
) else (
    echo ✓ Dependencies already installed
)

REM Start backend
echo.
echo ✓ Starting backend server...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
start "" python backend/main.py

REM Wait for backend to start
timeout /t 3 /nobreak

echo.
echo ✓ AI Code Agent is ready!
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo Next steps:
echo 1. Open your browser and go to:
echo    http://localhost:8000
echo.
echo 2. Start using the AI Code Agent:
echo    - Chat with the AI agent
echo    - Analyze your code
echo    - Capture and understand screens
echo.
echo 3. Keyboard shortcuts:
echo    - Ctrl+K: Focus chat input
echo    - Ctrl+Enter: Send message
echo    - Ctrl+S: Save chat history
echo.
echo Press Ctrl+C in the backend window to stop the server
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

pause
