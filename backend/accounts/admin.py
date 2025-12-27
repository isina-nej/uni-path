from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User model admin with role-based filtering.
    """
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                      'groups', 'user_permissions')
        }),
        (_('Role'), {
            'fields': ('role',)
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    
    list_display = ('username', 'email', 'get_full_name', 'role', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role', 'created_at')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-created_at',)
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = _('Full Name')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Profile model admin.
    """
    
    list_display = ('user', 'student_number', 'major', 'phone', 'created_at')
    list_filter = ('major', 'created_at', 'updated_at')
    search_fields = ('user__username', 'student_number', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('User'), {
            'fields': ('user',)
        }),
        (_('Academic Information'), {
            'fields': ('student_number', 'major', 'department')
        }),
        (_('Personal Information'), {
            'fields': ('phone', 'bio', 'avatar')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

