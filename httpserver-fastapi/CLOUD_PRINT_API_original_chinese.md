# 云打印协议 API 文档

## 🌐 接口概览

基于云打印协议文档实现的FastAPI接口，支持打印机状态查询、打印数据传输和结果报告功能。

### 📋 接口列表

| 接口 | 方法 | 路径 | 功能 | 标签 |
|------|------|------|------|
| 查询状态 | POST | `/query` | 打印机查询和报告状态 |
| 报告结果 | POST | `/result` | 打印机结果报告 |
| 添加任务 | POST | `/add_print_job` | 添加打印任务(测试用) |
| 获取状态 | GET | `/printer_status/{printer_id}` | 获取打印机状态(测试用) |

---

## 🔐 接口详情

### 1. 查询和报告状态请求

**POST** `/query`

打印机向服务器发送状态报告并请求打印数据。

#### 请求头
```
Content-Type: application/json
```

#### 请求体
```json
{
    "printerId": "0e22311e",
    "version": "LP112C-100-100", 
    "status": "OK",
    "sign": "nZrWMCV8UmDrb/3v+IEF1csN/FK5mZF7Y+y6oQAIGpg="
}
```

**参数说明:**
| 参数 | 类型 | 长度限制 | 说明 |
|------|------|----------|------|
| `printerId` | string | 1-32字符 | 唯一设备ID |
| `version` | string | 1-32字符 | 打印机固件版本 |
| `status` | string | 1-32字符 | 打印机状态 |
| `sign` | string | - | SHA256签名 |

#### 支持的打印机状态
- `OK` - 打印作业完成(原始数据格式)
- `ONLINE` - 打印机状态正常
- `BUSY` - 打印机正在打印作业
- `NOPAPER` - 打印机无纸
- `RUNOUTOF` - 打印机纸张即将用完(特殊型号)
- `COVEROPEN` - 打印机纸盒盖已打开
- `OVERHEART` - 打印机过热
- `CUTERROR` - 打印机切刀错误

#### 响应

**正常响应(JSON格式):**
```json
{
    "code": 0,
    "message": "OK"
}
```

**打印数据响应(RAW格式):**
```
Content-Type: application/octet-stream
Data-Type: raw
Bussiness-Id: 20251201_a1b2c3d4
```

**错误响应:**
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

#### 签名计算方法

```python
import hashlib
import base64

# 签名字符串构造
source_str = f"printerId={printerId}&status={status}&version={version}{sign_key}"

# SHA256哈希
hash_obj = hashlib.sha256(source_str.encode('utf-8'))
calculated_hash = hash_obj.hexdigest()

# Base64编码
sign = base64.b64encode(calculated_hash.encode('utf-8')).decode('utf-8')
```

---

### 2. 报告打印结果

**POST** `/result`

打印机向服务器报告打印任务执行结果。

#### 请求体
```json
{
    "printerId": "0e22311e",
    "bussinessId": "20251201_a1b2c3d4",
    "status": "OK", 
    "sign": "JbHcxjEATcWtzrjeSnr3UWy6VKEoFuu18QlcPxVevlg="
}
```

**参数说明:**
| 参数 | 类型 | 长度限制 | 说明 |
|------|------|----------|------|
| `printerId` | string | 1-32字符 | 唯一设备ID |
| `bussinessId` | string | 1-32字符 | 业务ID(从查询响应获得) |
| `status` | string | 1-32字符 | 执行结果状态 |
| `sign` | string | - | SHA256签名 |

#### 响应

```json
{
    "code": 0,
    "message": "OK"
}
```

#### 签名计算方法

```python
# 签名字符串构造
source_str = f"printerId={printerId}&bussinessId={bussinessId}&status={status}{sign_key}"

# SHA256 + Base64
sign = calculate_sign(source_str)
```

---

### 3. 测试接口

#### 添加打印任务

**POST** `/add_print_job`

用于测试目的，向指定打印机添加打印任务。

```json
{
    "printer_id": "0e22311e",
    "data": "这是测试打印数据"
}
```

#### 获取打印机状态

**GET** `/printer_status/{printer_id}`

查看指定打印机的当前状态和待打印任务数。

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

## 🧪 测试

### 运行测试脚本

```bash
# 启动服务器
python demo_app.py

# 运行测试
python test_cloud_print.py
```

### 测试场景

1. **基础功能测试**
   - 打印机查询
   - 结果报告
   - 签名验证

2. **错误场景测试**
   - 无效签名
   - 未知打印机
   - 无效状态

3. **完整工作流测试**
   - 添加打印任务
   - 打印机查询(返回数据)
   - 结果报告
   - 再次查询(无数据)

### 测试数据

```python
# 测试打印机配置
TEST_PRINTER_ID = "0e22311e"
TEST_SIGN_KEY = "Tkr5^d@mzCuT5!_L"

# 示例签名计算
sign = calculate_printer_sign(
    printer_id="0e22311e",
    status="OK", 
    version="LP112C-100-100",
    sign_key="Tkr5^d@mzCuT5!_L"
)
# 结果: "nZrWMCV8UmDrb/3v+IEF1csN/FK5mZF7Y+y6oQAIGpg="
```

---

## 🔧 开发说明

### 数据模型

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

### 安全特性

- ✅ **签名验证** - SHA256 + Base64确保数据完整性
- ✅ **输入验证** - 严格的数据格式和长度限制
- ✅ **错误处理** - 标准化的错误响应格式
- ✅ **状态验证** - 只接受预定义的打印机状态

### 性能优化

- ✅ **异步处理** - 基于FastAPI的高性能异步框架
- ✅ **内存存储** - 快速的打印任务队列管理
- ✅ **类型验证** - Pydantic V2自动数据验证

---

## 📱 使用示例

### JavaScript/TypeScript

```typescript
// 查询打印数据
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

// 检查响应类型
if (response.headers.get('content-type').includes('application/octet-stream')) {
    // 处理打印数据
    const printData = await response.arrayBuffer();
    const businessId = response.headers.get('bussiness-id');
} else {
    // 处理JSON响应
    const result = await response.json();
}
```

### Python

```python
import requests

# 查询打印数据
query_data = {
    "printerId": "0e22311e",
    "version": "LP112C-100-100", 
    "status": "OK",
    "sign": calculate_sign(...)
}

response = requests.post("http://localhost:8000/query", json=query_data)

if response.headers.get('content-type') == 'application/octet-stream':
    # 处理打印数据
    print_data = response.content
    business_id = response.headers.get('bussiness-id')
else:
    # 处理JSON响应
    result = response.json()
```

---

## 🎉 总结

完整的云打印协议实现，包含：

- ✅ **标准协议支持** - 完全符合文档规范
- ✅ **签名验证** - 安全的数据传输
- ✅ **状态管理** - 完整的打印机状态处理
- ✅ **错误处理** - 标准化响应格式
- ✅ **测试工具** - 完整的测试套件
- ✅ **API文档** - 详细的接口说明

现在可以开始与打印机设备进行云打印通信了！