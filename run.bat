@echo off
echo Starting RSVP Reader...
echo.
echo Please ensure you have:
echo 1. Installed Python 3.8 or higher
echo 2. Created a virtual environment (optional)
echo 3. Installed dependencies: pip install -r requirements.txt
echo.
echo Starting server on http://localhost:8000
echo.

cd backend
python main.py

pause
