from rest_framework import serializers
from .models import DegreeChart, Course, ChartCourse, Prerequisite, CoRequisite


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model.
    """
    
    class Meta:
        model = Course
        fields = (
            'id', 'name', 'code', 'description', 'credits', 'unit_type',
            'theoretical_units', 'practical_units', 'day_of_week',
            'start_time', 'end_time', 'semester', 'is_mandatory',
            'is_offered', 'instructor', 'capacity', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class PrerequisiteSerializer(serializers.ModelSerializer):
    """
    Serializer for Prerequisite model.
    """
    prerequisite_course = CourseSerializer(read_only=True)
    prerequisite_course_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Prerequisite
        fields = (
            'id', 'course', 'prerequisite_course', 'prerequisite_course_id',
            'is_corequisite', 'min_grade', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class CoRequisiteSerializer(serializers.ModelSerializer):
    """
    Serializer for CoRequisite model.
    """
    corequisite_course = CourseSerializer(read_only=True)
    corequisite_course_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = CoRequisite
        fields = (
            'id', 'course', 'corequisite_course', 'corequisite_course_id', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class CourseDetailSerializer(CourseSerializer):
    """
    Detailed course serializer with prerequisites and co-requisites.
    """
    prerequisites = serializers.SerializerMethodField()
    corequisites = serializers.SerializerMethodField()
    
    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ('prerequisites', 'corequisites')
    
    def get_prerequisites(self, obj):
        """Get prerequisites for this course."""
        prerequisites = Prerequisite.objects.filter(course=obj)
        return PrerequisiteSerializer(prerequisites, many=True).data
    
    def get_corequisites(self, obj):
        """Get co-requisites for this course."""
        corequisites = CoRequisite.objects.filter(course=obj)
        return CoRequisiteSerializer(corequisites, many=True).data


class ChartCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for ChartCourse (course in degree chart).
    """
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ChartCourse
        fields = (
            'id', 'degree_chart', 'course', 'course_id', 'is_mandatory',
            'recommended_semester', 'importance_score', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'importance_score', 'created_at', 'updated_at')


class DegreeChartSerializer(serializers.ModelSerializer):
    """
    Serializer for DegreeChart (major).
    """
    
    class Meta:
        model = DegreeChart
        fields = (
            'id', 'name', 'code', 'description', 'department',
            'total_credits', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class DegreeChartDetailSerializer(DegreeChartSerializer):
    """
    Detailed degree chart serializer with courses.
    """
    courses = serializers.SerializerMethodField()
    
    class Meta(DegreeChartSerializer.Meta):
        fields = DegreeChartSerializer.Meta.fields + ('courses',)
    
    def get_courses(self, obj):
        """Get all courses for this degree chart."""
        chart_courses = ChartCourse.objects.filter(degree_chart=obj).select_related('course')
        return ChartCourseSerializer(chart_courses, many=True).data
