# 📱 راهنمای تست Front-end بر روی موبایل - بدون سرور Backend

## 🎯 خلاصه حل

ما یک **Mock API Server** درست کردیم که فرانت‌اند می‌تواند بدون نیاز به سرور Django آن را تست کند. این حل شامل:

1. ✅ **Mock API Server** - سرور ساده‌ای که تمام API endpoints را شبیه‌سازی می‌کند
2. ✅ **سیستم کانفیگ** - تنظیم آسان بین Mock و Real API
3. ✅ **تست کامل** - تمام 12 API endpoint با موفقیت تست شدند
4. ✅ **شبکه محلی** - قابل استفاده از موبایل بر روی شبکه LAN

---

## 🚀 شروع سریع

### گام 1: فایل‌های ایجادشده

```
✓ mock_server_simple.py   - Mock API Server (پورت 8001)
✓ test_api_simple.py      - اسکریپت تست API
✓ unipath_mobile/lib/config/api_config.dart - سیستم کانفیگ
✓ backend/mock_api_db.json - دیتابیس Mock
```

### گام 2: راه‌اندازی Mock Server

```bash
# در دایرکتوری اصلی پروژه
D:/project/project_payani/2/.venv/Scripts/python.exe mock_server_simple.py
```

**خروجی موفق:**
```
============================================================
🚀 Mock API Server شروع شد
============================================================
📡 آدرس Local: http://localhost:8001
📡 آدرس شبکه: http://0.0.0.0:8001
📱 تست: curl http://localhost:8001/api/health
⚠️  برای توقف: Ctrl+C
============================================================
```

### گام 3: تست تمام API ها

```bash
# در یک ترمینال دیگر
D:/project/project_payani/2/.venv/Scripts/python.exe test_api_simple.py
```

**نتیجه:**
```
✓ موفق: 12
✗ ناموفق: 0
💯 درصد: 100.0%
```

---

## 📱 استفاده از موبایل

### برای تست محلی (Localhost):

**فایل:** `unipath_mobile/lib/config/api_config.dart`

```dart
class ApiConfig {
  // استفاده از Mock API
  static const bool useMockApi = true;  // ✓ فعال
  
  static const String mockServerIp = 'localhost';
  static const int mockServerPort = 8001;
}
```

### برای تست بر روی شبکه (Real Device):

#### مرحله 1: IP آدرس ماشین را پیدا کنید

```bash
# در Windows PowerShell
ipconfig

# دنبال کنید: IPv4 Address یا یک آدرس مثل 192.168.x.x
```

#### مرحله 2: Mock Server را بر روی 0.0.0.0 شروع کنید

Mock Server از قبل بر روی `0.0.0.0:8001` اجرا می‌شود، بنابراین:
- دستگاه‌های دیگر می‌توانند به `http://YOUR_MACHINE_IP:8001` دسترسی داشته باشند

#### مرحله 3: تنظیم Flutter App

`unipath_mobile/lib/config/api_config.dart` را تغییر دهید:

```dart
class ApiConfig {
  // استفاده از Mock API
  static const bool useMockApi = true;
  
  // IP آدرس ماشین سرور را وارد کنید
  static const String mockServerIp = '192.168.100.104';  // مثال
  static const int mockServerPort = 8001;
}
```

#### مرحله 4: App را بر روی موبایل اجرا کنید

```bash
flutter run -d <device_id>
```

---

## 🔄 تبدیل به Real API

برای استفاده از سرور واقعی Django:

### مرحله 1: تنظیم Django Server

```bash
# Terminal 1 - Backend
cd backend
python manage.py runserver 0.0.0.0:8000
```

### مرحله 2: تغییر کانفیگ

`unipath_mobile/lib/config/api_config.dart`:

```dart
class ApiConfig {
  // استفاده از Real API
  static const bool useMockApi = false;  // ✓ غیرفعال
  
  // IP آدرس سرور Django
  static const String serverIp = '192.168.100.104';  // IP ماشین
  static const int serverPort = 8000;
}
```

### مرحله 3: Update DioClient

`unipath_mobile/lib/services/dio_client.dart` از `ApiConfig.baseUrl` استفاده می‌کند:

```dart
_dio = Dio(BaseOptions(
  baseUrl: ApiConfig.baseUrl,  // استفاده از کانفیگ
  // ...
));
```

---

## 📊 Endpoints Mock API

### تمام Endpoints قابل دسترسی:

```
✓ GET  /api/health                   - سلامتی سرور
✓ POST /api/auth/login               - ورود
✓ GET  /api/auth/user                - پروفایل کاربر
✓ GET  /api/courses                  - لیست دروس
✓ GET  /api/courses/{id}             - درس خاص
✓ GET  /api/enrollments              - ثبت‌نام‌های دانشجو
✓ POST /api/enrollments              - ثبت‌نام در درس جدید
✓ GET  /api/grades                   - نمرات
✓ GET  /api/students/{id}/grades     - نمرات دانشجو
✓ GET  /api/recommendations          - توصیه‌های دروس
✓ GET  /api/statistics               - آمار دانشجو
✓ GET  /api/students                 - لیست دانشجویان
```

---

## 🔧 اصلاح Mock Data

دیتا‌های Mock در فایل زیر ذخیره شده:

```
backend/mock_api_db.json
```

### ساختار:

```json
{
  "users": [...],
  "auth": {...},
  "courses": [...],
  "enrollments": [...],
  "grades": [...],
  "recommendations": [...],
  "statistics": {...}
}
```

**برای تغییر دیتا:**

1. `mock_api_db.json` را ویرایش کنید
2. Mock Server را دوباره شروع کنید
3. تست کنید

---

## 🛠️ برطرف‌کردن مشکلات

### مشکل: "Connection refused"

```
❌ Error: Connection refused at 127.0.0.1:8001
```

**حل:**
1. Mock Server اجرا می‌شود؟ → `python mock_server_simple.py`
2. API Config صحیح است؟ → `api_config.dart` را بررسی کنید
3. Firewall مسدود نکرده؟ → Firewall را بررسی کنید

### مشکل: CORS Error (موبایل)

```
❌ CORS policy: No 'Access-Control-Allow-Origin' header
```

**حل:**
Mock Server از قبل CORS را فعال دارد.
برای Real API، تأیید کنید:

```python
# backend/unipath/settings.py
CORS_ALLOW_ALL_ORIGINS = True  # ✓ فعال
```

### مشکل: Port قبلاً مشغول است

```
❌ Address already in use: ('0.0.0.0', 8001)
```

**حل:**
```bash
# Kill existing process
taskkill /F /IM python.exe

# یا تغییر پورت در mock_server_simple.py
port = 8002  # پورت جدید
```

---

## 📝 خلاصه نتایج تست

| Test | نتیجه | Status |
|------|-------|--------|
| سلامتی سرور | ✓ | 200 OK |
| ورود | ✓ | 200 OK |
| پروفایل | ✓ | 200 OK |
| دروس | ✓ | 200 OK |
| درس خاص | ✓ | 200 OK |
| ثبت‌نام‌ها | ✓ | 200 OK |
| ثبت‌نام جدید | ✓ | 201 Created |
| نمرات | ✓ | 200 OK |
| نمرات دانشجو | ✓ | 200 OK |
| توصیه‌ها | ✓ | 200 OK |
| آمار | ✓ | 200 OK |
| دانشجویان | ✓ | 200 OK |
| **کل** | **12/12** | **100%** |

---

## ✨ مزایا

✅ **تست بدون Backend** - تست UI بدون سرور  
✅ **Mock Data واقعی** - داده‌های نزدیک به محیط واقعی  
✅ **تبدیل آسان** - یک تنظیم برای تبدیل  
✅ **CORS فعال** - برای موبایل و Web  
✅ **سرعت بالا** - Mock Server بسیار سریع است  
✅ **آسان برای توسعه** - استفاده و تغییر آسان  

---

## 📚 منابع اضافی

- [Flutter Networking Documentation](https://flutter.dev/docs/development/data-and-backend/networking)
- [Dio Package](https://pub.dev/packages/dio)
- [Django CORS Headers](https://github.com/adamchainz/django-cors-headers)

---

**✅ همه چیز آماده است! اکنون می‌توانید فرانت‌اند را بر روی موبایل تست کنید.**
