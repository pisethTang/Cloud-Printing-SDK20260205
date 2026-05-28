# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **Cloud Printing SDK** with two active server implementations and Windows client utilities:

- `httpserver-fastapi/` — FastAPI server implementing the HTTP(S) Cloud Print Protocol
- `mqtt-sample-server/` — MQTT broker server for printer communication via MQTT
- `Cloud setup tool 20250708/` — Pre-compiled Windows client tools (binaries, not source)

## Running the Servers

Both projects use `uv` for dependency management. Each has its own `.venv/`.

### HTTP Server (FastAPI)

```powershell
cd httpserver-fastapi
.venv\Scripts\python.exe demo_app.py
```

Server starts on `http://localhost:8900`. Swagger UI: `http://localhost:8900/fastapi/docs`.

The VS Code launch config (`"FastAPI: demo_app (uvicorn)"`) runs it on port **8800** with `--reload`.

To skip printer signature verification during development, set `SKIP_SIGN_VERIFY=1` in `httpserver-fastapi/.env` (already set there).

### MQTT Server

```powershell
cd mqtt-sample-server
# With authentication (default credentials: admin/admin123, user/user123):
.venv\Scripts\python.exe mqtt_server.py

# Without authentication (debugging):
.venv\Scripts\python.exe mqtt_server_noauth.py
```

Listens on `0.0.0.0:9883`. On first run, `mqtt_config.py` auto-generates `passwords.txt` using bcrypt hashes.

### MQTT Test Publisher

```powershell
cd mqtt-sample-server
.venv\Scripts\python.exe test_hello_world.py
```

Publishes an ESC/POS "Hello World" print job to a connected printer. Requires the MQTT server to be running and a printer connected with device ID matching `PRINTER_DEVICE_ID` in the script.

## Architecture

```
Printer Hardware
    │
    ├─── HTTP(S) ──► httpserver-fastapi/demo_app.py
    │                  POST /query   — printer polls for jobs, returns binary ESC/POS data
    │                  POST /result  — printer reports completion
    │                  POST /fastapi/add_print_job — enqueue job (test/dev use)
    │                  GET  /fastapi/printer_status/{id} — check queue (test/dev use)
    │
    └─── MQTT ─────► mqtt-sample-server/mqtt_server.py
                       Broker on :9883
                       Subscribe: /sys/{deviceId}/user/data   ← send print data TO printer
                       Publish:   /sys/{deviceId}/user/status ← receive status FROM printer
```

The HTTP server holds all state in-memory (`printers_db`, `print_jobs_db` dicts). There is no database.

Endpoints are registered twice — once under `/fastapi/` (for Swagger UI and management) and once at the root path `/query`, `/result` (for real printers that use bare paths). Both delegate to the same `_printer_query` / `_printer_result` async functions.

## Protocol Details

**Signature formula (query):**
```
sourceStr = "printerId={id}&status={status}&version={version}{sign_key}"
sign = base64(sha256_binary(sourceStr))
```

**Signature formula (result):**
```
sourceStr = "printerId={id}&bussinessId={bussinessId}&status={status}{sign_key}"
sign = base64(sha256_binary(sourceStr))
```

The SHA256 result is binary-encoded before Base64 (not hex-encoded). This is the correct implementation in `demo_app.py`.

**Binary response:** When a print job is queued, the server responds with `doc/response.bin` as `application/octet-stream` plus headers `Data-Type: raw` and `Bussiness-Id: {id}`.

## Printer Configuration (`config.ini`)

The Windows client tools write `Cloud setup tool 20250708/ClientCloudToolsV2.3/config.ini`. Key fields:

- `[tcpcloud]` — HTTP cloud server URL/port/printer ID
- `[mqtt]` — MQTT broker address, credentials, device ID, topics
- `[http]` — Alternative HTTP endpoint configuration

Default sign key used across all demo printer entries: `Tkr5^d@mzCuT5!_L`

Default MQTT test printer device ID: `111222555`

## Dependencies

- `httpserver-fastapi`: Python ≥3.13, fastapi, uvicorn[standard], pydantic≥2, python-dotenv
- `mqtt-sample-server`: Python ≥3.13, amqtt (async MQTT broker), passlib (password hashing), paho-mqtt (test client)
