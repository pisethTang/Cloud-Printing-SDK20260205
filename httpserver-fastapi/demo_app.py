from fastapi import FastAPI, HTTPException, Response, APIRouter
from pydantic import BaseModel, Field, field_validator
import uvicorn
import hashlib
import base64
import secrets
from datetime import datetime

from fastapi.responses import FileResponse



# Cloud print protocol data models


class PrinterQueryRequest(BaseModel):
    """Printer query status request"""
    printerId: str = Field(..., min_length=1,
                           max_length=32, description="Unique device ID")
    version: str = Field(..., max_length=32, description="Printer firmware version")
    status: str = Field(..., max_length=32, description="Printer status")
    sign: str = Field(..., description="SHA256 signature string")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid_statuses = ["OK", "ONLINE", "BUSY", "NOPAPER",
                          "RUNOUTOF", "COVEROPEN", "OVERHEART", "CUTERROR"]
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v


class PrinterResultRequest(BaseModel):
    """Printer result report request"""
    printerId: str = Field(..., min_length=1,
                           max_length=32, description="Unique device ID")
    bussinessId: str = Field(..., min_length=1,
                             max_length=32, description="Business ID")
    status: str = Field(..., max_length=32, description="Printer status")
    sign: str = Field(..., description="SHA256 signature string")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid_statuses = ["OK", "ONLINE", "BUSY", "NOPAPER",
                          "RUNOUTOF", "COVEROPEN", "OVERHEART", "CUTERROR"]
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v


class PrinterQueryResponse(BaseModel):
    """Printer query response"""
    code: int = Field(..., ge=0, le=1, description="0 success, 1 failure")
    message: str = Field(..., description="Operation type or error message")


class PrintDataResponse(BaseModel):
    """Print data response"""
    code: int = Field(..., ge=0, le=1, description="0 success, 1 failure")
    message: str = Field(..., description="Operation type or error message")


# Simulated printer database
printers_db = {
    "0e22311e": {
        "id": "0e22311e",
        "version": "LP112C-100-100",
        "status": "OK",
        "sign_key": "Tkr5^d@mzCuT5!_L",  # Signature key stored in the printer
        "business_id": None
    }
}

# Pending print data storage
print_jobs_db = {}


# Helper functions


def verify_printer_sign(printer_id: str, version: str, status: str, sign: str) -> bool:
    """
    Verify printer query request signature

    sourStr = "printerId={printer_id}&status={status}&version={version}{sign_key}"
    sign = sha256_hash(sourStr)
    base_sign = base64(sign)
    """
    printer = printers_db.get(printer_id)
    if not printer:
        return False

    sign_key = printer["sign_key"]
    source_str = f"printerId={printer_id}&status={status}&version={version}{sign_key}"

    # Calculate SHA256 hash
    hash_obj = hashlib.sha256(source_str.encode('utf-8'))
    hash_bytes = hash_obj.digest()  # Get binary hash result
    
    # Directly Base64 encode the binary result
    calculated_sign = base64.b64encode(hash_bytes).decode('utf-8')
    print(f"Calculated signature: {calculated_sign}")
    return calculated_sign == sign


def verify_result_sign(printer_id: str, business_id: str, status: str, sign: str) -> bool:
    """
    Verify printer result request signature

    sourStr = "printerId={printer_id}&bussinessId={business_id}&status={status}{sign_key}"
    sign = sha256_hash(sourStr)
    base_sign = base64(sign)
    """
    printer = printers_db.get(printer_id)
    if not printer:
        return False
    # hello
    sign_key = printer["sign_key"]
    source_str = f"printerId={printer_id}&bussinessId={business_id}&status={status}{sign_key}"

    # Calculate SHA256 hash
    hash_obj = hashlib.sha256(source_str.encode('utf-8'))
    hash_bytes = hash_obj.digest()  # Get binary hash result
    
    # Directly Base64 encode the binary result
    calculated_sign = base64.b64encode(hash_bytes).decode('utf-8')
    print(f"Calculated signature: {calculated_sign}")
    return calculated_sign == sign


def generate_business_id() -> str:
    """Generate business ID"""
    return f"{datetime.now().strftime('%Y%m%d')}_{secrets.token_hex(8)}"

# Request model for adding print jobs


class AddPrintJobRequest(BaseModel):
    printer_id: str = Field(..., min_length=1,
                            max_length=32, description="Printer ID")
    data: str = Field(..., description="Print data")


# Create FastAPI application instance
app = FastAPI(
    title="Cloud Print Protocol API",
    description="FastAPI application implementing cloud print protocol HTTP interfaces",
    version="1.0.0",
    docs_url="/fastapi/docs",  # Swagger UI path
    redoc_url="/fastapi/redoc",  # ReDoc path
    openapi_url="/fastapi/openapi.json"  # OpenAPI specification path
)




# Create APIRouter, all endpoints will have the /fastapi prefix
api_router = APIRouter(prefix="/fastapi")





# GET interface - root path
@api_router.get("/", summary="Root path", tags=["System"])
async def root():
    """Root path, returns API information"""
    return {
        "message": "Cloud Print Protocol API Service",
        "version": "1.0.0",
        "docs": "/docs"
    }



# Serving favicon locally
@app.get("/fastapi/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.svg", media_type="image/svg+xml")



# GET interface - FastAPI info
@api_router.get("/info", summary="FastAPI info", tags=["System"])
async def fastapi_info():
    """Returns FastAPI framework related information"""
    return {
        "framework": "FastAPI",
        "version": "0.104.0",
        "description": "High-performance, modern Python web framework",
        "features": [
            "Automatic API documentation generation",
            "Type hint support",
            "Asynchronous request handling",
            "OpenAPI specification",
            "Data validation",
            "Dependency injection"
        ],
        "docs_url": "/fastapi/docs",
        "redoc_url": "/fastapi/redoc",
        "openapi_url": "/fastapi/openapi.json",
        "note": "API docs have been moved under the /fastapi prefix"
    }

# 1. Query and report status request interface


@api_router.post("/query", summary="Query and report status request", tags=["Cloud Print Protocol"])
async def printer_query(request: PrinterQueryRequest):
    """
    Printer query status interface
    Receives printer status report and returns print data
    """
    printer_id = request.printerId
    version = request.version
    status = request.status
    sign = request.sign

    print(
        f"Printer query request: printerId={printer_id}, version={version}, status={status}")

    # Verify signature
    if not verify_printer_sign(printer_id, version, status, sign):
        return PrinterQueryResponse(code=1, message="sign error").model_dump()

    # Check if printer exists
    if printer_id not in printers_db:
        return PrinterQueryResponse(code=2, message="no printer").model_dump()

    # Update printer status
    printers_db[printer_id]["status"] = status
    printers_db[printer_id]["version"] = version

    print(f"Printer status:{printers_db} ==== {printers_db[printer_id]}")

    # Check if there is pending print data
    if printer_id in print_jobs_db and print_jobs_db[printer_id]:
        job_data = print_jobs_db[printer_id].pop(0)  # Get and remove the first task
        # Generate business ID
        business_id = generate_business_id()
        printers_db[printer_id]["business_id"] = business_id
        print(f"Print data: has = {job_data}")

        # Read doc/response.bin file as print data
        try:
            with open("./doc/response.bin", "rb") as f:
                print_data = f.read()

            # Return print data (raw format)
            return Response(
                content=print_data,
                media_type="application/octet-stream",
                headers={
                    "Content-Type": "application/octet-stream",
                    "Data-Type": "raw",
                    "Bussiness-Id": business_id
                }
            )
        except FileNotFoundError:
            return PrinterQueryResponse(code=1, message="print data file not found").model_dump()
    else:
        # No print data, return JSON response
        print(f"Print data: none")
        return PrinterQueryResponse(code=0, message="OK").model_dump()


@api_router.post("/result", summary="Report print result", tags=["Cloud Print Protocol"])
async def printer_result(request: PrinterResultRequest):
    """
    Printer result report interface
    Receives printer execution result report
    """
    printer_id = request.printerId
    business_id = request.bussinessId
    status = request.status
    sign = request.sign

    print(
        f"Printer result report: printerId={printer_id}, businessId={business_id}, status={status}")

    # Verify signature
    if not verify_result_sign(printer_id, business_id, status, sign):
        return PrinterQueryResponse(code=1, message="sign error").model_dump()

    # Check if printer exists
    if printer_id not in printers_db:
        return PrinterQueryResponse(code=2, message="no printer").model_dump()

    # Process result report
    if status == "OK":
        print(f"Print job {business_id} completed")
        return PrinterQueryResponse(code=0, message="OK").model_dump()
    elif status == "BUSY":
        print(f"Printer {printer_id} busy")
        return PrinterQueryResponse(code=0, message="OK").model_dump()
    elif status in ["NOPAPER", "RUNOUTOF", "COVEROPEN", "OVERHEART", "CUTERROR"]:
        print(f"Printer {printer_id} error: {status}")
        return PrinterQueryResponse(code=0, message="OK").model_dump()
    else:
        print(f"Printer {printer_id} unknown status: {status}")
        return PrinterQueryResponse(code=0, message="OK").model_dump()
# Test interface - Add print job (for testing)


@api_router.post("/add_print_job", summary="Add print job (test)", tags=["Cloud Print Protocol"])
async def add_print_job(request: AddPrintJobRequest):
    """
    Add print job to specified printer
    For testing cloud print protocol functionality
    """
    printer_id = request.printer_id
    data = request.data

    if printer_id not in printers_db:
        raise HTTPException(status_code=404, detail="Printer does not exist")

    # Add to print job queue
    if printer_id not in print_jobs_db:
        print_jobs_db[printer_id] = []

    print_jobs_db[printer_id].append({
        "data": data,
        "timestamp": datetime.now().isoformat(),
        "id": len(print_jobs_db[printer_id])
    })

    return {
        "message": "Print job added successfully",
        "printer_id": printer_id,
        "job_count": len(print_jobs_db[printer_id])
    }

# Test interface - Get printer status


@api_router.get("/printer_status/{printer_id}", summary="Get printer status (test)", tags=["Cloud Print Protocol"])
async def get_printer_status(printer_id: str):
    """
    Get current status of specified printer
    For testing and debugging
    """
    if printer_id not in printers_db:
        raise HTTPException(status_code=404, detail="Printer does not exist")

    printer = printers_db[printer_id]

    return {
        "printer_id": printer_id,
        "status": printer["status"],
        "version": printer["version"],
        "business_id": printer["business_id"],
        "pending_jobs": len(print_jobs_db.get(printer_id, []))
    }


# Include APIRouter in the application
app.include_router(api_router)


if __name__ == "__main__":
    print("🚀 Starting cloud print protocol API server...")
    print("📱 Access address: http://localhost:8800")
    print("📖 API docs: http://localhost:8800/fastapi/docs")

    uvicorn.run(
        "demo_app:app",
        host="0.0.0.0",
        port=8800,
        reload=True,
        log_level="info"
    )
