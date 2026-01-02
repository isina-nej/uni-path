"""
Serializers for Degree Chart API (PRD 3.1)
"""

from rest_framework import serializers
from courses.models import ChartSchema, ChartNode, Course, CourseGroup, CourseRequirement


class PrerequisiteSerializer(serializers.ModelSerializer):
    """فقط کد درس پیشنیاز"""
    class Meta:
        model = CourseRequirement
        fields = ['prerequisite']


class CourseDetailSerializer(serializers.ModelSerializer):
    """جزئیات درس شامل پیشنیازها"""
    prerequisites = serializers.SerializerMethodField()
    corequisites = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'code', 'name', 'credits', 'semester',
            'is_elective', 'prerequisites', 'corequisites'
        ]
    
    def get_prerequisites(self, obj):
        """دریافت کد‌های درس‌های پیشنیاز"""
        reqs = CourseRequirement.objects.filter(course=obj)
        return [
            {
                'id': req.prerequisite_id,
                'code': req.prerequisite.code,
                'name': req.prerequisite.name,
            }
            for req in reqs
        ]
    
    def get_corequisites(self, obj):
        """دریافت کد‌های درس‌های همنیاز"""
        coreqs = obj.corequisites.all()
        return [
            {'id': c.id, 'code': c.code, 'name': c.name}
            for c in coreqs
        ]


class CourseGroupDetailSerializer(serializers.ModelSerializer):
    """گروه درس‌های اختیاری"""
    courses = CourseDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = CourseGroup
        fields = ['id', 'name', 'code', 'courses']


class ChartNodeSerializer(serializers.ModelSerializer):
    """نود در چارت (درس یا گروه اختیاری)"""
    course = CourseDetailSerializer(read_only=True)
    course_group = CourseGroupDetailSerializer(read_only=True)
    is_elective_slot = serializers.SerializerMethodField()
    node_type = serializers.SerializerMethodField()
    
    class Meta:
        model = ChartNode
        fields = [
            'id', 'semester', 'position',
            'course', 'course_group',
            'is_elective_slot', 'node_type'
        ]
    
    def get_is_elective_slot(self, obj):
        return obj.is_elective_slot
    
    def get_node_type(self, obj):
        """نوع نود: 'course' یا 'elective'"""
        if obj.course:
            return 'course'
        return 'elective'


class SemesterSerializer(serializers.Serializer):
    """ترم شامل چند نود"""
    number = serializers.IntegerField()
    nodes = ChartNodeSerializer(many=True)
    total_credits = serializers.SerializerMethodField()
    
    def get_total_credits(self, obj):
        """مجموع واحدهای ترم"""
        return sum(
            node.course.credits if node.course else 3
            for node in obj.get('nodes', [])
        )


class ChartSchemaDetailSerializer(serializers.ModelSerializer):
    """جزئیات کامل چارت شامل تمام ترم‌ها"""
    semesters = serializers.SerializerMethodField()
    passed_courses = serializers.SerializerMethodField()
    completed_semesters = serializers.SerializerMethodField()
    
    class Meta:
        model = ChartSchema
        fields = [
            'id', 'code', 'name', 'major', 'degree',
            'entry_year_start', 'entry_year_end',
            'total_credits', 'is_active',
            'semesters', 'passed_courses', 'completed_semesters'
        ]
    
    def get_semesters(self, obj):
        """سازماندهی نودها به ترم‌ها"""
        semesters_data = {}
        
        nodes = ChartNode.objects.filter(schema=obj).select_related(
            'course', 'course_group'
        ).order_by('semester', 'position')
        
        for node in nodes:
            if node.semester not in semesters_data:
                semesters_data[node.semester] = []
            semesters_data[node.semester].append(node)
        
        # Convert to list
        result = []
        for sem_num in range(1, 9):
            if sem_num in semesters_data:
                result.append({
                    'number': sem_num,
                    'nodes': ChartNodeSerializer(
                        semesters_data[sem_num],
                        many=True
                    ).data
                })
        
        return result
    
    def get_passed_courses(self, obj):
        """لیست ID‌های دروس پاس شده توسط کاربر"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            passed = request.user.studentprofile.student_courses.filter(
                is_passed=True
            ).values_list('course_id', flat=True)
            return list(passed)
        return []
    
    def get_completed_semesters(self, obj):
        """تعداد ترم‌های تکمیل شده"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.studentprofile.completed_semesters or 0
        return 0


class CourseRecommendationSerializer(serializers.Serializer):
    """پیشنهاد درس"""
    course_id = serializers.IntegerField()
    code = serializers.CharField()
    name = serializers.CharField()
    credits = serializers.IntegerField()
    priority_score = serializers.IntegerField()  # 0-100
    reason = serializers.CharField()
    unlocks = serializers.ListField(child=serializers.IntegerField())  # course IDs
    prerequisites_met = serializers.BooleanField()
    is_mandatory = serializers.BooleanField()
    is_elective = serializers.BooleanField()
