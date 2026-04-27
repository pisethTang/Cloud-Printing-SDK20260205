# 🚀 云打印协议快速开始

## ✅ 已完成的功能

根据云打印协议文档，已成功实现以下接口：

### 🔗 核心协议接口

1. **`POST /query`** - 查询和报告状态请求
2. **`POST /result`** - 报告打印结果  
3. **`POST /add_print_job`** - 添加打印任务(测试用)
4. **`GET /printer_status/{printer_id}`** - 获取打印机状态(测试用)

---

## 🏃‍♂️ 立即开始

### 1. 启动服务器

```bash
# 进入项目目录
cd e:/Project/OEM/CloudPrint/demos/httpserver-fastapi

# 启动云打印服务
venv\Scripts\python.exe demo_app.py
```

### 2. 查看API文档

打开浏览器访问：
- 🌐 主页: http://localhost:8000
- 📖 完整文档: http://localhost:8000/docs
- 🔴 ReDoc: http://localhost:8000/redoc

### 3. 测试协议功能

```bash
# 运行云打印协议测试
venv\Scripts\python.exe test_cloud_print.py
```

---

## 🧪 快速测试

### 基础功能验证

```bash
# PowerShell中测试

# 1. 添加打印任务
$body = @{
    printer_id = "0e22311e"
    data = "Hello Cloud Print Protocol Test!"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/add_print_job" -Method POST -Body $body -ContentType "application/json"

# 2. 模拟打印机查询(需要计算签名)
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

## 📋 协议要点

### 🔐 签名计算

**查询接口签名公式:**
```
sourceStr = "printerId={printerId}&status={status}&version={version}{sign_key}"
sign = base64(sha256(sourceStr))
```

**结果报告签名公式:**
```
sourceStr = "printerId={printerId}&bussinessId={bussinessId}&status={status}{sign_key}"
sign = base64(sha256(sourceStr))
```

### 📊 支持的打印机状态

- `OK` - 打印作业完成
- `ONLINE` - 打印机正常
- `BUSY` - 打印机忙碌
- `NOPAPER` - 无纸
- `RUNOUTOF` - 纸张将用完
- `COVEROPEN` - 纸盒盖打开
- `OVERHEART` - 过热
- `CUTERROR` - 切刀错误

### 📡 响应类型

**成功响应(JSON):**
```json
{
    "code": 0,
    "message": "OK"
}
```

**打印数据响应(Binary):**
```
Content-Type: application/octet-stream
Data-Type: raw
Bussiness-Id: 20251201_abc12345
[二进制打印数据]
```

---

## 🎯 测试场景

### 场景1: 正常打印流程

1. 客户端添加打印任务 → `POST /add_print_job`
2. 打印机查询状态 → `POST /query` (返回打印数据)
3. 打印机报告结果 → `POST /result`

### 场景2: 错误处理

1. ❌ 签名错误 → 返回 `{"code": 1, "message": "sign error"}`
2. ❌ 打印机不存在 → 返回 `{"code": 2, "message": "no printer"}`
3. ❌ 无效状态 → Pydantic验证拒绝请求

---

## 🔧 开发信息

### 📁 项目文件

```
demo_app.py              # 主应用文件，包含云打印协议接口
test_cloud_print.py      # 协议测试脚本
CLOUD_PRINT_API.md       # 完整API文档
CLOUD_PRINT_QUICK_START.md  # 本快速开始指南
```

### 🛠️ 技术特性

- ✅ **FastAPI异步框架** - 高性能API服务器
- ✅ **Pydantic V2验证** - 自动数据验证和序列化
- ✅ **SHA256签名验证** - 安全的数据传输
- ✅ **标准错误响应** - 统一的错误处理格式
- ✅ **完整测试套件** - 自动化协议验证

### 🔍 调试技巧

1. **查看请求日志** - 服务器启动后显示所有请求详情
2. **使用Swagger UI** - http://localhost:8000/docs 可直接测试
3. **检查签名计算** - 测试脚本中有完整的签名计算示例
4. **监控响应头** - 打印数据时响应头包含业务ID

---

## 🎉 完成！

现在您拥有一个完整的云打印协议服务器：

- ✅ **协议兼容** - 完全符合云打印协议规范
- ✅ **安全可靠** - SHA256签名验证
- ✅ **高性能** - 异步FastAPI框架
- ✅ **易测试** - 完整测试工具
- ✅ **好文档** - 详细API文档

**开始云打印通信吧！** 🚀