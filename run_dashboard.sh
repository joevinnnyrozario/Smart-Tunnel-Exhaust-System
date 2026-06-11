#!/bin/bash

# Tunnel Exhaust System Dashboard Launcher for Linux/Mac

echo ""
echo "===================================="
echo "Tunnel Exhaust System - Flask Dashboard"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ using your package manager"
    exit 1
fi

echo "[*] Python found: $(python3 --version)"
echo ""

# Check if dependencies are installed
echo "[*] Checking dependencies..."
python3 -m pip show Flask > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[!] Dependencies not installed"
    echo "[*] Installing dependencies from requirements_dashboard.txt..."
    python3 -m pip install -r requirements_dashboard.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

echo "[+] All dependencies installed"
echo ""

# Start the Flask app
echo "[*] Starting Flask Dashboard Server..."
echo "[*] Dashboard will be available at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
