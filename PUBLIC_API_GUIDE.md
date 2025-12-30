# 🌐 Public API Server - دسترسی از انترنت

**تاریخ:** 27 دسامبر 2025  
**وضعیت:** ✅ آماده برای استفاده عمومی

---

## 🎯 سه روش برای Public Access

### ✅ راه 1: ngrok (سادهترین - توصیه شده)

#### Step 1: نصب ngrok

```bash
# Automatic install
pip install pyngrok

# یا
pip install pyngrok requests
```

#### Step 2: اجرا

```bash
# With ngrok
D:/project/project_payani/2/.venv/Scripts/python.exe mock_server_public.py --ngrok
```

**خروجی:**
```
🚀 Mock API Server - Public Edition
============================================================

🌐 Setting up ngrok for public access...
✓ ngrok library found
✅ ngrok Tunnel Active!
🌐 Public URL: https://abc1234-def567.ngrok.io
📍 Local URL: http://localhost:8001
🔗 Test: https://abc1234-def567.ngrok.io/api/health
```

#### Step 3: استفاده

**در Flutter App:**
```dart
// unipath_mobile/lib/config/api_config.dart
static const String mockServerIp = 'abc1234-def567.ngrok.io';  // URL ngrok
static const int mockServerPort = 443;  // HTTPS port
static const bool useHttps = true;
```

**یا از هر جا:**
```bash
curl https://abc1234-def567.ngrok.io/api/health
```

---

### ✅ راه 2: Port Forwarding (برای دسترسی دائم)

#### Step 1: IP ثابت گیر آورید

```bash
ipconfig  # دنبال: IPv4 Address
```

#### Step 2: Router تنظیم کنید

1. وارد Settings شوید: `192.168.1.1` یا `192.168.0.1`
2. Port Forwarding پیدا کنید
3. تنظیمات:
   - **Local IP:** `192.168.100.104` (IP شما)
   - **Local Port:** `8001`
   - **External Port:** `8001` (یا هر پورت دیگر)
   - **Protocol:** TCP

#### Step 3: اجرا

```bash
# Local server
python mock_server_simple.py
```

#### Step 4: استفاده

**Public IP را بیابید:**
```bash
# Google: "what is my ip"
# یا: https://ipinfo.io
```

**در App:**
```dart
static const String mockServerIp = '203.0.113.45';  // Public IP
static const int mockServerPort = 8001;
```

---

### ✅ راه 3: Cloud Hosting (برای Production)

#### گزینه‌های پیشنهادی:

**1. Heroku (رایگان)**
```bash
heroku login
heroku create unipath-api
git push heroku main
```

**2. Render (رایگان)**
```bash
# Deploy شده به render.com
```

**3. Railway (رایگان)**
```bash
railway up
```

**4. PythonAnywhere (رایگان)**
```
www.pythonanywhere.com
```

---

## 📊 مقایسه روش‌ها

| روش | سرعت | امنیت | دسترسی | هزینه |
|-----|------|-------|---------|-------|
| ngrok | ⚡⚡ بالا | 🔒🔒 خوب | 🌐 فوری | 💰 رایگان |
| Port Forwarding | ⚡⚡⚡ بسیار | 🔒 خوب | 🌐 دائم | 💰 رایگان |
| Cloud (Render) | ⚡ معمولی | 🔒🔒🔒 عالی | 🌐 دائم | 💰 رایگان |
| Cloud (Heroku) | ⚡ معمولی | 🔒🔒🔒 عالی | 🌐 دائم | 💰 $7/mo |

---

## 🚀 استفاده ngrok (بهترین برای شروع)

### تک دستور:

```bash
D:/project/project_payani/2/.venv/Scripts/python.exe mock_server_public.py --ngrok
```

### نتیجه:

```
✅ ngrok Tunnel Active!
🌐 Public URL: https://abc1234-def567.ngrok.io

✅ بلافاصله قابل دسترسی!
✅ دسترسی از هر جا
✅ HTTPS خودکار
✅ رایگان
```

---

## 🔧 پیشرفته: شخصی‌سازی

### Port تغییر دهید:

```bash
# Port 9000
python mock_server_public.py --port 9000 --ngrok
```

### Host خاص:

```bash
# فقط localhost
python mock_server_public.py --host localhost

# یا 0.0.0.0 (پیش‌فرض)
python mock_server_public.py --host 0.0.0.0
```

### بدون ngrok:

```bash
# صرفاً local
python mock_server_public.py
```

---

## 📱 تست Public API

### از Mobile:

```dart
// 1. Get public URL
// 2. Update config
static const String mockServerIp = 'public-url-here';

// 3. Run app
flutter run
```

### از Command Line:

```bash
# Local
curl http://localhost:8001/api/health

# Public (ngrok)
curl https://abc1234-def567.ngrok.io/api/health

# Public (port forwarding)
curl http://203.0.113.45:8001/api/health
```

---

## 🔒 امنیت

### ⚠️ توجه:

- ngrok URL تغییر می‌کند (یا نیاز به حساب برای دسترسی ثابت)
- Port Forwarding عمومی هست
- رمز‌ها محفوظ نیستند (Mock است)

### برای Production:

```bash
# HTTPS استفاده کنید
# Database محفوظ کنید
# Authentication قوی کنید
# Logging فعال کنید
```

---

## 🎯 سناریو‌ها

### ✅ سناریو 1: دانشجویان دورافتاده

```
PC Server (Mock API)
        ↓
   ngrok tunnel
        ↓
   Public HTTPS URL
        ↓
Mobile (دانشجو)
   ✓ تست کند
   ✓ بدون VPN
   ✓ بدون Setup پیچیده
```

### ✅ سناریو 2: تست بین تیم

```
Developer A (Windows)
        ↓
ngrok Public URL
        ↓
Developer B (Mac/Linux) ✓
Developer C (Mobile)    ✓
Tester (Any Device)     ✓
```

### ✅ سناریو 3: Integration Test

```
CI/CD Pipeline
        ↓
Public API URL
        ↓
API Tests ✓
Integration Tests ✓
```

---

## 📚 مثال‌های بیشتر

### تست Postman:

```
1. Postman باز کنید
2. URL: https://abc1234-def567.ngrok.io/api/health
3. Send کنید
4. Response: {"status": "ok", ...}
```

### تست Python:

```python
import requests

url = 'https://abc1234-def567.ngrok.io/api/health'
response = requests.get(url)
print(response.json())
```

### تست JavaScript:

```javascript
fetch('https://abc1234-def567.ngrok.io/api/health')
  .then(r => r.json())
  .then(data => console.log(data))
```

---

## 🆘 مشکل‌گشایی

### ngrok کار نمی‌کند

```bash
# دوباره نصب کنید
pip uninstall pyngrok
pip install pyngrok requests
```

### URL معطل است

```bash
# Restart
Ctrl+C
# Run again
python mock_server_public.py --ngrok
```

### Port مشغول است

```bash
# Port دیگر استفاده کنید
python mock_server_public.py --ngrok --port 9000
```

---

## 📝 Quick Reference

```bash
# Local
python mock_server_simple.py

# Public with ngrok
python mock_server_public.py --ngrok

# Custom port
python mock_server_public.py --ngrok --port 9000

# Test health
curl http://localhost:8001/api/health

# View ngrok status
# Open: http://localhost:4040
```

---

## 🎉 خلاصه

**3 مرحله برای Public Access:**

1. **نصب:** `pip install pyngrok`
2. **اجرا:** `python mock_server_public.py --ngrok`
3. **استفاده:** Copy URL و استفاده کنید

**بس! اکنون API عمومی است!** 🌐

---

**نکات:**
- ✅ ngrok رایگان است
- ✅ HTTPS خودکار
- ✅ بدون پیچیدگی
- ✅ برای تست عالی است

**Let's go public! 🚀**
