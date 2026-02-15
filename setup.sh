#!/bin/bash

echo "========================================"
echo "RSVP Reader - Setup Script"
echo "========================================"
echo ""

echo "[1/4] Checking Python installation..."
python3 --version || python --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi
echo ""

echo "[2/4] Creating virtual environment..."
python3 -m venv venv || python -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi
echo ""

echo "[3/4] Activating virtual environment..."
source venv/bin/activate
echo ""

echo "[4/4] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo ""

echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "To start the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run: python backend/main.py"
echo "3. Open browser: http://localhost:8000"
echo ""
echo "Or simply run: ./run.sh"
echo ""
