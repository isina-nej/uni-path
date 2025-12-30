# 📱 Mobile Testing Guide - Test Frontend Without Backend Server

## 🎯 Solution Summary

We've created a **Mock API Server** that allows the frontend to be tested without a running Django backend server. This solution includes:

1. ✅ **Mock API Server** - A simple server that simulates all API endpoints
2. ✅ **Configuration System** - Easy switching between Mock and Real API
3. ✅ **Complete Testing** - All 12 API endpoints tested with 100% success
4. ✅ **Network Support** - Can be used from mobile devices on LAN

---

## 🚀 Quick Start

### Step 1: Start Mock Server

```bash
# In project root directory
D:/project/project_payani/2/.venv/Scripts/python.exe mock_server_simple.py
```

**Expected output:**
```
============================================================
🚀 Mock API Server شروع شد
============================================================
📡 آدرس Local: http://localhost:8001
📡 آدرس شبکه: http://0.0.0.0:8001
⚠️  برای توقف: Ctrl+C
============================================================
```

### Step 2: Test All APIs

```bash
# In another terminal
D:/project/project_payani/2/.venv/Scripts/python.exe test_api_simple.py
```

**Result:**
```
✓ موفق: 12
✗ ناموفق: 0
💯 درصد: 100.0%
```

---

## 📱 Using on Mobile Device

### Configuration File

**Location:** `unipath_mobile/lib/config/api_config.dart`

### For Local Testing (Localhost):

```dart
class ApiConfig {
  static const bool useMockApi = true;  // Enable Mock API
  
  static const String mockServerIp = 'localhost';
  static const int mockServerPort = 8001;
}
```

### For Network Testing (Real Device):

#### Step 1: Find Your Machine IP

```bash
# Windows PowerShell
ipconfig

# Look for IPv4 Address (e.g., 192.168.100.104)
```

#### Step 2: Update Configuration

Edit `unipath_mobile/lib/config/api_config.dart`:

```dart
class ApiConfig {
  static const bool useMockApi = true;
  
  // Replace with your machine IP
  static const String mockServerIp = '192.168.100.104';
  static const int mockServerPort = 8001;
}
```

#### Step 3: Run on Mobile

```bash
flutter run -d <device_id>
```

---

## 🔄 Switching to Real Backend

### Step 1: Start Django Server

```bash
# Terminal 1
cd backend
python manage.py runserver 0.0.0.0:8000
```

### Step 2: Update Configuration

`unipath_mobile/lib/config/api_config.dart`:

```dart
class ApiConfig {
  static const bool useMockApi = false;  // Disable Mock API
  
  static const String serverIp = '192.168.100.104';
  static const int serverPort = 8000;
}
```

### Step 3: Rebuild App

```bash
flutter pub get
flutter run
```

---

## 📊 Available API Endpoints

All 12 endpoints are working and tested:

```
✓ GET  /api/health                   - Server health check
✓ POST /api/auth/login               - User login
✓ GET  /api/auth/user                - User profile
✓ GET  /api/courses                  - List all courses
✓ GET  /api/courses/{id}             - Get specific course
✓ GET  /api/enrollments              - List enrollments
✓ POST /api/enrollments              - Enroll in course
✓ GET  /api/grades                   - Get grades
✓ GET  /api/students/{id}/grades     - Student grades
✓ GET  /api/recommendations          - Course recommendations
✓ GET  /api/statistics               - Student statistics
✓ GET  /api/students                 - List students
```

---

## 📝 Files Created/Modified

```
Created:
├── mock_server_simple.py              # Mock API Server
├── test_api_simple.py                 # API Test Script
├── backend/mock_api_db.json           # Mock Database
├── unipath_mobile/lib/config/api_config.dart  # Configuration
└── MOBILE_TESTING_GUIDE_FA.md         # This guide (Persian)

Modified:
├── backend/unipath/settings.py        # Updated CORS & ALLOWED_HOSTS
└── unipath_mobile/lib/services/dio_client.dart # Updated to use ApiConfig
```

---

## ✨ Benefits

✅ **No Backend Required** - Test UI independently  
✅ **Realistic Mock Data** - Close to production data  
✅ **Easy Switching** - One configuration to change  
✅ **CORS Enabled** - Works with mobile and web  
✅ **Fast** - Mock server is very responsive  
✅ **Easy to Customize** - Simple JSON data format  

---

## 🔧 Troubleshooting

### Issue: "Connection refused"

**Solution:**
1. Is Mock Server running? → `python mock_server_simple.py`
2. Is API Config correct? → Check `api_config.dart`
3. Is firewall blocking? → Check firewall settings

### Issue: CORS Error (Mobile)

**Solution:** Mock Server has CORS enabled by default.
For real API, ensure:

```python
# backend/unipath/settings.py
CORS_ALLOW_ALL_ORIGINS = True
```

### Issue: Port already in use

**Solution:**
```bash
# Kill existing process
taskkill /F /IM python.exe

# Or change port in mock_server_simple.py
port = 8002
```

---

## 🎯 Test Results Summary

| Endpoint | Status | Code |
|----------|--------|------|
| Health Check | ✓ | 200 |
| Login | ✓ | 200 |
| User Profile | ✓ | 200 |
| Courses | ✓ | 200 |
| Specific Course | ✓ | 200 |
| Enrollments | ✓ | 200 |
| New Enrollment | ✓ | 201 |
| Grades | ✓ | 200 |
| Student Grades | ✓ | 200 |
| Recommendations | ✓ | 200 |
| Statistics | ✓ | 200 |
| Students | ✓ | 200 |
| **Total** | **12/12 ✓** | **100%** |

---

## 📚 Architecture

```
┌─────────────────┐
│  Flutter App    │ (Mobile Device)
└────────┬────────┘
         │
         │ HTTP (port 8001)
         │
┌────────▼──────────────┐
│ Mock API Server       │ (localhost:8001)
│ (mock_server_simple.py)
└────────┬──────────────┘
         │
         │ Reads from
         │
┌────────▼──────────────┐
│ Mock Database         │
│ (mock_api_db.json)    │
└───────────────────────┘

Alternative: Real Backend
┌─────────────────┐
│  Flutter App    │
└────────┬────────┘
         │
         │ HTTP (port 8000)
         │
┌────────▼──────────────┐
│ Django REST API       │
│ (manage.py runserver) │
└────────┬──────────────┘
         │
         │
┌────────▼──────────────┐
│ SQLite Database       │
│ (db.sqlite3)          │
└───────────────────────┘
```

---

## 📖 Related Documentation

- [Flutter Networking Guide](https://flutter.dev/docs/development/data-and-backend/networking)
- [Dio Package Documentation](https://pub.dev/packages/dio)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [CORS in Django](https://github.com/adamchainz/django-cors-headers)

---

**✅ Everything is ready! You can now test the frontend on mobile devices.**
