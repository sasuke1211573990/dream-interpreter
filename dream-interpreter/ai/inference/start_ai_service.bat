@echo off
chcp 65001 >nul
echo ========================================
echo Starting AI Service
echo ========================================
echo.

REM Disable proxy settings
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=
set ALL_PROXY=
set all_proxy=
set NO_PROXY=*
set no_proxy=*

echo Proxy settings disabled.
echo.

REM Change to the script directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Starting AI service...
echo This may take a few minutes for first-time model download.
echo.
echo Press Ctrl+C to stop the service.
echo.

python app.py

pause
