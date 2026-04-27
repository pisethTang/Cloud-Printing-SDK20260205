# Cloud Printing SDK

This repository contains two main components of the Cloud Printing SDK: 

- the **printer client setup tools** (Windows), and 
- the **cloud print server reference implementation** (FastAPI).

---

## Folder Overview

### `Cloud setup tool 20250708/`

Windows-based client tools used to configure printers and connect them to the cloud print service.

| Subfolder / File | Purpose |
|------------------|---------|
| `ClientCloudToolsV2.3/` | .NET client configuration tool for registering printers with the cloud server. Includes localized resource DLLs (`en-US`, `zh-CN`, `zh-Hans`, `byn`). |
| `CloudPrintTools/` | .NET 6.0 runtime tools for cloud print operations. |
| `Setting tools 2024.06.13/` | Standalone Windows utility (`SetTools.exe`) for configuring printer hardware settings, logs, and device parameters. |
| `ClientCloudToolsV2.4.zip` | Archived version of the client tools. |
| `HCCTG cloud server address.txt` | Default cloud server endpoint (`printsrv.quickticket.cn`). |

> **Note:** These are compiled Windows binaries and runtime dependencies (`PortIO.dll`, `vcruntime140.dll`, etc.). They are distributed as-is and are intended to run on the client PC that manages the printers.

---

### `httpserver-fastapi/`

Python reference implementation of the HTTP(S) Cloud Print Protocol server built with **FastAPI**.

| File | Purpose |
|------|---------|
| `demo_app.py` | Main application. Implements the cloud print protocol endpoints (`/query`, `/result`, `/add_print_job`, `/printer_status/{printer_id}`) with SHA256 signature verification, job queuing, and raw binary data responses. |
| `check_routes.py` | Utility script that lists and verifies all registered FastAPI routes. |
| `requirements.txt` | Python dependencies: `fastapi`, `uvicorn`, `pydantic`. |
| `CLOUD_PRINT_API.md` / `CLOUD_PRINT_API_en.md` | Full API documentation (Chinese and English). |
| `CLOUD_PRINT_QUICK_START.md` / `CLOUD_PRINT_QUICK_START_en.md` | Quick-start guide for running and testing the server. |
| `doc/HTTP(s) cloud print protocol.md` | Original protocol specification document. |
| `doc/response.bin` | Sample binary payload returned to printers when a print job is available. |

#### Quick Start

```bash
cd httpserver-fastapi
pip install -r requirements.txt
python demo_app.py
```

The server starts on `http://localhost:8800`. API documentation is available at `http://localhost:8800/fastapi/docs`.

#### Protocol Summary

Printers poll the server via `POST /fastapi/query` to report their status and request print jobs. If a job exists, the server responds with raw binary data (`application/octet-stream`). After printing, the printer reports the result via `POST /fastapi/result`. All printer requests are authenticated with a per-device SHA256 + Base64 signature.

---

## Architecture

```
┌─────────────────────────┐         HTTP(S)          ┌─────────────────────────┐
│   Printer (Hardware)    │  ◄────────────────────►  │  Cloud Print Server     │
│                         │   POST /query (status)   │  (httpserver-fastapi)   │
│  - Firmware: LP112C     │   POST /result (report)  │  - FastAPI + Uvicorn    │
│  - Sign key stored      │                          │  - In-memory job queue  │
│    on device            │                          │  - SHA256 signatures    │
└─────────────────────────┘                          └─────────────────────────┘
         ▲                                                    ▲
         │                                                    │
         │         Configured via                             │   Jobs added via
         └────────  Cloud setup tools  ───────────────────────┘   POST /add_print_job
                   (Windows client utilities)
```
