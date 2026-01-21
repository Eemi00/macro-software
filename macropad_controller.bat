@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please follow installation steps in README.md
    pause
    exit /b 1
)
call .venv\Scripts\activate
start "" pythonw app\main.py