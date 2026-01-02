from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class DegreeChart(models.Model):
    """
    Represents a degree program (Major) with its curriculum structure.
    Supports multiple entry years with different versions of the curriculum.
    Example: Computer Science degree for entry years 1392-1402
    """
    
    LEVEL_CHOICES = [
        ('12', _('کارشناسی (Bachelor)')),
        ('13', _('کارشناسی ارشد (Masters)')),
        ('14', _('دکتری (PhD)')),
    ]
    
    name = models.CharField(
        max_length=255,
        help_text=_("Name of the degree program (e.g., Computer Science)")
    )
    
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text=_("Unique code for the degree program (e.g., CS-BS-92-402)")
    )
    
    description = models.TextField(
        blank=True,
        help_text=_("Description of the degree program")
    )
    
    department = models.CharField(
        max_length=255,
        help_text=_("Department name")
    )
    
    total_credits = models.IntegerField(
        default=120,
        validators=[MinValueValidator(30), MaxValueValidator(200)],
        help_text=_("Total credits required for this degree")
    )
    
    # NEW FIELDS FOR ENTRY YEAR RANGE
    start_year = models.IntegerField(
        default=1392,
        help_text=_("First entry year this degree chart applies to (e.g., 1392)")
    )
    
    end_year = models.IntegerField(
        default=1402,
        help_text=_("Last entry year this degree chart applies to (e.g., 1402)")
    )
    
    # NEW FIELD FOR FIELD CODE (USED IN STUDENT IDS)
    field_code = models.CharField(
        max_length=10,
        default='102',
        help_text=_("Field code for student IDs (e.g., 102 for CS)")
    )
    
    # NEW FIELD FOR EDUCATION LEVEL
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='12',
        help_text=_("Education level")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("degree chart")
        verbose_name_plural = _("degree charts")
        ordering = ['-start_year', 'name']
        # Allow same program for different entry year ranges or levels
        indexes = [
            models.Index(fields=['field_code', 'level']),
            models.Index(fields=['start_year', 'end_year']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code}) - {self.start_year}-{self.end_year}"
    
    def is_active_for_year(self, entry_year):
        """Check if this degree chart is active for given entry year"""
        return self.start_year <= entry_year <= self.end_year


class Course(models.Model):
    """
    Represents a single course in the system.
    """
    
    UNIT_TYPE_CHOICES = [
        ('theory', _('Theoretical')),
        ('practical', _('Practical')),
        ('both', _('Theory + Practical')),
    ]
    
    name = models.CharField(
        max_length=255,
        help_text=_("Course name")
    )
    
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text=_("Course code (e.g., CS101)")
    )
    
    description = models.TextField(
        blank=True,
        help_text=_("Course description")
    )
    
    credits = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        help_text=_("Number of credits")
    )
    
    unit_type = models.CharField(
        max_length=20,
        choices=UNIT_TYPE_CHOICES,
        default='both',
        help_text=_("Type of course")
    )
    
    theoretical_units = models.IntegerField(
        default=0,
        help_text=_("Number of theoretical units/hours per week")
    )
    
    practical_units = models.IntegerField(
        default=0,
        help_text=_("Number of practical units/hours per week")
    )
    
    # For schedule planning
    day_of_week = models.CharField(
        max_length=20,
        blank=True,
        help_text=_("Day of week (Sat, Sun, Mon, Tue, Wed, Thu)")
    )
    
    start_time = models.TimeField(
        null=True,
        blank=True,
        help_text=_("Start time of the course")
    )
    
    end_time = models.TimeField(
        null=True,
        blank=True,
        help_text=_("End time of the course")
    )
    
    semester = models.IntegerField(
        null=True,
        blank=True,
        help_text=_("Recommended semester (1-8)")
    )
    
    is_mandatory = models.BooleanField(
        default=True,
        help_text=_("Is this course mandatory for the degree?")
    )
    
    is_offered = models.BooleanField(
        default=True,
        help_text=_("Is this course currently being offered?")
    )
    
    instructor = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Instructor/Professor name")
    )
    
    capacity = models.IntegerField(
        null=True,
        blank=True,
        help_text=_("Maximum student capacity")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class ChartCourse(models.Model):
    """
    Junction model: Links courses to degree charts (many-to-many with extra data).
    Represents which courses belong to which degree program.
    """
    
    degree_chart = models.ForeignKey(
        DegreeChart,
        on_delete=models.CASCADE,
        related_name='chart_courses',
        help_text=_("The degree program")
    )
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='chart_offerings',
        help_text=_("The course")
    )
    
    is_mandatory = models.BooleanField(
        default=True,
        help_text=_("Is this course mandatory for this program?")
    )
    
    recommended_semester = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        help_text=_("Recommended semester to take this course")
    )
    
    importance_score = models.FloatField(
        default=0.0,
        help_text=_("Calculated importance score (# of dependent courses)")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("chart course")
        verbose_name_plural = _("chart courses")
        unique_together = ('degree_chart', 'course')
        ordering = ['recommended_semester', 'course__code']
    
    def __str__(self):
        return f"{self.course.code} in {self.degree_chart.code}"


class Prerequisite(models.Model):
    """
    Represents prerequisite relationships between courses.
    """
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='prerequisites_for',
        help_text=_("The course that requires prerequisites")
    )
    
    prerequisite_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='prerequisites_of',
        help_text=_("The course that must be completed first")
    )
    
    is_corequisite = models.BooleanField(
        default=False,
        help_text=_("Is this a co-requisite? (can be taken at the same time)")
    )
    
    min_grade = models.CharField(
        max_length=2,
        default='D',
        help_text=_("Minimum grade required in prerequisite (A, B, C, D)")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("prerequisite")
        verbose_name_plural = _("prerequisites")
        unique_together = ('course', 'prerequisite_course')
    
    def __str__(self):
        prereq_type = "co-req" if self.is_corequisite else "pre-req"
        return f"{self.prerequisite_course.code} {prereq_type} for {self.course.code}"


class CoRequisite(models.Model):
    """
    Represents co-requisite relationships between courses.
    Co-requisites can be taken at the same time as the course.
    """
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='corequisites_for',
        help_text=_("The course that requires co-requisites")
    )
    
    corequisite_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='corequisites_of',
        help_text=_("The course that must be taken at the same time")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("co-requisite")
        verbose_name_plural = _("co-requisites")
        unique_together = ('course', 'corequisite_course')
    
    def __str__(self):
        return f"{self.corequisite_course.code} co-req with {self.course.code}"


class CourseRequirement(models.Model):
    """
    Specifies prerequisite requirements based on minimum units passed.
    Example: Can enroll in Capstone only after passing 100 units.
    This is different from direct course prerequisites (Prerequisite model).
    """
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='unit_requirements',
        help_text=_("The course that has unit requirement")
    )
    
    min_passed_units = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(200)],
        help_text=_("Minimum units that must be passed before this course")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("course requirement")
        verbose_name_plural = _("course requirements")
        unique_together = ('course', 'min_passed_units')
    
    def __str__(self):
        return f"{self.course.code} - Min {self.min_passed_units} units"


class ChartSchema(models.Model):
    """
    Represents a specific version of a degree program.
    Allows multiple degree programs (Bachelor, Masters, PhD) for same major.
    Supports versioning by entry year ranges.
    
    Example: Computer Science Bachelor for entry years 1392-1402
    """
    
    MAJOR_CHOICES = [
        ('CS', _('مهندسی کامپیوتر (Computer Science)')),
        ('EE', _('مهندسی برق (Electrical Engineering)')),
        ('CE', _('مهندسی عمران (Civil Engineering)')),
        ('ME', _('مهندسی مکانیک (Mechanical Engineering)')),
        ('SE', _('مهندسی نرم‌افزار (Software Engineering)')),
    ]
    
    DEGREE_CHOICES = [
        ('12', _('کارشناسی (Bachelor)')),
        ('13', _('کارشناسی ارشد (Masters)')),
        ('14', _('دکتری (PhD)')),
    ]
    
    # Basic info
    name = models.CharField(
        max_length=255,
        help_text=_("Display name (e.g., مهندسی کامپیوتر - کارشناسی)")
    )
    
    code = models.CharField(
        max_length=50,
        help_text=_("Schema code (e.g., CS-BS-92-402)")
    )
    
    description = models.TextField(
        blank=True,
        help_text=_("Description of this degree program version")
    )
    
    # Classification
    major = models.CharField(
        max_length=20,
        choices=MAJOR_CHOICES,
        help_text=_("Field of study")
    )
    
    degree = models.CharField(
        max_length=20,
        choices=DEGREE_CHOICES,
        default='12',
        help_text=_("Degree level")
    )
    
    # Entry year range
    entry_year_start = models.IntegerField(
        validators=[MinValueValidator(1300), MaxValueValidator(1500)],
        help_text=_("First entry year (e.g., 1392)")
    )
    
    entry_year_end = models.IntegerField(
        validators=[MinValueValidator(1300), MaxValueValidator(1500)],
        help_text=_("Last entry year (e.g., 1402)")
    )
    
    # Metadata
    total_credits = models.IntegerField(
        default=120,
        validators=[MinValueValidator(30), MaxValueValidator(200)],
        help_text=_("Total credits required")
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text=_("Is this schema currently active?")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("chart schema")
        verbose_name_plural = _("chart schemas")
        unique_together = [('major', 'degree', 'entry_year_start', 'entry_year_end')]
        ordering = ['-entry_year_start', 'major']
        indexes = [
            models.Index(fields=['major', 'degree']),
            models.Index(fields=['entry_year_start', 'entry_year_end']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.entry_year_start}-{self.entry_year_end})"
    
    def is_valid_for_year(self, entry_year):
        """Check if this schema is valid for given entry year"""
        return self.entry_year_start <= entry_year <= self.entry_year_end
    
    def get_semester_from_course_id(self, course_id):
        """
        Extract semester from course code.
        Course ID format: XYZ where X is semester.
        Examples: 101 -> Semester 1, 801 -> Semester 8
        """
        return (course_id // 100)


class CourseGroup(models.Model):
    """
    Represents a group of courses that serve as electives.
    
    Example: "Technical Electives" group contains:
    - Data Mining (703)
    - Cloud Computing (705)
    - Image Processing (701)
    
    A student must choose one from this group for their elective slot.
    """
    
    name = models.CharField(
        max_length=255,
        help_text=_("Group name (e.g., Technical Electives)")
    )
    
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text=_("Unique code (e.g., TECH-ELECTIVE)")
    )
    
    description = models.TextField(
        blank=True,
        help_text=_("Description of what this group contains")
    )
    
    courses = models.ManyToManyField(
        'Course',
        related_name='course_groups',
        help_text=_("Courses available in this group")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("course group")
        verbose_name_plural = _("course groups")
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.courses.count()} courses)"


class ChartNode(models.Model):
    """
    Represents a single position/slot in a degree chart.
    
    Each node is either:
    1. A specific required course (e.g., "ریاضی ۱")
    2. An elective slot pointing to a group (e.g., "Choose one: Technical Electives")
    
    Example for Computer Science:
    - Semester 1, Position 1: Specific course "فیزیک ۱" (101)
    - Semester 6, Position 3: Elective group "Technical Electives" (courses: 701, 703, 705)
    """
    
    schema = models.ForeignKey(
        'ChartSchema',
        on_delete=models.CASCADE,
        related_name='nodes',
        help_text=_("The chart schema this node belongs to")
    )
    
    semester = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        help_text=_("Semester number (1-8)")
    )
    
    position = models.IntegerField(
        default=0,
        help_text=_("Display order within semester")
    )
    
    # Either a specific course OR a course group (not both, not neither)
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='chart_nodes_specific',
        help_text=_("If specified, this is a required course")
    )
    
    course_group = models.ForeignKey(
        'CourseGroup',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='chart_nodes',
        help_text=_("If specified, student chooses one from this group")
    )
    
    is_mandatory = models.BooleanField(
        default=True,
        help_text=_("Is this course/group mandatory?")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("chart node")
        verbose_name_plural = _("chart nodes")
        unique_together = [('schema', 'semester', 'position')]
        ordering = ['semester', 'position']
    
    def clean(self):
        """Validate that exactly one of course or course_group is set"""
        from django.core.exceptions import ValidationError
        
        if not self.course and not self.course_group:
            raise ValidationError(_("Either a specific course or a course group must be selected."))
        
        if self.course and self.course_group:
            raise ValidationError(_("A node cannot have both a specific course and a group. Choose one."))
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.course:
            return f"{self.schema.code} - Sem {self.semester}: {self.course.code}"
        else:
            return f"{self.schema.code} - Sem {self.semester}: {self.course_group.name}"
    
    @property
    def is_elective_slot(self):
        """Returns True if this node is an elective slot"""
        return self.course_group is not None
    
    @property
    def is_required_course(self):
        """Returns True if this node is a required specific course"""
        return self.course is not None


