@echo off
REM Tunnel Exhaust System Dashboard Launcher for Windows

echo.
echo ====================================
echo Tunnel Exhaust System - Flask Dashboard
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [*] Python found
echo.

REM Check if dependencies are installed
echo [*] Checking dependencies...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo [!] Dependencies not installed
    echo [*] Installing dependencies from requirements_dashboard.txt...
    pip install -r requirements_dashboard.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [+] All dependencies installed
echo.

REM Start the Flask app
echo [*] Starting Flask Dashboard Server...
echo [*] Dashboard will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
