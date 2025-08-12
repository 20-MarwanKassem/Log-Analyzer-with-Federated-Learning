@echo off
echo Starting Log Analyzer GUI...

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking required packages...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Error installing required packages.
    pause
    exit /b 1
)

REM Start the application
echo Starting application...
python log_analyzer_gui.py
if %ERRORLEVEL% NEQ 0 (
    echo Error starting Log Analyzer GUI.
    echo Please check the error message above.
    pause
    exit /b 1
)

pause 