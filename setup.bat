@echo off
REM DGW Scrapper Setup Script for Windows
REM This script helps you set up the DGW Scrapper environment

echo =============================
echo DGW Scrapper Setup Script
echo =============================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo Python %python_version% found
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo Dependencies installed
echo.

REM Install Playwright browsers
echo Installing Playwright browsers...
playwright install chromium
echo Playwright browsers installed
echo.

REM Create output directory
echo Creating output directory...
if not exist output mkdir output
echo Output directory created
echo.

REM Setup complete
echo =============================
echo Setup complete!
echo =============================
echo.
echo To use DGW Scrapper:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run the scraper: python main.py --email YOUR_EMAIL --password YOUR_PASSWORD --from_date DD/MM/YYYY --to_date DD/MM/YYYY
echo.
echo Example:
echo python main.py --email user@example.com --password pass123 --from_date 01/01/2024 --to_date 31/01/2024
echo.
echo For more information, see README.md
echo.
pause
