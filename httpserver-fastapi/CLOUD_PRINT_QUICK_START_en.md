# 🚀 Cloud Print Protocol Quick Start

## ✅ Completed Features

Based on the cloud print protocol documentation, the following interfaces have been successfully implemented:

### 🔗 Core Protocol Interfaces

1. **`POST /query`** - Query and report status request
2. **`POST /result`** - Report print result
3. **`POST /add_print_job`** - Add print job (for testing)
4. **`GET /printer_status/{printer_id}`** - Get printer status (for testing)

---

## 🏃‍♂️ Get Started Now

### 1. Start the Server

```bash
# Enter project directory
cd e:/Project/OEM/CloudPrint/demos/httpserver-fastapi

# Start cloud print service
venv\Scripts\python.exe demo_app.py
```

### 2. View API Documentation

Open browser and visit:
- 🌐 Homepage: http://localhost:8000
- 📖 Full Docs: http://localhost:8000/docs
- 🔴 ReDoc: http://localhost:8000/redoc

### 3. Test Protocol Functions

```bash
# Run cloud print protocol tests
venv\Scripts\python.exe test_cloud_print.py
```

---

## 🧪 Quick Testing

### Basic Functionality Verification

```bash
# Testing in PowerShell

# 1. Add print job
$body = @{
    printer_id = "0e22311e"
    data = "Hello Cloud Print Protocol Test!"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/add_print_job" -Method POST -Body $body -ContentType "application/json"

# 2. Simulate printer query (signature calculation required)
$version = "LP112C-100-100"
$status = "OK" 
$signKey = "Tkr5^d@mzCuT5!_L"
$sourceStr = "printerId=0e22311e&status=$status&version=$version$signKey"

$bytes = [System.Text.Encoding]::UTF8.GetBytes($sourceStr)
$sha256 = [System.Security.Cryptography.SHA256]::Create().ComputeHash($bytes)
$hash = [System.BitConverter]::ToString($sha256).Replace("-", "").ToLower()
$sign = [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($hash))

$queryBody = @{
    printerId = "0e22311e"
    version = $version
    status = $status
    sign = $sign
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/query" -Method POST -Body $queryBody -ContentType "application/json"
```

---

## 📋 Protocol Highlights

### 🔐 Signature Calculation

**Query Interface Signature Formula:**
```
sourceStr = "printerId={printerId}&status={status}&version={version}{sign_key}"
sign = base64(sha256(sourceStr))
```

**Result Report Signature Formula:**
```
sourceStr = "printerId={printerId}&bussinessId={bussinessId}&status={status}{sign_key}"
sign = base64(sha256(sourceStr))
```

### 📊 Supported Printer Status

- `OK` - Print job completed
- `ONLINE` - Printer normal
- `BUSY` - Printer busy
- `NOPAPER` - Out of paper
- `RUNOUTOF` - Paper running low
- `COVEROPEN` - Cover opened
- `OVERHEART` - Overheated
- `CUTERROR` - Cutter error

### 📡 Response Types

**Success Response (JSON):**
```json
{
    "code": 0,
    "message": "OK"
}
```

**Print Data Response (Binary):**
```
Content-Type: application/octet-stream
Data-Type: raw
Bussiness-Id: 20251201_abc12345
[binary print data]
```

---

## 🎯 Test Scenarios

### Scenario 1: Normal Print Flow

1. Client adds print job → `POST /add_print_job`
2. Printer queries status → `POST /query` (returns print data)
3. Printer reports result → `POST /result`

### Scenario 2: Error Handling

1. ❌ Signature error → Returns `{"code": 1, "message": "sign error"}`
2. ❌ Printer not found → Returns `{"code": 2, "message": "no printer"}`
3. ❌ Invalid status → Pydantic validation rejects request

---

## 🔧 Development Information

### 📁 Project Files

```
demo_app.py              # Main application file, contains cloud print protocol interfaces
test_cloud_print.py      # Protocol test script
CLOUD_PRINT_API.md       # Complete API documentation
CLOUD_PRINT_QUICK_START.md  # This quick start guide
```

### 🛠️ Technical Features

- ✅ **FastAPI Async Framework** - High-performance API server
- ✅ **Pydantic V2 Validation** - Automatic data validation and serialization
- ✅ **SHA256 Signature Verification** - Secure data transmission
- ✅ **Standard Error Response** - Unified error handling format
- ✅ **Complete Test Suite** - Automated protocol verification

### 🔍 Debugging Tips

1. **View Request Logs** - Server shows all request details after startup
2. **Use Swagger UI** - http://localhost:8000/docs for direct testing
3. **Check Signature Calculation** - Complete signature calculation examples in test script
4. **Monitor Response Headers** - Response headers contain business ID when returning print data

---

## 🎉 Done!

Now you have a complete cloud print protocol server:

- ✅ **Protocol Compatible** - Fully compliant with cloud print protocol specifications
- ✅ **Secure and Reliable** - SHA256 signature verification
- ✅ **High Performance** - Async FastAPI framework
- ✅ **Easy to Test** - Complete testing tools
- ✅ **Good Documentation** - Detailed API documentation

**Start cloud print communication now!** 🚀
