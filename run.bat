@echo off
echo Starting MT5 Data Downloader...

:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in your system PATH!
    echo Please install Python from https://www.python.org/downloads/
    echo IMPORTANT: Make sure to check the box "Add Python to PATH" during installation.
    pause
    exit /b
)

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual Python environment [this keeps things clean]...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate

:: Install requirements
echo Installing/Checking required packages...
pip install -r requirements.txt -q

:: Check if .env exists, if not, copy .env.example
if not exist ".env" (
    echo Creating default .env file...
    copy .env.example .env
)

:: Run script
echo Running MT5 Downloader...
echo ==================================================
python mt5_downloader.py

echo.
echo Process complete.
pause
