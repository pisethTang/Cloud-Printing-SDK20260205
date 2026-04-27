# Cloud Print Protocol API Documentation

## 🌐 Interface Overview

FastAPI interfaces implemented based on the cloud print protocol documentation, supporting printer status queries, print data transfer, and result reporting functions.

### 📋 Interface List

| Interface | Method | Path | Function |
|-----------|--------|------|----------|
| Query Status | POST | `/query` | Printer query and status reporting |
| Report Result | POST | `/result` | Printer result reporting |
| Add Job | POST | `/add_print_job` | Add print job (for testing) |
| Get Status | GET | `/printer_status/{printer_id}` | Get printer status (for testing) |

---

## 🔐 Interface Details

### 1. Query and Report Status Request

**POST** `/query`

The printer sends a status report to the server and requests print data.

#### Request Headers
```
Content-Type: application/json
```

#### Request Body
```json
{
    "printerId": "0e22311e",
    "version": "LP112C-100-100", 
    "status": "OK",
    "sign": "nZrWMCV8UmDrb/3v+IEF1csN/FK5mZF7Y+y6oQAIGpg="
}
```

**Parameter Description:**
| Parameter | Type | Length Limit | Description |
|-----------|------|--------------|-------------|
| `printerId` | string | 1-32 characters | Unique device ID |
| `version` | string | 1-32 characters | Printer firmware version |
| `status` | string | 1-32 characters | Printer status |
| `sign` | string | - | SHA256 signature |

#### Supported Printer Status
- `OK` - Print job completed (raw data format)
- `ONLINE` - Printer status normal
- `BUSY` - Printer is printing job
- `NOPAPER` - Printer out of paper
- `RUNOUTOF` - Printer paper running low (special models)
- `COVEROPEN` - Printer cover opened
- `OVERHEART` - Printer overheated
- `CUTERROR` - Printer cutter error

#### Response

**Normal Response (JSON format):**
```json
{
    "code": 0,
    "message": "OK"
}
```

**Print Data Response (RAW format):**
```
Content-Type: application/octet-stream
Data-Type: raw
Bussiness-Id: 20251201_a1b2c3d4
```

**Error Response:**
```json
{
    "code": 1,
    "message": "sign error"
}
```

```json
{
    "code": 2,
    "message": "no printer"
}
```

#### Signature Calculation Method

```python
import hashlib
import base64

# Signature string construction
source_str = f"printerId={printerId}&status={status}&version={version}{sign_key}"

# SHA256 hash
hash_obj = hashlib.sha256(source_str.encode('utf-8'))
calculated_hash = hash_obj.hexdigest()

# Base64 encoding
sign = base64.b64encode(calculated_hash.encode('utf-8')).decode('utf-8')
```

---

### 2. Report Print Result

**POST** `/result`

The printer reports the execution result of the print task to the server.

#### Request Body
```json
{
    "printerId": "0e22311e",
    "bussinessId": "20251201_a1b2c3d4",
    "status": "OK", 
    "sign": "JbHcxjEATcWtzrjeSnr3UWy6VKEoFuu18QlcPxVevlg="
}
```

**Parameter Description:**
| Parameter | Type | Length Limit | Description |
|-----------|------|--------------|-------------|
| `printerId` | string | 1-32 characters | Unique device ID |
| `bussinessId` | string | 1-32 characters | Business ID (obtained from query response) |
| `status` | string | 1-32 characters | Execution result status |
| `sign` | string | - | SHA256 signature |

#### Response

```json
{
    "code": 0,
    "message": "OK"
}
```

#### Signature Calculation Method

```python
# Signature string construction
source_str = f"printerId={printerId}&bussinessId={bussinessId}&status={status}{sign_key}"

# SHA256 + Base64
sign = calculate_sign(source_str)
```

---

### 3. Test Interfaces

#### Add Print Job

**POST** `/add_print_job`

For testing purposes, adds a print job to the specified printer.

```json
{
    "printer_id": "0e22311e",
    "data": "This is test print data"
}
```

#### Get Printer Status

**GET** `/printer_status/{printer_id}`

View the current status and number of pending print jobs for the specified printer.

```json
{
    "printer_id": "0e22311e",
    "status": "OK",
    "version": "LP112C-100-100",
    "business_id": "20251201_a1b2c3d4",
    "pending_jobs": 2
}
```

---

## 🧪 Testing

### Running Test Scripts

```bash
# Start server
python demo_app.py

# Run tests
python test_cloud_print.py
```

### Test Scenarios

1. **Basic Functionality Tests**
   - Printer query
   - Result reporting
   - Signature verification

2. **Error Scenario Tests**
   - Invalid signature
   - Unknown printer
   - Invalid status

3. **Complete Workflow Tests**
   - Add print job
   - Printer query (returns data)
   - Result reporting
   - Query again (no data)

### Test Data

```python
# Test printer configuration
TEST_PRINTER_ID = "0e22311e"
TEST_SIGN_KEY = "Tkr5^d@mzCuT5!_L"

# Example signature calculation
sign = calculate_printer_sign(
    printer_id="0e22311e",
    status="OK", 
    version="LP112C-100-100",
    sign_key="Tkr5^d@mzCuT5!_L"
)
# Result: "nZrWMCV8UmDrb/3v+IEF1csN/FK5mZF7Y+y6oQAIGpg="
```

---

## 🔧 Development Notes

### Data Models

```python
class PrinterQueryRequest(BaseModel):
    printerId: str = Field(..., min_length=1, max_length=32)
    version: str = Field(..., max_length=32)
    status: str = Field(..., max_length=32)
    sign: str = Field(...)

class PrinterResultRequest(BaseModel):
    printerId: str = Field(..., min_length=1, max_length=32)
    bussinessId: str = Field(..., min_length=1, max_length=32)
    status: str = Field(..., max_length=32)
    sign: str = Field(...)

class PrinterQueryResponse(BaseModel):
    code: int = Field(..., ge=0, le=1)
    message: str = Field(...)
```

### Security Features

- ✅ **Signature Verification** - SHA256 + Base64 ensures data integrity
- ✅ **Input Validation** - Strict data format and length limits
- ✅ **Error Handling** - Standardized error response format
- ✅ **Status Validation** - Only accepts predefined printer statuses

### Performance Optimization

- ✅ **Async Processing** - High-performance async framework based on FastAPI
- ✅ **In-Memory Storage** - Fast print job queue management
- ✅ **Type Validation** - Pydantic V2 automatic data validation

---

## 📱 Usage Examples

### JavaScript/TypeScript

```typescript
// Query print data
const queryData = {
    printerId: "0e22311e",
    version: "LP112C-100-100",
    status: "OK",
    sign: calculateSign(...)
};

const response = await fetch('/query', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(queryData)
});

// Check response type
if (response.headers.get('content-type').includes('application/octet-stream')) {
    // Handle print data
    const printData = await response.arrayBuffer();
    const businessId = response.headers.get('bussiness-id');
} else {
    // Handle JSON response
    const result = await response.json();
}
```

### Python

```python
import requests

# Query print data
query_data = {
    "printerId": "0e22311e",
    "version": "LP112C-100-100", 
    "status": "OK",
    "sign": calculate_sign(...)
}

response = requests.post("http://localhost:8000/query", json=query_data)

if response.headers.get('content-type') == 'application/octet-stream':
    # Handle print data
    print_data = response.content
    business_id = response.headers.get('bussiness-id')
else:
    # Handle JSON response
    result = response.json()
```

---

## 🎉 Summary

Complete cloud print protocol implementation, including:

- ✅ **Standard Protocol Support** - Fully compliant with documentation specifications
- ✅ **Signature Verification** - Secure data transmission
- ✅ **Status Management** - Complete printer status handling
- ✅ **Error Handling** - Standardized response format
- ✅ **Testing Tools** - Complete test suite
- ✅ **API Documentation** - Detailed interface description

Now you can start cloud print communication with printer devices!
