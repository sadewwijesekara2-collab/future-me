@echo off
title Future Me - Launcher
color 0b
cd /d "%~dp0"

echo.
echo  ================================
echo   Future Me - Career Navigator
echo  ================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found!
    echo  Install from https://www.python.org/downloads
    pause
    exit /b
)

if not exist ".env" (
    copy ".env.example" ".env" >nul
    echo  [!] Created .env file. Open it, add your OPENROUTER_API_KEY, save, then run this again.
    notepad ".env"
    pause
    exit /b
)

echo  [1/3] Installing dependencies...
pip install -r requirements.txt >nul 2>&1
echo        Done!

echo  [2/3] Starting backend...
start "Future Me - Backend" cmd /k "python app.py"

echo  [3/3] Waiting for server...
timeout /t 3 /nobreak >nul

start http://127.0.0.1:5000

echo.
echo  Future Me is running at http://127.0.0.1:5000
echo  Close the Backend window to stop.
pause
