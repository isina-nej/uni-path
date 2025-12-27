from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    DegreeChart, Course, ChartCourse, Prerequisite, CoRequisite
)


@admin.register(DegreeChart)
class DegreeChartAdmin(admin.ModelAdmin):
    """
    Degree Chart (Major) admin.
    """
    
    list_display = ('code', 'name', 'department', 'total_credits', 'created_at')
    list_filter = ('department', 'created_at', 'updated_at')
    search_fields = ('code', 'name', 'department')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'code', 'department', 'total_credits')
        }),
        (_('Description'), {
            'fields': ('description',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Course admin.
    """
    
    list_display = ('code', 'name', 'credits', 'unit_type', 'is_offered', 'is_mandatory')
    list_filter = ('unit_type', 'is_offered', 'is_mandatory', 'created_at')
    search_fields = ('code', 'name', 'instructor')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'code', 'credits', 'unit_type')
        }),
        (_('Units'), {
            'fields': ('theoretical_units', 'practical_units')
        }),
        (_('Schedule'), {
            'fields': ('day_of_week', 'start_time', 'end_time', 'semester')
        }),
        (_('Additional Information'), {
            'fields': ('description', 'instructor', 'capacity')
        }),
        (_('Status'), {
            'fields': ('is_offered', 'is_mandatory')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ChartCourseInline(admin.TabularInline):
    """
    Inline admin for ChartCourse in DegreeChart admin.
    """
    model = ChartCourse
    extra = 0
    fields = ('course', 'is_mandatory', 'recommended_semester', 'importance_score')
    readonly_fields = ('importance_score',)


@admin.register(ChartCourse)
class ChartCourseAdmin(admin.ModelAdmin):
    """
    Chart Course admin.
    """
    
    list_display = ('degree_chart', 'course', 'is_mandatory', 'recommended_semester', 'importance_score')
    list_filter = ('degree_chart', 'is_mandatory', 'recommended_semester')
    search_fields = ('degree_chart__name', 'course__code', 'course__name')
    readonly_fields = ('created_at', 'updated_at', 'importance_score')
    
    fieldsets = (
        (_('Relationship'), {
            'fields': ('degree_chart', 'course')
        }),
        (_('Configuration'), {
            'fields': ('is_mandatory', 'recommended_semester', 'importance_score')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class PrerequisiteInline(admin.TabularInline):
    """
    Inline admin for Prerequisites in Course admin.
    """
    model = Prerequisite
    extra = 0
    fk_name = 'course'
    fields = ('prerequisite_course', 'is_corequisite', 'min_grade')


@admin.register(Prerequisite)
class PrerequisiteAdmin(admin.ModelAdmin):
    """
    Prerequisite admin.
    """
    
    list_display = ('course', 'prerequisite_course', 'is_corequisite', 'min_grade')
    list_filter = ('is_corequisite', 'min_grade', 'created_at')
    search_fields = ('course__code', 'prerequisite_course__code')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        (_('Relationship'), {
            'fields': ('course', 'prerequisite_course')
        }),
        (_('Configuration'), {
            'fields': ('is_corequisite', 'min_grade')
        }),
        (_('Timestamps'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(CoRequisite)
class CoRequisiteAdmin(admin.ModelAdmin):
    """
    Co-requisite admin.
    """
    
    list_display = ('course', 'corequisite_course', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('course__code', 'corequisite_course__code')
    readonly_fields = ('created_at',)

