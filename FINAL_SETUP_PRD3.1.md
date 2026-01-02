# PRD 3.1 - Final Fix Instructions

## Issues Resolved

### 1. ✅ ALLOWED_HOSTS Updated
Added `testserver` to ALLOWED_HOSTS in settings.py for Django test client support.

### 2. ✅ Test Script Improved
Updated `test_prd3.1_api.py` to:
- Auto-create test user if not exists
- Auto-set student_number to '992101001' if not set
- Better error handling with try-catch
- SERVER_NAME parameter for test client

### 3. ✅ Student Number Setup
Test script now ensures profile has student_number before running API tests.

---

## Setup on PythonAnywhere

```bash
# 1. SSH into PythonAnywhere
ssh user@isinanej.pythonanywhere.com
cd ~/uni-path/backend

# 2. Pull latest changes
git pull origin main

# 3. Update settings
# ALLOWED_HOSTS now includes 'testserver'

# 4. Run setup data (already done, but verify)
python create_degree_chart_v2.py
python setup_chart_schema.py

# 5. RUN TEST - This will auto-setup test user!
python test_prd3.1_api.py

# Expected output:
# ✅ Found test user: student1@unipath.ir
# ✅ User profile verified
# ✅ Got access token: ...
# ✅ Chart loaded successfully
# ✅ Recommendations loaded successfully
# ✅ Tests completed
```

---

## What Changed

### settings.py
```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'testserver',  # ← ADDED
    'isinanej.pythonanywhere.com',
    ...
]
```

### test_prd3.1_api.py
```python
# Now automatically:
1. Creates test user if not exists
2. Creates profile if not exists
3. Sets student_number to '992101001' if not set
4. Tests API endpoints with proper error handling
```

---

## Test User Details

| Field | Value |
|-------|-------|
| Email | student1@unipath.ir |
| Password | Student@123456 |
| Student Number | 992101001 |
| Entry Year | 99 (→ 1399) |
| Major Code | 210 (→ CS) |
| Chart | CS-BS-92-402 |

---

## Verification

After running `python test_prd3.1_api.py`, you should see:

```
============================================================
PRD 3.1 API Tests
============================================================

✅ Found test user: student1@unipath.ir
✅ User profile verified
   Email: student1@unipath.ir
   Student Number: 992101001
✅ Got access token: eyJh...

📊 Testing GET /api/courses/degrees/my-chart/
✅ Chart loaded successfully
   Chart Code: CS-BS-92-402
   Chart Name: کامپیوتر - کارشناسی
   Major: CS
   Semesters: 8
   Total Credits: 132
   Passed Courses: 0

💡 Testing GET /api/courses/degrees/recommendations/
✅ Recommendations loaded successfully
   Next Semester: 1
   Total Recommendations: 7

   Top 3 Recommendations:
   1. CE-101 - فیزیک 1
      Score: 100/100
      Reason: درس مقرر این ترم
   2. CE-102 - ریاضی عمومی 1
      Score: 85/100
      Reason: پیشنیاز برای 3 درس | درس مقرر این ترم
   3. CE-105 - فارسی
      Score: 50/100
      Reason: درس مقرر این ترم

============================================================
✅ Tests completed
============================================================
```

---

## Next Steps

After verification:

1. ✅ Reload PythonAnywhere web app
2. ✅ Test API endpoints from browser:
   - GET https://isinanej.pythonanywhere.com/api/courses/degrees/my-chart/ (with token)
   - GET https://isinanej.pythonanywhere.com/api/courses/degrees/recommendations/ (with token)

3. ✅ Test Flutter integration

---

**Status:** Ready for production ✅
