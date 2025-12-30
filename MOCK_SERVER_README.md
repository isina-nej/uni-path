# Mock API Server - Unipath Project

**تاریخ ایجاد:** 27 دسامبر 2025  
**نسخه:** 1.0  
**وضعیت:** ✅ تمام تست‌ها موفق (12/12)

---

## 📋 فهرست

1. [توضیح](#توضیح)
2. [فایل‌های اصلی](#فایل‌های-اصلی)
3. [نحوه اجرا](#نحوه-اجرا)
4. [API Endpoints](#api-endpoints)
5. [تنظیمات](#تنظیمات)
6. [بهینه‌سازی‌ها](#بهینه‌سازی‌ها)

---

## 📝 توضیح

این Mock API Server برای تست‌کردن Front-end بدون نیاز به سرور Django درست شده است.

**مزایا:**
- ✅ هیچ وابستگی خارجی نیازی نیست (فقط Python استاندارد)
- ✅ شروع سریع
- ✅ CORS فعال برای موبایل
- ✅ JSON مستقل‌الذات
- ✅ تمام endpoints پیاده‌سازی شده

---

## 📁 فایل‌های اصلی

### 1. Mock Server
**فایل:** `mock_server_simple.py`

```python
# اجرا
python mock_server_simple.py

# یا
D:/project/project_payani/2/.venv/Scripts/python.exe mock_server_simple.py
```

**پورت:** 8001  
**آدرس:** http://localhost:8001/api

### 2. Mock Database
**فایل:** `backend/mock_api_db.json`

شامل تمام داده‌های Mock:
- Users
- Courses
- Enrollments
- Grades
- Recommendations
- Statistics

### 3. API Test Script
**فایل:** `test_api_simple.py`

```python
# اجرا
python test_api_simple.py
```

تست تمام 12 endpoint و نمایش نتایج.

### 4. Configuration
**فایل:** `unipath_mobile/lib/config/api_config.dart`

```dart
class ApiConfig {
  // Mock یا Real API
  static const bool useMockApi = true;
  
  // تنظیمات
  static const String mockServerIp = 'localhost';
  static const int mockServerPort = 8001;
}
```

---

## 🚀 نحوه اجرا

### روش 1: اجرای دستی

```bash
# Terminal 1 - Mock Server
cd d:\project\project_payani\2
D:/project/project_payani/2/.venv/Scripts/python.exe mock_server_simple.py

# Terminal 2 - Test
cd d:\project\project_payani\2
D:/project/project_payani/2/.venv/Scripts/python.exe test_api_simple.py
```

### روش 2: استفاده از Batch File (Windows)

```batch
@echo off
cd /d d:\project\project_payani\2
D:/project/project_payani/2/.venv/Scripts/python.exe mock_server_simple.py
```

### روش 3: از VS Code

1. **Terminal منو** → **New Terminal**
2. وارد کنید: `python mock_server_simple.py`
3. Enter فشار دهید

---

## 🔌 API Endpoints

### Health & Info
```http
GET /api/health
GET /api
```

**Response:**
```json
{
  "status": "ok",
  "message": "Mock API Server is running",
  "version": "1.0"
}
```

### Authentication
```http
POST /api/auth/login
POST /api/auth/refresh
GET  /api/auth/user
POST /api/auth/register
```

### Courses
```http
GET /api/courses
GET /api/courses/{id}
```

### Enrollments
```http
GET  /api/enrollments
POST /api/enrollments
```

### Grades
```http
GET /api/grades
GET /api/students/{id}/grades
```

### Recommendations
```http
GET /api/recommendations
```

### Statistics & Users
```http
GET /api/statistics
GET /api/students
```

---

## ⚙️ تنظیمات

### تغییر پورت

**فایل:** `mock_server_simple.py`

```python
def main():
    port = 8001  # تغییر اینجا
    server = HTTPServer(('0.0.0.0', port), MockAPIHandler)
```

### تغییر Host

برای شبکه محلی فقط:
```python
server = HTTPServer(('localhost', port), MockAPIHandler)
```

برای تمام شبکه‌ها:
```python
server = HTTPServer(('0.0.0.0', port), MockAPIHandler)
```

### اضافه‌کردن Endpoints جدید

در `mock_server_simple.py`:

```python
elif path == '/api/new-endpoint':
    data = {'message': 'response'}
    return self.send_json_response(data)
```

### تغییر Mock Data

**فایل:** `backend/mock_api_db.json`

ویرایش JSON و سرور را دوباره شروع کنید.

---

## 🔍 بهینه‌سازی‌ها

### 1. CORS
- ✅ فعال برای تمام Origins
- ✅ Methods: GET, POST, PUT, DELETE, OPTIONS
- ✅ Headers: Content-Type, Authorization

### 2. Encoding
- ✅ UTF-8 پشتیبانی (فارسی)
- ✅ JSON proper formatting

### 3. Performance
- ✅ بدون database overhead
- ✅ In-memory responses
- ✅ Fast response times

### 4. Error Handling
- ✅ Status codes مناسب
- ✅ Error messages
- ✅ CORS on errors

---

## 📊 نتایج تست

```
╔══════════════════════════════════════════════════════╗
║  تست Mock API Server - Unipath Project             ║
║  زمان: 2025-12-27 22:53:32                         ║
╚══════════════════════════════════════════════════════╝

1️⃣  سلامتی سرور                    ✓ 200 OK
2️⃣  ورود                           ✓ 200 OK
3️⃣  پروفایل                        ✓ 200 OK
4️⃣  دروس                           ✓ 200 OK
5️⃣  درس خاص                        ✓ 200 OK
6️⃣  ثبت‌نام‌ها                      ✓ 200 OK
7️⃣  ثبت‌نام جدید                   ✓ 201 Created
8️⃣  نمرات                         ✓ 200 OK
9️⃣  نمرات دانشجو                   ✓ 200 OK
🔟 توصیه‌ها                       ✓ 200 OK
1️⃣1️⃣  آمار                         ✓ 200 OK
1️⃣2️⃣  دانشجویان                    ✓ 200 OK

✓ موفق: 12/12
💯 درصد: 100%
```

---

## 🛠️ مشکل‌گشایی

### سرور شروع نمی‌شود

```bash
# بررسی Python
python --version

# بررسی virtual environment
.venv\Scripts\activate

# اجرا با verbose
python -u mock_server_simple.py
```

### Port مشغول است

```bash
# Windows - Kill process
taskkill /F /IM python.exe

# یا تغییر پورت در کد
```

### CORS Error

```
❌ No 'Access-Control-Allow-Origin' header
```

Server از قبل CORS را فعال دارد. اگر مشکل هست:

```python
# بررسی کنید
self.send_header('Access-Control-Allow-Origin', '*')
```

---

## 📚 منابع

- [Python HTTP Server](https://docs.python.org/3/library/http.server.html)
- [JSON Format](https://www.json.org/)
- [HTTP Status Codes](https://httpwg.org/specs/rfc9110.html)

---

## 📋 Changelog

**Version 1.0** (27 Dec 2025)
- ✅ Mock Server ایجاد
- ✅ تمام endpoints پیاده‌سازی
- ✅ تست‌ها موفق
- ✅ Mock Database
- ✅ Configuration System

---

## 📝 یادداشت‌ها

1. **برای production:** از این برای production استفاده نکنید. فقط برای تست است.

2. **برای توسعه:** می‌توانید endpoints جدید را اضافه کنید.

3. **برای موبایل:** IP آدرس ماشین را در `api_config.dart` قرار دهید.

4. **برای Django:** تنظیمات CORS در `settings.py` بررسی کنید.

---

**✅ آماده برای استفاده!**
