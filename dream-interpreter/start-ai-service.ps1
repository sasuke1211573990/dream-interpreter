# AI Service Startup Script
$ErrorActionPreference = "Continue"

Write-Host "Starting AI Service..." -ForegroundColor Green
Write-Host "Working Directory: $PWD" -ForegroundColor Yellow

$aiPath = Join-Path $PSScriptRoot "ai\inference\app.py"
Write-Host "AI Service Path: $aiPath" -ForegroundColor Yellow

if (Test-Path $aiPath) {
    Write-Host "Found AI service file. Starting..." -ForegroundColor Green
    Set-Location (Split-Path $aiPath)
    python app.py
} else {
    Write-Host "Error: AI service file not found at $aiPath" -ForegroundColor Red
    Write-Host "Current directory: $PWD" -ForegroundColor Yellow
    Get-ChildItem -Recurse -Filter "app.py" | Select-Object FullName
}
