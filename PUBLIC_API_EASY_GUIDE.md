# 🌐 راهنمای Public API Server - بدون ngrok

اگر ngrok کار نکند، 2 روش دیگر داریم:

---

## ✅ روش 1: استفاده از Cloudflare Tunnel (رایگان - بهترین)

### Step 1: دانلود Cloudflare Tunnel

```bash
# Download from
https://github.com/cloudflare/cloudflared/releases

# یا با مدیر پکیج
choco install cloudflared  # Windows
brew install cloudflare/cloudflare/cloudflared  # Mac
```

### Step 2: اجرای Server

```bash
# Terminal 1
D:/project/project_payani/2/.venv/Scripts/python.exe mock_server_simple.py
```

### Step 3: ایجاد Tunnel

```bash
# Terminal 2
cloudflared tunnel --url http://localhost:8001
```

**نتیجه:**
```
Tunnel created. Hostname: https://abc1234567.trycloudflare.com
```

### Step 4: استفاده

```dart
// unipath_mobile/lib/config/api_config.dart
static const String publicMockServerUrl = 'https://abc1234567.trycloudflare.com';
static const bool useMockApi = true;
static const bool useHttps = true;
```

---

## ✅ روش 2: Port Forwarding (اگر Router دارید)

### Step 1: IP محلی گیر آورید

```bash
ipconfig
# دنبال: IPv4 Address
# مثال: 192.168.100.104
```

### Step 2: Server شروع کنید

```bash
D:/project/project_payani/2/.venv/Scripts/python.exe mock_server_simple.py
```

**Port forwarding کنید:**
- Router Settings: 192.168.1.1 یا 192.168.0.1
- Port Forwarding:
  - Local IP: 192.168.100.104
  - Local Port: 8001
  - External Port: 8001
  - Protocol: TCP

### Step 3: Public IP را پیدا کنید

```bash
# Google: "what is my ip"
# یا: https://ipinfo.io
# نتیجه: 203.0.113.45
```

### Step 4: استفاده

```dart
static const String publicMockServerUrl = 'http://203.0.113.45:8001';
```

---

## ✅ روش 3: Local Network (ساده‌ترین)

اگر فقط موبایل و PC بر روی همان شبکه هستند:

### Step 1: IP ماشین را بیابید

```bash
ipconfig
# IPv4 Address: 192.168.100.104
```

### Step 2: Server شروع کنید

```bash
D:/project/project_payani/2/.venv/Scripts/python.exe mock_server_simple.py
```

### Step 3: تنظیم App

```dart
static const String mockServerIp = '192.168.100.104';
static const int mockServerPort = 8001;
static const bool useMockApi = true;
```

### Step 4: تست

```bash
# From mobile on same network
curl http://192.168.100.104:8001/api/health
```

---

## 📊 مقایسه

| روش | سختی | رایگان | دسترسی | سرعت |
|-----|------|--------|--------|------|
| Local Network | ⭐ ساده | ✅ | 🏠 شبکه | ⚡⚡⚡ |
| Cloudflare | ⭐⭐ | ✅ | 🌐 عمومی | ⚡⚡ |
| Port Forward | ⭐⭐⭐ | ✅ | 🌐 عمومی | ⚡⚡⚡ |
| ngrok | ⭐ ساده | ❌ (Account) | 🌐 عمومی | ⚡⚡ |

---

## 🎯 توصیه من

**برای شروع:** روش 3 (Local Network)
```bash
python mock_server_simple.py
# و تنظیم IP در api_config.dart
```

**برای عمومی:** روش 1 (Cloudflare)
```bash
# دنلود Cloudflare Tunnel
# اجرا: cloudflared tunnel --url http://localhost:8001
```

---

## 🔗 مثال کامل (Cloudflare)

```bash
# Terminal 1 - Server
D:/project/project_payani/2/.venv/Scripts/python.exe mock_server_simple.py

# Terminal 2 - Tunnel
cloudflared tunnel --url http://localhost:8001

# خروجی:
# Tunnel created. Hostname: https://abc1234567.trycloudflare.com
```

**App Config:**
```dart
class ApiConfig {
  static const bool useMockApi = true;
  static const bool useHttps = true;
  static const String publicMockServerUrl = 'https://abc1234567.trycloudflare.com';
}
```

**تست:**
```bash
curl https://abc1234567.trycloudflare.com/api/health
```

---

## 📱 استفاده کمال

### Step 1: Server شروع کنید

```bash
python mock_server_simple.py
```

### Step 2: Tunnel (Cloudflare)

```bash
cloudflared tunnel --url http://localhost:8001
```

### Step 3: Copy URL

```
https://abc1234567.trycloudflare.com
```

### Step 4: Update Config

```dart
// api_config.dart
static const String publicMockServerUrl = 'https://abc1234567.trycloudflare.com';
static const bool useHttps = true;
```

### Step 5: تست

```bash
flutter run
```

**اکنون تمام دنیا می‌تواند API را استفاده کند!** 🌐

---

## 🛠️ نکات

- ✅ Server مستقل است
- ✅ Cloudflare رایگان است
- ✅ HTTPS خودکار
- ✅ بدون Account
- ✅ سریع است

---

**انتخاب کنید و شروع کنید!** 🚀
