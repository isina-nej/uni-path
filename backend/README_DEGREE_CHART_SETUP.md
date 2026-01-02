# Backend Setup Complete - Degree Chart System

**Status**: ✅ READY FOR PRODUCTION DEPLOYMENT  
**Last Updated**: Current Session

---

## What's New

### Backend Models - Redesigned for Degree Programs

The `DegreeChart` model has been enhanced to support entry year ranges, field codes, and education levels:

```
DegreeChart (Enhanced)
├── start_year: 1392 (First entry year)
├── end_year: 1402 (Last entry year)
├── field_code: "102" (For student ID generation)
├── level: "12" (12=Bachelor, 13=Masters, 14=PhD)
└── + All existing fields (name, code, department, total_credits, etc.)
```

### New Models Added

1. **CourseRequirement** - Track minimum units before enrollment
   - Example: "Capstone requires 100 passed units"

2. **ChartCourse** - Already existed, properly configured
   - Links courses to degree charts with semester organization

### Data Created

**Computer Engineering Degree Program** (Entry Years 1392-1402):
- 55 Courses across 8 semesters
- 38 Prerequisite relationships
- 7 Co-requisite relationships
- All linked in degree chart

---

## Key Features

### Entry Year Support
```python
# Create a degree chart for specific entry years
chart = DegreeChart.objects.create(
    name='مهندسی کامپیوتر - کارشناسی',
    code='CS-BS-92-402',
    start_year=1392,
    end_year=1402,
    field_code='102',  # Computer Engineering
    level='12'  # Bachelor
)

# Check if chart applies to entry year
if chart.is_active_for_year(1395):
    print("This chart applies to 1395 cohort")
```

### Education Level Classification
```python
LEVEL_CHOICES = [
    ('12', 'کارشناسی (Bachelor)'),
    ('13', 'کارشناسی ارشد (Masters)'),
    ('14', 'دکتری (PhD)'),
]
```

### Field Code for Student IDs
```python
# Field codes used in student ID generation
# Example Student ID: 400121020001
#                      ↓ ↓↓↓↓↓↓↓↓↓
#                      year + level + field + sequence
# field_code=102 means Computer Engineering
```

---

## Database Migration

### Local Setup ✅
```bash
# Migration already created and applied locally
python manage.py migrate courses
# ✅ All tables created
# ✅ All indexes built
# ✅ Data populated
```

### Production Setup (Next)
```bash
# On PythonAnywhere:
python manage.py migrate courses
```

**Migration File**: `courses/migrations/0002_courserequirement_alter_degreechart_options_and_more.py`

---

## File Changes Summary

### Models (Updated)
- `backend/courses/models.py`
  - DegreeChart: 4 new fields (start_year, end_year, field_code, level)
  - CourseRequirement: NEW model for unit prerequisites
  - Prerequisite: No changes (already correct)

### Admin (Updated)
- `backend/courses/admin.py`
  - DegreeChartAdmin: Enhanced with entry year management
  - ChartCourseAdmin: Semester management
  - CourseRequirementAdmin: NEW admin for unit requirements

### Migrations (New)
- `backend/courses/migrations/0002_courserequirement_*.py`

### Data Generation (New)
- `backend/create_degree_chart_v2.py` - Creates 55 courses + degree chart
- `backend/cleanup_all_data.py` - Cleans old test data

---

## Admin Interface Improvements

### DegreeChart Admin
New fields visible:
- Entry Year Range: 1392 to 1402
- Level: کارشناسی (Bachelor)
- Field Code: 102
- Inline course management by semester

### Course Admin
- View course prerequisites inline
- Edit pre-requisites and co-requisites
- See course relationships

### ChartCourse Admin
- Manage semester assignments
- Mark courses as mandatory/elective
- View which courses belong to which degree chart

---

## Backward Compatibility

✅ **No Breaking Changes**

- All existing fields preserved in DegreeChart
- New fields have sensible defaults
- Existing data continues to work
- Simple migration with no data loss

---

## Production Deployment Steps

### 1. Upload Files to PythonAnywhere
```
backend/courses/models.py (updated)
backend/courses/admin.py (updated)
backend/courses/migrations/0002_*.py (new)
```

### 2. SSH into PythonAnywhere
```bash
ssh isinanej@ssh.pythonanywhere.com
cd ~/uni-path/backend
```

### 3. Apply Migration
```bash
python manage.py migrate courses
```

### 4. Populate Data (Optional - if data needed)
```bash
# Copy create_degree_chart_v2.py to server and run
python create_degree_chart_v2.py
```

### 5. Verify
```bash
# Check Django admin - should see new fields
python manage.py shell
>>> from courses.models import DegreeChart
>>> DegreeChart.objects.all()
```

### 6. Reload Web App
- Go to PythonAnywhere dashboard
- Click "Reload web app"

---

## Testing Locally

### View Degree Chart
```bash
python manage.py shell
>>> from courses.models import DegreeChart
>>> chart = DegreeChart.objects.get(code='CS-BS-92-402')
>>> print(f"Entry Years: {chart.start_year}-{chart.end_year}")
>>> print(f"Courses: {chart.chart_courses.count()}")
>>> courses = chart.chart_courses.all().order_by('recommended_semester')
```

### View Prerequisites
```bash
>>> from courses.models import Course
>>> course = Course.objects.get(code='CE-401')  # Algorithms
>>> course.prerequisites_for.all()
```

### View Entry Year Range
```bash
>>> chart.is_active_for_year(1395)  # True
>>> chart.is_active_for_year(1410)  # False
```

---

## API Integration (Next Phase)

When API endpoints are created:

```python
# Example future endpoint
GET /api/degree-charts/CS-BS-92-402/

Response:
{
  "id": 1,
  "name": "مهندسی کامپیوتر - کارشناسی",
  "code": "CS-BS-92-402",
  "level": "12",
  "start_year": 1392,
  "end_year": 1402,
  "field_code": "102",
  "total_credits": 132,
  "courses": [
    {
      "code": "CE-101",
      "name": "فیزیک 1",
      "credits": 3,
      "semester": 1,
      "is_mandatory": true,
      "prerequisites": []
    },
    ...
  ]
}
```

---

## OpenSpec Documentation

See the complete specification in:
- `openspec/changes/setup-degree-chart/proposal.md` - Problem & Solution
- `openspec/changes/setup-degree-chart/models_spec.md` - Detailed specifications
- `openspec/changes/setup-degree-chart/IMPLEMENTATION_SUMMARY.md` - What was implemented

---

## Support

For questions about:
- **Model structure**: See `backend/courses/models.py`
- **Admin interface**: See `backend/courses/admin.py`
- **Data population**: See `backend/create_degree_chart_v2.py`
- **Specifications**: See OpenSpec files above

---

**All changes follow OpenSpec methodology and have been tested locally. Ready for production!** ✅
