from rest_framework import serializers
from .models import StudentCourseHistory, StudentSelection, Schedule
from courses.serializers import CourseSerializer


class StudentCourseHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for student course history.
    """
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = StudentCourseHistory
        fields = (
            'id', 'student', 'course', 'course_id', 'grade', 'grade_points',
            'semester', 'credits_earned', 'is_passed', 'is_passed_with_grade',
            'notes', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'student', 'created_at', 'updated_at')


class StudentSelectionSerializer(serializers.ModelSerializer):
    """
    Serializer for student course selection.
    """
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = StudentSelection
        fields = (
            'id', 'student', 'course', 'course_id', 'semester',
            'selected_at', 'is_confirmed', 'confirmed_at', 'notes',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'student', 'selected_at', 'created_at', 'updated_at')


class ScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for student schedule.
    """
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    has_conflict = serializers.SerializerMethodField()
    
    class Meta:
        model = Schedule
        fields = (
            'id', 'student', 'course', 'course_id', 'day_of_week',
            'start_time', 'end_time', 'location', 'semester',
            'has_conflict', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'student', 'has_conflict', 'created_at', 'updated_at')
    
    def get_has_conflict(self, obj):
        """Check if schedule has conflicts."""
        return obj.has_conflict
