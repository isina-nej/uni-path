# Spec Delta: Degree Chart Models

## File: backend/courses/models.py

### MODIFIED Requirement: DegreeChart Model
Redesign DegreeChart to support entry year ranges and proper curriculum structure.

**Current Issues:**
- Missing `start_year`, `end_year` fields for entry year ranges
- No link between courses and degree charts with semester information
- Cannot organize courses by semester

**Changes:**
```python
class DegreeChart(models.Model):
    """
    Represents a degree program (Major) with its curriculum structure.
    Supports multiple entry years with different versions of the curriculum.
    """
    
    # Existing fields
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    department = models.CharField(max_length=255)
    total_credits = models.IntegerField(default=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # NEW: Entry year range
    start_year = models.IntegerField(
        default=1392,
        help_text="First entry year this degree chart applies to (e.g., 1392)"
    )
    end_year = models.IntegerField(
        default=1402,
        help_text="Last entry year this degree chart applies to (e.g., 1402)"
    )
    
    # NEW: Field code for student number generation
    field_code = models.CharField(
        max_length=10,
        default='102',
        help_text="Field code for student IDs (e.g., 102 for CS)"
    )
    
    # NEW: Education level (bachelor, masters, phd)
    level = models.CharField(
        max_length=20,
        choices=[
            ('12', 'کارشناسی'),
            ('13', 'کارشناسی ارشد'),
            ('14', 'دکتری'),
        ],
        default='12'
    )
    
    # Link to courses
    courses = models.ManyToManyField(
        'Course',
        through='DegreeChartCourse',
        related_name='degree_charts'
    )
```

#### Scenario:
Creating degree chart for Computer Engineering, entry years 1392-1402:
```python
chart = DegreeChart.objects.create(
    name='مهندسی کامپیوتر - کارشناسی',
    code='CE-BS-92-402',
    department='مهندسی',
    start_year=1392,
    end_year=1402,
    field_code='102',
    level='12',
    total_credits=132
)
```

---

### ADDED Requirement: DegreeChartCourse Model
Link courses to degree charts with semester information for organizing curriculum.

**New Model:**
```python
class DegreeChartCourse(models.Model):
    """
    Through model linking courses to degree charts with semester information.
    Allows organizing courses by semester within a degree program.
    """
    
    degree_chart = models.ForeignKey(
        'DegreeChart',
        on_delete=models.CASCADE,
        related_name='chart_courses'
    )
    
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE
    )
    
    semester = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        help_text="Semester number (1-8)"
    )
    
    is_mandatory = models.BooleanField(
        default=True,
        help_text="Is this course mandatory in the degree?"
    )
    
    order = models.IntegerField(
        default=0,
        help_text="Display order within semester"
    )
    
    class Meta:
        unique_together = [['degree_chart', 'course']]
        ordering = ['semester', 'order']
    
    def __str__(self):
        return f"{self.degree_chart.code} - {self.course.code} (Sem {self.semester})"
```

#### Scenario:
Adding Mathematics 1 to semester 1 of CE degree chart:
```python
DegreeChartCourse.objects.create(
    degree_chart=chart,
    course=math_course,
    semester=1,
    is_mandatory=True,
    order=2
)
```

---

### ADDED Requirement: CourseRequirement Model
Track minimum unit requirements before enrollment in a course.

**New Model:**
```python
class CourseRequirement(models.Model):
    """
    Specifies prerequisites based on minimum units passed.
    Example: Can enroll in course X only after passing 80 units.
    """
    
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='unit_requirements'
    )
    
    min_passed_units = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Minimum units that must be passed before this course"
    )
    
    def __str__(self):
        return f"{self.course.code} - Min {self.min_passed_units} units"
```

#### Scenario:
Capstone project requires 100 passed units:
```python
CourseRequirement.objects.create(
    course=capstone_course,
    min_passed_units=100
)
```

---

### MODIFIED Requirement: Prerequisite Model Structure
Verify the existing Prerequisite model is properly structured with `is_corequisite` field.

**Needed Fields:**
- `course` - ForeignKey to Course (course that has prerequisite)
- `prerequisite_course` - ForeignKey to Course (the required course)
- `is_corequisite` - Boolean flag (True = must take together, False = must complete before)
- `min_grade` - Optional minimum grade requirement

#### Scenario:
Setting up prerequisites: Algorithms requires Data Structures:
```python
Prerequisite.objects.create(
    course=algorithms,
    prerequisite_course=data_structures,
    is_corequisite=False
)

# Or co-requisite: Discrete Math must be taken with Algorithms
Prerequisite.objects.create(
    course=algorithms,
    prerequisite_course=discrete_math,
    is_corequisite=True
)
```

---

## File: backend/courses/admin.py

### ADDED Requirement: Register New Models in Django Admin

```python
from .models import DegreeChart, DegreeChartCourse, CourseRequirement

# Inline admin for DegreeChartCourse
class DegreeChartCourseInline(admin.TabularInline):
    model = DegreeChartCourse
    extra = 0
    fields = ['course', 'semester', 'is_mandatory', 'order']

# Admin for DegreeChart
class DegreeChartAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'level', 'start_year', 'end_year', 'total_credits']
    list_filter = ['level', 'start_year']
    search_fields = ['name', 'code']
    inlines = [DegreeChartCourseInline]

# Register models
admin.site.register(DegreeChart, DegreeChartAdmin)
admin.site.register(DegreeChartCourse)
admin.site.register(CourseRequirement)
```

#### Scenario:
Admin can view CS degree chart with all courses organized by semester.
