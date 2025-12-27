from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class StudentCourseHistory(models.Model):
    """
    Track student's passed courses and grades.
    """
    
    GRADE_CHOICES = [
        ('A', 'A (4.0)'),
        ('A-', 'A- (3.7)'),
        ('B+', 'B+ (3.3)'),
        ('B', 'B (3.0)'),
        ('B-', 'B- (2.7)'),
        ('C+', 'C+ (2.3)'),
        ('C', 'C (2.0)'),
        ('D', 'D (1.0)'),
        ('F', 'F (0.0)'),
        ('W', 'W (Withdrawal)'),
    ]
    
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_history',
        limit_choices_to={'role': 'student'},
        help_text=_("Student user")
    )
    
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='student_histories',
        help_text=_("Course taken")
    )
    
    grade = models.CharField(
        max_length=3,
        choices=GRADE_CHOICES,
        help_text=_("Grade received")
    )
    
    grade_points = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(4.0)],
        help_text=_("Grade points (0.0-4.0)")
    )
    
    semester = models.CharField(
        max_length=10,
        help_text=_("Semester taken (e.g., Spring 1402, Fall 1401)")
    )
    
    credits_earned = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
        help_text=_("Credits earned (0 if failed)")
    )
    
    is_passed = models.BooleanField(
        default=True,
        help_text=_("Is course passed?")
    )
    
    notes = models.TextField(
        blank=True,
        help_text=_("Additional notes")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("student course history")
        verbose_name_plural = _("student course histories")
        ordering = ['-semester', '-created_at']
        unique_together = ('student', 'course', 'semester')
    
    def __str__(self):
        return f"{self.student.username} - {self.course.code} ({self.semester})"
    
    @property
    def is_passed_with_grade(self):
        """Check if grade is passing (D or higher)."""
        passing_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D']
        return self.grade in passing_grades


class StudentSelection(models.Model):
    """
    Track student's current course selections for upcoming semester.
    """
    
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_selections',
        limit_choices_to={'role': 'student'},
        help_text=_("Student user")
    )
    
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='student_selections',
        help_text=_("Selected course")
    )
    
    semester = models.CharField(
        max_length=10,
        help_text=_("Semester for selection (e.g., Spring 1403)")
    )
    
    selected_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Date of selection")
    )
    
    is_confirmed = models.BooleanField(
        default=False,
        help_text=_("Is selection confirmed by student?")
    )
    
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Date of confirmation")
    )
    
    notes = models.TextField(
        blank=True,
        help_text=_("Student notes for this course selection")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("student course selection")
        verbose_name_plural = _("student course selections")
        ordering = ['-selected_at']
        unique_together = ('student', 'course', 'semester')
    
    def __str__(self):
        return f"{self.student.username} - {self.course.code} ({self.semester})"


class Schedule(models.Model):
    """
    Weekly schedule for a student's selected courses.
    """
    
    DAYS_OF_WEEK = [
        ('sat', _('Saturday')),
        ('sun', _('Sunday')),
        ('mon', _('Monday')),
        ('tue', _('Tuesday')),
        ('wed', _('Wednesday')),
        ('thu', _('Thursday')),
        ('fri', _('Friday')),
    ]
    
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='schedules',
        limit_choices_to={'role': 'student'},
        help_text=_("Student user")
    )
    
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='schedules',
        help_text=_("Course in schedule")
    )
    
    day_of_week = models.CharField(
        max_length=3,
        choices=DAYS_OF_WEEK,
        help_text=_("Day of week")
    )
    
    start_time = models.TimeField(
        help_text=_("Start time")
    )
    
    end_time = models.TimeField(
        help_text=_("End time")
    )
    
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Class location/room")
    )
    
    semester = models.CharField(
        max_length=10,
        help_text=_("Semester for schedule")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("schedule")
        verbose_name_plural = _("schedules")
        ordering = ['semester', 'day_of_week', 'start_time']
    
    def __str__(self):
        return f"{self.course.code} - {self.get_day_of_week_display()}"
    
    @property
    def has_conflict(self):
        """Check if this schedule conflicts with other schedules."""
        conflicts = Schedule.objects.filter(
            student=self.student,
            semester=self.semester,
            day_of_week=self.day_of_week
        ).exclude(pk=self.pk)
        
        for other in conflicts:
            # Check for time overlap
            if not (self.end_time <= other.start_time or self.start_time >= other.end_time):
                return True
        
        return False

