@echo off
echo Starting MQTT Broker on port 9883...
cd /d "%~dp0"
.venv\Scripts\python.exe mqtt_server.py
pause
