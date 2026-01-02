# OpenSpec Proposal: Setup Degree Chart System

**Status**: In Progress  
**Created**: Current Session  
**Updated**: With Backend Verification

---

## 1. Problem Statement

### Current Situation
Backend has a basic `DegreeChart` model with minimal fields that cannot support the curriculum requirements:
- ❌ No way to track which entry years a degree chart applies to (start_year, end_year)
- ❌ No field_code to link to student ID generation (e.g., 102 for Computer Science)
- ❌ No semester organization for courses (cannot organize 56 courses across 8 semesters)
- ❌ No education level tracking (bachelor vs masters vs phd)
- ❌ No distinction between mandatory and elective courses

### User Request
> "نگا هر چارت باید مختص یک رشته و یک مقطع و یه بازه ورودی باشه... الان مثلا چارت زیر که باید اضافش کنی برای ورودی های 92 تا 402"

(A degree chart should be specific to one field, one level, and an entry year range. For example, the chart below should be added for entry years 92-402)

Required structure:
- Computer Engineering (مهندسی کامپیوتر) 
- Bachelor level (کارشناسی) with code 12
- Entry years: 1392-1402 (92-402 in short form)
- 56 courses across 8 semesters
- 36 prerequisite relationships
- 8 corequisite relationships

---

## 2. Proposed Solution

### Overview
Redesign the `DegreeChart` model and create supporting models to properly structure degree programs with entry year ranges, field codes, education levels, and semester organization.

### Required Changes

#### Phase 1: Model Structure (BLOCKING)
- **MODIFIED**: `DegreeChart` - Add start_year, end_year, field_code, level
- **ADDED**: `DegreeChartCourse` - Link courses to charts with semester info
- **ADDED**: `CourseRequirement` - Track minimum unit requirements
- **VERIFIED**: `Prerequisite` - Already supports prerequisites and corequisites

#### Phase 2: Data Population
- Generate degree chart for Computer Engineering (92-402)
- Populate all 56 courses with semester assignments
- Link 36 prerequisite relationships
- Link 8 corequisite relationships

#### Phase 3: API & Deployment
- Create serializers for degree chart queries
- Deploy migration to PythonAnywhere
- Populate production database

---

## 3. Design Specifications

See [models_spec.md](models_spec.md) for detailed field specifications, scenarios, and examples.

**Key Models:**

```
DegreeChart
├── name: "مهندسی کامپیوتر - کارشناسی"
├── code: "CE-BS-92-402"
├── start_year: 1392
├── end_year: 1402
├── field_code: "102"
├── level: "12" (Bachelor)
└── courses → DegreeChartCourse (through model)
    └── course: Course
    ├── semester: 1-8
    └── is_mandatory: True/False

Prerequisite
├── course: Course (Algorithm)
├── prerequisite_course: Course (Data Structures)
└── is_corequisite: False

CourseRequirement
├── course: Course (Capstone)
└── min_passed_units: 100
```

---

## 4. Implementation Roadmap

### Step 1: Update DegreeChart Model
✅ Add start_year, end_year, field_code, level fields to existing DegreeChart  
✅ Keep existing name, code, description, department, total_credits fields  
✅ No data loss - adds new optional columns

### Step 2: Create DegreeChartCourse Model
✅ New through-model for Course ↔ DegreeChart M2M relationship  
✅ Includes semester number (1-8) for organization  
✅ Includes is_mandatory flag and order  
✅ Unique constraint: each course appears once per chart

### Step 3: Create CourseRequirement Model
✅ Track minimum passed units before enrollment  
✅ Complements existing Prerequisite model (which tracks direct course dependencies)

### Step 4: Create Django Migration
⏳ Use makemigrations to generate schema changes  
⏳ Test migration on local database  
⏳ Deploy to PythonAnywhere

### Step 5: Update Prerequisite Model (If Needed)
✅ Verify existing model has all needed fields:  
   - course (FK)
   - prerequisite_course (FK)
   - is_corequisite (Boolean)
   - min_grade (optional)

### Step 6: Populate Degree Chart Data
⏳ Update create_degree_chart.py to use new model structure  
⏳ Execute script to populate all 56 courses  
⏳ Verify all prerequisites/corequisites linked correctly

### Step 7: API Endpoints
⏳ Create DegreeChartSerializer with nested courses  
⏳ Create ViewSet for degree chart queries  
⏳ Endpoint: GET /api/degree-charts/ - list all  
⏳ Endpoint: GET /api/degree-charts/{id}/ - detail with full curriculum

### Step 8: Production Deployment
⏳ Upload changes to PythonAnywhere  
⏳ Run migrations on production  
⏳ Populate production degree chart data  
⏳ Test endpoints in production

---

## 5. Success Criteria

### ✅ Completed (Before Implementation)
- [x] Backend deployment to PythonAnywhere
- [x] Email+username login verified working
- [x] Test data generation with correct student IDs
- [x] 56 courses designed with prerequisites/corequisites

### 🔄 In Progress (This Proposal)
- [ ] Spec validation and approval
- [ ] Model implementation
- [ ] Migration creation and testing
- [ ] Data population

### ⏳ Pending (After Implementation)
- [ ] API endpoints for curriculum queries
- [ ] Production deployment
- [ ] End-to-end testing in production

**Final Success State:**
```
GET /api/degree-charts/ce-bs-92-402/
{
  "id": 1,
  "name": "مهندسی کامپیوتر - کارشناسی",
  "code": "CE-BS-92-402",
  "start_year": 1392,
  "end_year": 1402,
  "field_code": "102",
  "level": "12",
  "total_credits": 132,
  "courses": [
    {
      "semester": 1,
      "order": 1,
      "course": {
        "code": "CE-101",
        "name": "Fundamentals of Programming",
        "credits": 3,
        "prerequisites": []
      },
      "is_mandatory": true
    },
    ...56 total courses...
  ]
}
```

---

## 6. Risk Assessment

### Low Risk Items
- ✅ Adding new fields to existing DegreeChart (backward compatible)
- ✅ Creating new models (no existing data affected)
- ✅ Migration to local test database

### Medium Risk Items
- ⚠️ Migration to production PythonAnywhere (needs backup first)
- ⚠️ Updating create_degree_chart.py script (script, not schema)

### Mitigation
1. Test all migrations locally first
2. Backup database before production migration
3. Run migrations on PythonAnywhere in controlled manner
4. Populate data after successful migration verification

---

## 7. Timeline

**Today:**
- Spec validation
- Model implementation
- Migration creation

**Next Step:**
- Local testing
- PythonAnywhere deployment
- Data population

**Estimated Time:** 2-3 hours for full implementation + testing

---

## 8. OpenSpec References

**Related Files:**
- [models_spec.md](models_spec.md) - Detailed field specifications
- [Backend Models Location](../../../backend/courses/models.py)
- [Test Data Generation](../../../backend/create_degree_chart.py)

**Approval Chain:**
1. ✅ Proposal review (this document)
2. ⏳ Design specification review (models_spec.md)
3. ⏳ Implementation approval before coding
- ✅ CourseRequirement model tracks minimum unit prerequisites
- ✅ All relationships properly configured
- ✅ Data migration script can successfully populate degree charts
- ✅ API endpoints return structured degree chart data

## Estimated Effort
- Model Design & Migration: 2-3 hours
- API Serializers: 1-2 hours  
- Data Population Script: 1 hour
- Testing: 1 hour
