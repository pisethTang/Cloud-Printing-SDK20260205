# HTTP(S) Cloud Print Protocol

| Version | Date | Instructions |
| --- | --- | --- |
| V1.1 | 2025.12.01 | Improve the agreement section |
| V1.0 | 2025.04.17 | Create documentation initially |

> **Note:**
> - This cloud printing protocol is implemented based on the method where the printer sends a request and the server responds.
> - There are two ways for the client to request. The first one is to request the printing of data and the reporting of status. The second type is to report the status of the printing task.

---

# 1. Query and Report Status Request

```plain
URL: /query
Method: POST
Request data type: application/json
Response data type: application/json
```

## 1.1 Client Request

### Request Header

No specification.

### Request Body

| Parameter | Type | Restraint | Instructions |
| --- | --- | --- | --- |
| `printerId` | String | 1 to 32 char | Unique device ID, customer factory default value, can also be set with the tool later |
| `version` | String | 1 to 32 char | Printer firmware |
| `status` | String | 1 to 32 char | [**OK**](#3-printer-status) — status normal |
| `sign` | String | — | SHA256 signature string, used to verify the client |

#### Sign Calculation Method

> The red part is the current printer setting value, and the blue part is the signature key.

```
sourStr = "printerId=0e22311e&status=OK&version=LP112C-100-100Tkr5^d@mzCuT5!_L";
sign = sha256_hash(sourStr);
base_sign = base64(sign);
```

- `0e22311e` — printer setting value (example)
- `OK` — status value (example)
- `LP112C-100-100` — version value (example)
- `Tkr5^d@mzCuT5!_L` — signature key

### Request Samples

```json
{
    "printerId": "0e22311e",
    "status": "OK",
    "version": "LP112C-100-100",
    "sign": "nZrWMCV8UmDrb/3v+IEF1csN/FK5mZF7Y+y6oQAIGpg="
}
```

> **Notice:**
> - The signature key has been stored in the printer, and can be set through the settings tool.
> - This API will send the printer status report and the request for print data to the server together. It will request server data at regular intervals, and the request interval can also be set.
> - If the printer's status changes, for example, from normal to no paper, it will immediately call the interface to report the status.

## 1.2 Server Response

### Header

#### Normal

```
Content-Type: application/json
```

#### Print Data

```
Content-Type: application/octet-stream
Data-Type: raw
Bussiness-Id: xxxx-xxxxxxx
```

### Body

> If the response header is `raw`, that is, the print data format, then the body is pure print data. No further introduction is needed here.

#### Common Parameters

| Parameter | Type | Restraint |
| --- | --- | --- |
| `code` | Int | `0` — success<br>`1` — failure |
| `message` | String | if code `0` — operation type<br>if code `1` — error message |

#### Response Samples

```json
{
  "code": 0,
  "message": "OK"
}
```

### Error Response

#### Signature Mismatch

```json
{
    "code": 1,
    "message": "sign error"
}
```

#### Printer Not Configured

```json
{
    "code": 2,
    "message": "no printer"
}
```

---

# 2. Report Print Result

```plain
URL: /result
Method: POST
Request data type: application/json
Response data type: application/json
```

## 2.1 Client Request

### Request Header

No specification.

### Request Body

| Parameter | Type | Restraint | Instructions |
| --- | --- | --- | --- |
| `printerId` | String | 1 to 32 char | Unique device ID, customer factory default value, can also be set with the tool later |
| `bussinessId` | String | 1 to 32 char | Get from header of server response |
| `status` | String | 1 to 32 char | [**OK**](#3-printer-status) |
| `sign` | String | — | SHA256 signature string, used to verify the client |

> **Notice:**
> - The signature key has been stored in the printer, and can be set through the settings tool.
> - If the printer is functioning properly, the print will be executed. In other states, it is considered that the printer is faulty and the task needs to be resent.

### Request Samples

```json
{
    "printerId": "0e22311e",
    "bussinessId": "db0775e9-dd16-4555-8da6-5d1ee43b722b",
    "status": "OK",
    "sign": "JbHcxjEATcWtzrjeSnr3UWy6VKEoFuu18QlcPxVevlg="
}
```

#### Sign Calculation Method

> The red part is the current printer setting value, and the blue part is the signature key.

```
sourStr = "printerId=0e22311e&bussinessId=db0775e9-dd16-4555-8da6-5d1ee43b722b&status=OKTkr5^d@mzCuT5!_L";
sign = sha256_hash(sourStr);
base_sign = base64(sign);
```

- `0e22311e` — printer setting value (example)
- `db0775e9-dd16-4555-8da6-5d1ee43b722b` — business ID (example)
- `OK` — status value (example)
- `Tkr5^d@mzCuT5!_L` — signature key

## 2.2 Server Response

> Please refer to Section [1.2 Server response](#12-server-response).

---

# 3. Printer Status

| Status | Instruction |
| --- | --- |
| `OK` | Print job complete (raw data format) |
| `ONLINE` | Printer status OK |
| `BUSY` | Printer is in print job |
| `NOPAPER` | Printer no paper |
| `RUNOUTOF` | The paper of the printer is running out soon, valid on special models |
| `COVEROPEN` | The paper bin cover of the printer is opened |
| `OVERHEART` | The printer is overheating |
| `CUTERROR` | The printer's cutter is incorrect |
