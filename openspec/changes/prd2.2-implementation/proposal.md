# OpenSpec Proposal: PRD 2.2 Implementation - Chart Schema & Electives

**Status**: ✅ IMPLEMENTED & TESTED  
**Date**: Current Session  
**Related PRD**: prd2.2.md

---

## Problem Statement

### Previous Implementation Limitations (PRD 2.1)
The earlier DegreeChart model had limitations:
- ❌ Only one version per major/degree (no historical tracking)
- ❌ No way to manage different versions for different entry year cohorts
- ❌ Elective courses hardcoded as placeholder courses
- ❌ No polymorphic structure for required vs elective slots

### User Requirement from PRD 2.2
> "سیستم باید از چند‌نسخگی چارت پشتیبانی کند. هر چارت درسی منحصر به یک رشته، مقطع و بازه سال ورودی است."

(The system must support multi-versioning of charts. Each degree chart is unique to a field, degree level, and entry year range.)

### Specific Needs
1. **Version Control**: Different entry year cohorts → different curriculum rules
2. **Elective Baskets**: "Choose one from Technical Electives" not hardcoded
3. **Flexible Positions**: Chart nodes can be specific courses OR elective groups
4. **Data Integrity**: Enforce mutual exclusion (either course OR group, not both)

---

## Proposed Solution

### Three New Models

#### 1. ChartSchema (Replaces/Augments DegreeChart)
- **Purpose**: Versioned degree program specifications
- **Fields**: major, degree, entry_year_start, entry_year_end, code, name
- **Unique Constraint**: (major, degree, year_start, year_end)
- **Example**: CS-BS-92-402 for Computer Science Bachelor (1392-1402)

#### 2. CourseGroup
- **Purpose**: Manage elective course categories
- **Fields**: name, code, description, courses (M2M)
- **Example**: "Technical Electives" containing Data Mining, Cloud Computing, etc.

#### 3. ChartNode (Polymorphic Position)
- **Purpose**: Individual positions in degree chart
- **Fields**: schema, semester, position, course (FK, nullable), course_group (FK, nullable)
- **Constraint**: Exactly one of (course, course_group) must be non-null
- **Types**:
  - **Specific Node**: course=CE-101, course_group=null → Required Physics 1
  - **Elective Node**: course=null, course_group=TECH-ELECTIVES → Choose technical elective

---

## Implementation Details

### Models Created

```python
class ChartSchema(models.Model):
    major = CharField(choices=[CS, EE, CE, ME, SE])
    degree = CharField(choices=['12', '13', '14'])  # Bachelor, Masters, PhD
    entry_year_start = IntegerField()
    entry_year_end = IntegerField()
    name = CharField()  # Display name
    code = CharField(unique=True)
    total_credits = IntegerField()
    is_active = BooleanField()
    # Unique constraint: (major, degree, year_start, year_end)
    # Indexes: (major, degree), (year_start, year_end)

class CourseGroup(models.Model):
    name = CharField()  # "Technical Electives"
    code = CharField(unique=True)  # "TECH-ELECTIVE"
    courses = ManyToManyField(Course)

class ChartNode(models.Model):
    schema = ForeignKey(ChartSchema)
    semester = IntegerField(1-8)
    position = IntegerField()  # Order within semester
    course = ForeignKey(Course, null=True, blank=True)
    course_group = ForeignKey(CourseGroup, null=True, blank=True)
    is_mandatory = BooleanField()
    # Constraint: XOR(course, course_group) - exactly one must be set
    # Unique constraint: (schema, semester, position)
```

### Data Created

**ChartSchema**:
- Computer Science BS (92-402): 1 schema created

**CourseGroups** (2 groups):
1. Technical Electives (5 courses)
2. General Electives (3 courses)

**ChartNodes** (55 positions):
- 50 required course nodes
- 5 elective slot nodes

### Admin Interface

**ChartSchemaAdmin**:
- View all degree program versions
- Filter by major, degree, year range
- Inline editing of chart nodes (ChartNodeInline)

**CourseGroupAdmin**:
- Manage elective groups
- Multi-select courses
- Display count of courses per group

**ChartNodeAdmin**:
- View all chart positions
- Filter by schema, semester, type (required vs elective)
- Visual indicator of node type

---

## Success Criteria Met

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Version support | ✅ | ChartSchema with (major, degree, year_range) uniqueness |
| Entry year range | ✅ | entry_year_start=1392, entry_year_end=1402 |
| Elective groups | ✅ | 2 CourseGroups created with 8 courses total |
| Polymorphic nodes | ✅ | ChartNode supports course OR group |
| Data validation | ✅ | clean() method enforces mutual exclusion |
| Admin interface | ✅ | Full CRUD for all 3 models |
| Data population | ✅ | 55 nodes created for 8 semesters |
| Database integrity | ✅ | All constraints enforced |

---

## Testing Results

### Local Database
- ✅ Migration created successfully
- ✅ Migration applied successfully
- ✅ All 3 tables created
- ✅ All indexes created
- ✅ Data population script executed successfully
- ✅ No orphaned records
- ✅ Foreign key constraints verified

### Data Verification
```
📊 Chart Schemas: 1
🎯 Elective Groups: 2
📋 Chart Nodes: 55
📚 Courses: 55
🔗 Prerequisites: 37
⚡ Co-requisites: 7
```

---

## Backward Compatibility

✅ **Non-breaking changes**:
- New models don't affect existing Course, Prerequisite, CoRequisite
- DegreeChart still exists and functional
- ChartSchema is new, separate from DegreeChart
- All existing data preserved

---

## Migration & Deployment

### Files Modified/Created

**New Models**:
- `backend/courses/models.py` - Added ChartSchema, CourseGroup, ChartNode

**Admin Interface**:
- `backend/courses/admin.py` - Added 3 admin classes

**Migration**:
- `backend/courses/migrations/0003_coursegroup_chartschema_chartnode.py` - NEW

**Data Setup**:
- `backend/setup_chart_schema.py` - Populate script

### Deployment Steps

```bash
# Step 1: Push to PythonAnywhere
git push  # Or scp files

# Step 2: Create migration (already done)
python manage.py makemigrations courses

# Step 3: Apply migration
python manage.py migrate courses

# Step 4: Populate data
python setup_chart_schema.py

# Step 5: Verify in admin
# Visit: /admin/courses/chartschema/
```

---

## Future Enhancements (Out of Scope)

1. API endpoints for degree chart queries
2. Student enrollment validation against prerequisites
3. Automatic semester recommendation based on prerequisites
4. Historical versioning of chart changes
5. Support for degree program variations (thesis vs non-thesis, etc.)

---

## Implementation Dates

- **Design**: Current session
- **Coding**: Current session
- **Local Testing**: ✅ Current session
- **Ready for Production**: ✅ Current session
- **Production Deployment**: TBD

---

## Conclusion

✅ **PRD 2.2 fully implemented and tested**

All requirements from PRD 2.2 have been implemented:
- Version-controlled degree charts
- Elective course groups
- Polymorphic chart positions
- Complete admin interface
- Data integrity enforced

Ready for production deployment to PythonAnywhere.
