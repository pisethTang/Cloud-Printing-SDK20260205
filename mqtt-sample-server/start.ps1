# MQTT Server PowerShell Starter
# Set UTF-8 encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   MQTT Server Starter" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] Activating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
    Write-Host "✓ Virtual environment activated." -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to activate virtual environment!" -ForegroundColor Red
    Write-Host "Please make sure venv directory exists." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

Write-Host "[2/3] Starting MQTT Server..." -ForegroundColor Yellow
Write-Host ""

try {
    python mqtt_server.py
} catch {
    Write-Host ""
    Write-Host "ERROR: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "MQTT Server has been stopped." -ForegroundColor Gray
Read-Host "Press Enter to exit"
