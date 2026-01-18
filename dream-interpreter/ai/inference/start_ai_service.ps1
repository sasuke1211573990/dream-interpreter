# AI Service Startup Script with Proxy Fix
$ErrorActionPreference = "Continue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting AI Service" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Disable proxy settings
Write-Host "Disabling proxy settings..." -ForegroundColor Yellow
$env:HTTP_PROXY = $null
$env:HTTPS_PROXY = $null
$env:http_proxy = $null
$env:https_proxy = $null
$env:ALL_PROXY = $null
$env:all_proxy = $null
$env:NO_PROXY = "*"
$env:no_proxy = "*"

Write-Host "Proxy settings cleared." -ForegroundColor Green
Write-Host ""

# Change to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "Current directory: $PWD" -ForegroundColor Yellow
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python version: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "Starting AI service..." -ForegroundColor Green
Write-Host "This may take a few minutes for first-time model download." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the service." -ForegroundColor Yellow
Write-Host ""

# Start the service
python app.py
