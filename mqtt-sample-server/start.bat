@echo off
chcp 65001 >nul
echo ========================================
echo   MQTT Server Starter
echo ========================================
echo.

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    echo Please make sure venv directory exists.
    pause
    exit /b 1
)
echo ✓ Virtual environment activated.中文
echo.

echo [2/3] Starting MQTT Server...
echo.

python mqtt_server.py

echo.
echo MQTT Server has been stopped.
pause
