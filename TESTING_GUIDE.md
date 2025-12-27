# Testing Guide - Auth System Integration

## Pre-Test Setup

### Start Django Backend
```bash
cd backend
python manage.py migrate
python manage.py runserver
```

### Run Flutter App
```bash
cd unipath_mobile
flutter pub get
flutter run
```

### Verify Backend is Running
```bash
curl http://localhost:8000/api/auth/login
# Should return: {"detail":"Method \"GET\" not allowed."}
```

---

## 🧪 Manual Testing Scenarios

### Scenario 1: User Registration

**Steps:**
1. Open Flutter app
2. Click "ثبت نام کنید" (Register) on login screen
3. Fill in registration form:
   - Username: `testuser123`
   - Email: `test@example.com`
   - First Name: `علی`
   - Last Name: `محمدی`
   - Password: `TestPass123!`
   - Confirm: `TestPass123!`
   - Role: `student`
4. Click "ثبت نام" (Register)

**Expected Results:**
- ✅ No validation errors
- ✅ Success message appears
- ✅ Redirect to login screen
- ✅ Can now login with registered credentials

**Error Cases:**
- Weak password (< 6 chars) → Error message
- Mismatched passwords → Error message
- Duplicate email → Error message
- Invalid email format → Error message

---

### Scenario 2: User Login

**Steps:**
1. Open Flutter app
2. Enter credentials:
   - Email: `test@example.com`
   - Password: `TestPass123!`
3. Click "ورود" (Login)

**Expected Results:**
- ✅ Loading spinner shows
- ✅ Successfully authenticates
- ✅ JWT tokens stored securely
- ✅ Redirect to dashboard
- ✅ User can see dashboard content

**Error Cases:**
- Wrong password → "ایمیل یا رمز عبور نادرست است"
- Non-existent email → Same error message
- Network error → "خطا در ارتباط با سرور"

---

### Scenario 3: Auto-Login

**Steps:**
1. Login successfully (Scenario 2)
2. Kill and restart the Flutter app
3. Observe app startup

**Expected Results:**
- ✅ Loading screen appears
- ✅ Auto-login completes
- ✅ Directly navigates to dashboard (no login screen)
- ✅ User info preserved

---

### Scenario 4: Logout

**Steps:**
1. Login successfully (Scenario 2)
2. Navigate to profile screen (if available)
3. Scroll to bottom
4. Click "خروج" (Logout)

**Expected Results:**
- ✅ Tokens cleared from storage
- ✅ Redirect to login screen
- ✅ Cannot access dashboard without re-login
- ✅ Cleared all user data

---

### Scenario 5: Token Refresh

**Steps:**
1. Login successfully
2. Open browser DevTools or network monitor
3. Wait for access token to expire (5 minutes)
4. Make any API request

**Expected Results:**
- ✅ 401 received on expired token
- ✅ Automatic refresh happens
- ✅ Request automatically retried
- ✅ User doesn't notice token expiration

---

### Scenario 6: Profile View & Edit

**Steps:**
1. Login successfully
2. Navigate to profile screen
3. Click edit button
4. Edit fields:
   - First Name: `احمد`
   - Phone: `09121234567`
   - Bio: `متخصص برنامه‌نویسی`
5. Click "ذخیره تغییرات" (Save Changes)

**Expected Results:**
- ✅ Form fields enabled when editing
- ✅ Changes saved to backend
- ✅ Success message shows
- ✅ Data persists after refresh

---

### Scenario 7: Change Password

**Steps:**
1. Login successfully
2. Navigate to settings (if available)
3. Click "تغییر رمز عبور"
4. Enter:
   - Old Password: `TestPass123!`
   - New Password: `NewPass456!`
   - Confirm: `NewPass456!`
5. Click "تغییر"

**Expected Results:**
- ✅ Validation passes
- ✅ Password changed successfully
- ✅ Can login with new password
- ✅ Old password no longer works

**Error Cases:**
- Wrong old password → "رمز عبور فعلی نادرست است"
- Mismatched new passwords → Validation error

---

## 🔧 API Testing (with cURL)

### Test 1: Registration

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "curluser",
    "email": "curl@test.com",
    "password": "TestPass123!",
    "password2": "TestPass123!",
    "role": "student"
  }'
```

**Expected Status:** 201 Created

---

### Test 2: Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "curl@test.com",
    "password": "TestPass123!"
  }'
```

**Expected Status:** 200 OK

**Response includes:**
- `access` - Access token
- `refresh` - Refresh token
- `user` - User info

**Save the access token:**
```bash
ACCESS_TOKEN="eyJ0eXAi..."
```

---

### Test 3: Get Profile

```bash
curl -X GET http://localhost:8000/api/user/profile \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Expected Status:** 200 OK

---

### Test 4: Refresh Token

```bash
curl -X POST http://localhost:8000/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "REFRESH_TOKEN_HERE"
  }'
```

**Expected Status:** 200 OK

**Returns:** New `access` token

---

### Test 5: Change Password

```bash
curl -X POST http://localhost:8000/api/user/change-password \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "TestPass123!",
    "new_password": "NewPass456!",
    "new_password2": "NewPass456!"
  }'
```

**Expected Status:** 200 OK

---

## 🧪 Automated Backend Tests

### Run All Tests
```bash
cd backend
python manage.py test accounts -v 2
```

### Run Specific Test Class
```bash
python manage.py test accounts.RegistrationAPITests -v 2
```

### Run Specific Test
```bash
python manage.py test accounts.RegistrationAPITests.test_register_valid_data -v 2
```

### With Coverage
```bash
coverage run --source='.' manage.py test accounts
coverage report
coverage html  # Creates htmlcov/index.html
```

---

## 📊 Test Coverage Report

**Current Status:** 28/28 tests passing ✅

**By Category:**

| Test Class | Tests | Status |
|-----------|-------|--------|
| UserModelTests | 6 | ✅ All Pass |
| ProfileModelTests | 1 | ✅ Pass |
| RegistrationAPITests | 5 | ✅ All Pass |
| LoginAPITests | 4 | ✅ All Pass |
| TokenRefreshTests | 1 | ✅ Pass |
| LogoutAPITests | 2 | ✅ All Pass |
| ChangePasswordTests | 3 | ✅ All Pass |
| ProfileAPITests | 3 | ✅ All Pass |
| PermissionTests | 3 | ✅ All Pass |

---

## 🐛 Debugging

### Check Flutter App Logs
```bash
flutter logs
```

### Check Django Backend Logs
```bash
# Terminal where runserver is running
# Should show request logs
```

### Check Stored Tokens (Android)
```bash
flutter pub run device_lab --module=local_test
```

### Common Issues

**Issue: 401 Unauthorized**
- Solution: Token expired, need refresh
- Check: `DateTime.now()` vs token expiry
- Fix: Auto-refresh in Dio interceptor

**Issue: CORS Error**
- Solution: Check Django CORS_ALLOWED_ORIGINS
- File: `backend/unipath/settings.py`
- Add: `http://localhost:8100` (Xcode), `http://localhost:8101` (Android)

**Issue: Connection Refused**
- Solution: Backend not running
- Fix: `python manage.py runserver`
- Check: `curl http://localhost:8000/api/auth/login`

**Issue: "No token found"**
- Solution: FlutterSecureStorage not initialized
- Fix: Run app again after login
- Check: Keychain/Keystore settings

---

## ✅ Integration Test Checklist

### Pre-Integration
- [ ] Backend running on http://localhost:8000
- [ ] Flutter app can connect to backend
- [ ] Test user account exists

### Registration Flow
- [ ] Can register with valid data
- [ ] Cannot register with duplicate email
- [ ] Cannot register with weak password
- [ ] Error messages display correctly
- [ ] Redirect to login after registration

### Login Flow
- [ ] Can login with correct credentials
- [ ] Cannot login with wrong password
- [ ] Tokens stored securely
- [ ] Can access protected endpoints
- [ ] Error messages are Persian

### Auto-Login
- [ ] Tokens saved after login
- [ ] Auto-login on app restart
- [ ] Navigate directly to dashboard
- [ ] No login screen shown

### Profile Management
- [ ] Can view own profile
- [ ] Can edit profile fields
- [ ] Can save profile changes
- [ ] Changes persist after refresh
- [ ] Cannot view other users' profiles

### Logout
- [ ] Can logout successfully
- [ ] Tokens cleared from storage
- [ ] Cannot access protected endpoints
- [ ] Redirect to login screen
- [ ] Must re-login to access app

### Token Refresh
- [ ] Access token expires after 5 min
- [ ] Automatic refresh on expired token
- [ ] Requests don't fail during refresh
- [ ] Can continue using app

---

## 🎯 Performance Testing

### Measure Response Times

**Login:**
```bash
time curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Pass123!"}'
```
Expected: < 200ms

**Token Refresh:**
```bash
time curl -X POST http://localhost:8000/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh":"TOKEN"}'
```
Expected: < 100ms

**Get Profile:**
```bash
time curl -X GET http://localhost:8000/api/user/profile \
  -H "Authorization: Bearer TOKEN"
```
Expected: < 200ms

---

## 📝 Test Report Template

```markdown
# Test Report - [Date]

## Environment
- Backend: Django [version]
- Frontend: Flutter [version]
- Device: [device/emulator]
- OS: [Android/iOS version]

## Test Results
### Registration: ✅ PASS / ❌ FAIL
- [ ] Valid registration works
- [ ] Error messages display
- [ ] Validation works

### Login: ✅ PASS / ❌ FAIL
- [ ] Can login
- [ ] Tokens stored
- [ ] Error handling works

### Auto-Login: ✅ PASS / ❌ FAIL
- [ ] Tokens saved
- [ ] App auto-logins
- [ ] No login screen

### Profile: ✅ PASS / ❌ FAIL
- [ ] Can view profile
- [ ] Can edit profile
- [ ] Changes persist

### Logout: ✅ PASS / ❌ FAIL
- [ ] Logout works
- [ ] Tokens cleared
- [ ] Cannot access app

## Issues Found
1. [Issue description]
   - Status: Open/Closed
   - Severity: Critical/High/Medium/Low

## Recommendations
- [Recommendation 1]
- [Recommendation 2]

## Conclusion
Overall: ✅ PASS / ⚠️ PASS WITH ISSUES / ❌ FAIL
```

---

## 🚀 Next Steps

After testing passes:
1. ✅ Complete Phase 8: Polish UI/UX
2. ✅ Complete Phase 9: Integration testing
3. ✅ Complete Phase 10: Documentation
4. Deploy to TestFlight/Firebase

---

**Last Updated:** 2024-12-19  
**Version:** 1.0
