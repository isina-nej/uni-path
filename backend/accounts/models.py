from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model with role-based distinction.
    Supports: Student, Admin, Professor, Head of Department (HOD)
    """
    
    ROLE_CHOICES = [
        ('student', _('Student')),
        ('professor', _('Professor')),
        ('admin', _('Admin')),
        ('hod', _('Head of Department')),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        help_text=_("User role for permission management")
    )
    
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active. "
                    "Unselect this instead of deleting accounts.")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def is_student(self):
        return self.role == 'student'
    
    def is_professor(self):
        return self.role == 'professor'
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_hod(self):
        return self.role == 'hod'


class Profile(models.Model):
    """
    Extended user profile with additional information.
    """
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        help_text=_("User account")
    )
    
    student_number = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        help_text=_("Student ID number")
    )
    
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text=_("Phone number")
    )
    
    bio = models.TextField(
        blank=True,
        help_text=_("User biography")
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        help_text=_("User profile picture")
    )
    
    # For students
    major = models.ForeignKey(
        'courses.DegreeChart',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        help_text=_("Student's major/degree program")
    )
    
    # For professors
    department = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Department for professors")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Profile of {self.user.get_full_name()}"

