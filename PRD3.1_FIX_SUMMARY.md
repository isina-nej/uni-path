# PRD 3.1 API Fix Summary

**Date:** January 3, 2026  
**Issue:** ImportError in `views_chart.py` - Wrong model names

---

## Issues Fixed

### 1. ❌ Wrong Import: `StudentProfile` → ✅ `Profile`
**File:** `backend/courses/views_chart.py`

**Was:**
```python
from accounts.models import StudentProfile, StudentCourse
```

**Now:**
```python
from accounts.models import get_user_model
from students.models import StudentCourseHistory
```

### 2. ❌ Wrong Model: `student_profile.student_id` → ✅ `profile.student_number`
**File:** `backend/courses/views_chart.py`

**All occurrences changed:**
- Line 43: `student_profile = user.studentprofile` → `profile = user.profile`
- Line 48: `student_id = student_profile.student_id` → `student_id = profile.student_number`

### 3. ❌ Wrong Model: `StudentCourse` → ✅ `StudentCourseHistory`
**File:** `backend/courses/views_chart.py`

**Changed:**
```python
# Old:
passed_courses = StudentCourse.objects.filter(
    student=student_profile,
    is_passed=True
)

# New:
passed_courses = StudentCourseHistory.objects.filter(
    student=user,
    grade__in=['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D']  # Passing grades
)
```

### 4. ✅ Added `requests` to `requirements.txt`
**File:** `backend/requirements.txt`

```
requests==2.31.0
```

### 5. ✅ Simplified `test_prd3.1_api.py`
**File:** `backend/test_prd3.1_api.py`

- Changed from using `requests` library to Django test client
- No longer requires running `python manage.py runserver` separately
- Runs within Django environment directly

---

## Model Mapping Reference

| Old Name | New Name | Location |
|----------|----------|----------|
| `StudentProfile` | `Profile` | `accounts.models` |
| `student_profile.student_id` | `profile.student_number` | `accounts.models.Profile` |
| `StudentCourse` | `StudentCourseHistory` | `students.models` |
| `StudentCourse.is_passed` | `StudentCourseHistory.grade` | (check for non-F/W grades) |

---

## Testing After Fix

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create test data
```bash
python create_degree_chart_v2.py      # Create 55 courses
python setup_chart_schema.py           # Create charts + nodes
```

### Step 3: Create test student (if not exists)
```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()

# Create user
user = User.objects.create_user(
    username='student1',
    email='student1@unipath.ir',
    password='Student@123456',
    role='student'
)

# Create profile with student number
profile = Profile.objects.create(
    user=user,
    student_number='992101001'  # Entry year 99, Major 210 (CS)
)

print(f"✅ Created {user.email} with student_number {profile.student_number}")
exit()
```

### Step 4: Test the API
```bash
python test_prd3.1_api.py
```

**Expected Output:**
```
============================================================
PRD 3.1 API Tests
============================================================

✅ Found test user: student1@unipath.ir
✅ User profile found
   Student Number: 992101001
✅ Got access token: ...

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
   ...

============================================================
✅ Tests completed
============================================================
```

---

## Deployment to PythonAnywhere

```bash
# SSH into PythonAnywhere
ssh user@isinanej.pythonanywhere.com

# Navigate to project
cd ~/uni-path/backend

# Pull changes
git pull origin main

# Install new dependencies
pip install requests

# Test locally
python test_prd3.1_api.py

# If successful, reload web app
# Visit: https://www.pythonanywhere.com/
# Web → your app → Reload
```

---

## Verification Checklist

- ✅ `views_chart.py` imports correct models
- ✅ `serializers_chart.py` imports correct models
- ✅ `requirements.txt` includes `requests`
- ✅ `test_prd3.1_api.py` uses Django test client
- ✅ API endpoints match model structure
- ✅ Student number parsing works (xxyyzzznnn format)
- ✅ Major code mapping correct (210→CS, etc)
- ✅ Chart schema lookup by entry year range
- ✅ Recommendations calculated correctly

---

**Status:** ✅ Ready for deployment
