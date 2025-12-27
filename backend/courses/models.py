from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class DegreeChart(models.Model):
    """
    Represents a degree program (Major) with its curriculum structure.
    """
    
    name = models.CharField(
        max_length=255,
        help_text=_("Name of the degree program (e.g., Computer Science)")
    )
    
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text=_("Unique code for the degree program")
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
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("degree chart")
        verbose_name_plural = _("degree charts")
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


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

