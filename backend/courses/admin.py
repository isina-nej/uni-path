from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    DegreeChart, Course, ChartCourse, Prerequisite, CoRequisite, CourseRequirement,
    ChartSchema, CourseGroup, ChartNode
)


# Inline admin classes - must be defined before they're used
class ChartCourseInline(admin.TabularInline):
    """
    Inline admin for ChartCourse in DegreeChart admin.
    """
    model = ChartCourse
    extra = 0
    fields = ('course', 'is_mandatory', 'recommended_semester')
    readonly_fields = ()


class PrerequisiteInline(admin.TabularInline):
    """
    Inline admin for Prerequisites in Course admin.
    """
    model = Prerequisite
    extra = 0
    fk_name = 'course'
    fields = ('prerequisite_course', 'is_corequisite', 'min_grade')


@admin.register(DegreeChart)
class DegreeChartAdmin(admin.ModelAdmin):
    """
    Degree Chart (Major) admin with entry year range and field code support.
    """
    
    list_display = ('code', 'name', 'level', 'start_year', 'end_year', 'field_code', 'total_credits')
    list_filter = ('level', 'start_year', 'end_year', 'department', 'created_at')
    search_fields = ('code', 'name', 'department', 'field_code')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'code', 'department', 'total_credits')
        }),
        (_('Entry Year Range'), {
            'fields': ('start_year', 'end_year'),
            'description': _('Entry years this degree chart applies to (e.g., 1392-1402)')
        }),
        (_('Classification'), {
            'fields': ('level', 'field_code'),
            'description': _('Education level and field code for student ID generation')
        }),
        (_('Description'), {
            'fields': ('description',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [ChartCourseInline]


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
    inlines = [PrerequisiteInline]


@admin.register(ChartCourse)
class ChartCourseAdmin(admin.ModelAdmin):
    """
    Chart Course admin.
    """
    
    list_display = ('degree_chart', 'course', 'is_mandatory', 'recommended_semester')
    list_filter = ('degree_chart', 'is_mandatory', 'recommended_semester')
    search_fields = ('degree_chart__name', 'course__code', 'course__name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('Relationship'), {
            'fields': ('degree_chart', 'course')
        }),
        (_('Configuration'), {
            'fields': ('is_mandatory', 'recommended_semester')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


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


@admin.register(CourseRequirement)
class CourseRequirementAdmin(admin.ModelAdmin):
    """
    Course Requirement admin - Track minimum unit requirements.
    Example: Capstone course requires 100 passed units.
    """
    
    list_display = ('course', 'min_passed_units', 'created_at')
    list_filter = ('min_passed_units', 'created_at')
    search_fields = ('course__code', 'course__name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('Requirement'), {
            'fields': ('course', 'min_passed_units'),
            'description': _('Minimum units that must be passed before this course')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ChartNodeInline(admin.TabularInline):
    """
    Inline admin for ChartNode in ChartSchema admin.
    Allows editing course positions directly in the chart.
    """
    model = ChartNode
    extra = 0
    fields = ('semester', 'position', 'course', 'course_group', 'is_mandatory')
    ordering = ['semester', 'position']


@admin.register(ChartSchema)
class ChartSchemaAdmin(admin.ModelAdmin):
    """
    Chart Schema admin - Manage degree program versions.
    Allows creating and versioning degree programs by entry year.
    
    Example: Computer Science Bachelor for entry years 1392-1402
    """
    
    list_display = ('name', 'major', 'degree', 'entry_year_start', 'entry_year_end', 'total_credits', 'is_active')
    list_filter = ('major', 'degree', 'entry_year_start', 'is_active', 'created_at')
    search_fields = ('name', 'code', 'major')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'code', 'description')
        }),
        (_('Classification'), {
            'fields': ('major', 'degree'),
            'description': _('Field of study and degree level')
        }),
        (_('Entry Year Range'), {
            'fields': ('entry_year_start', 'entry_year_end'),
            'description': _('This schema applies to students entering between these years')
        }),
        (_('Metadata'), {
            'fields': ('total_credits', 'is_active')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ChartNodeInline]


@admin.register(CourseGroup)
class CourseGroupAdmin(admin.ModelAdmin):
    """
    Course Group admin - Manage elective course groups.
    
    Example: "Technical Electives" group contains Data Mining, Cloud Computing, etc.
    A student must choose one course from this group.
    """
    
    list_display = ('name', 'code', 'course_count', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('courses',)
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'code', 'description')
        }),
        (_('Courses in Group'), {
            'fields': ('courses',),
            'description': _('Select all courses that belong to this elective group')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def course_count(self, obj):
        """Display number of courses in group"""
        return obj.courses.count()
    course_count.short_description = _('# Courses')


@admin.register(ChartNode)
class ChartNodeAdmin(admin.ModelAdmin):
    """
    Chart Node admin - Manage individual positions in a degree chart.
    
    Each node is either:
    - A required course (e.g., "ریاضی ۱")
    - An elective slot (e.g., "Choose one: Technical Electives")
    """
    
    list_display = ('schema', 'semester', 'position', 'node_type', 'is_mandatory', 'created_at')
    list_filter = ('schema', 'semester', 'is_mandatory', 'created_at')
    search_fields = ('schema__name', 'course__code', 'course__name', 'course_group__name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('Position'), {
            'fields': ('schema', 'semester', 'position'),
            'description': _('Where in the chart this node appears')
        }),
        (_('Content - Choose One'), {
            'fields': ('course', 'course_group'),
            'description': _('Either a specific required course OR an elective group (not both)')
        }),
        (_('Status'), {
            'fields': ('is_mandatory',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def node_type(self, obj):
        """Display whether this is a required course or elective slot"""
        if obj.course:
            return f"📚 Course: {obj.course.code}"
        else:
            return f"🎯 Elective: {obj.course_group.name}"
    node_type.short_description = _('Type')

