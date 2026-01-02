"""
API Views for Degree Chart functionality (PRD 3.1)
- Match ChartSchema based on student ID
- Provide course recommendations with priority scoring
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.contrib.auth import get_user_model

from courses.models import ChartSchema, ChartNode, Course, CourseRequirement
from students.models import StudentCourseHistory
from .serializers_chart import (
    ChartSchemaDetailSerializer,
    CourseRecommendationSerializer,
)

User = get_user_model()


class DegreeChartViewSet(viewsets.ViewSet):
    """
    API endpoints for degree chart functionality.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_chart(self, request):
        """
        GET /api/degrees/my-chart/
        
        Returns the degree chart matching the student's ID.
        Parses entry_year (first 2 digits) and major_code (digits 2-5).
        """
        user = request.user
        
        # Get student profile
        try:
            profile = user.profile
        except:
            return Response(
                {"error": "پروفایل دانشجویی یافت نشد"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        student_id = profile.student_number
        if not student_id or len(student_id) < 5:
            return Response(
                {"error": "شماره دانشجویی نامعتبر است"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parse student ID: xxyyzzznnn
        # xx = entry year (92-99, 00-14)
        # yyy = major code (210 = CS, etc)
        try:
            entry_year_str = student_id[:2]
            major_code_str = student_id[2:5]
            
            # Convert to full year (92 -> 1392, 99 -> 1399, 00 -> 1400, etc)
            entry_year_int = int(entry_year_str)
            if entry_year_int >= 92:
                entry_year = 1300 + entry_year_int
            else:
                entry_year = 1400 + entry_year_int
                
        except (ValueError, IndexError):
            return Response(
                {"error": "خطا در تجزیه شماره دانشجویی"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Map major code to ChartSchema major field
        major_mapping = {
            '210': 'CS',   # کامپیوتر
            '213': 'EE',   # برق
            '201': 'CE',   # عمران
            '211': 'ME',   # مکانیک
            '220': 'SE',   # نرم‌افزار
        }
        
        major = major_mapping.get(major_code_str)
        if not major:
            return Response(
                {"error": f"رشته {major_code_str} شناخته شده نیست"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find matching ChartSchema
        chart = ChartSchema.objects.filter(
            major=major,
            entry_year_start__lte=entry_year,
            entry_year_end__gte=entry_year
        ).first()
        
        if not chart:
            return Response(
                {"error": f"چارت برای رشته {major} سال ورود {entry_year} یافت نشد"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get passed courses for this student
        # Check StudentCourseHistory for passed courses (grade != 'F' and != 'W')
        passed_courses = StudentCourseHistory.objects.filter(
            student=user,
            grade__in=['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D']
        ).values_list('course_id', flat=True)
        
        # Serialize
        serializer = ChartSchemaDetailSerializer(
            chart,
            context={
                'passed_courses': list(passed_courses),
                'completed_semesters': 0,  # TODO: Calculate from StudentCourseHistory
                'request': request,
            }
        )
        
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        """
        GET /api/degrees/recommendations/
        
        Returns recommended courses for the next semester.
        Sorts by priority score based on:
        - Number of dependent courses (courses that require this one)
        - Strategic weight
        - Prerequisites being met
        """
        user = request.user
        
        # Get student profile
        try:
            profile = user.profile
        except:
            return Response(
                {"error": "پروفایل دانشجویی یافت نشد"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get passed courses from StudentCourseHistory
        passed_courses = set(
            StudentCourseHistory.objects.filter(
                student=user,
                grade__in=['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D']
            ).values_list('course_id', flat=True)
        )
        
        # Get student's chart
        student_id = profile.student_number
        if not student_id or len(student_id) < 5:
            return Response(
                {"error": "شماره دانشجویی نامعتبر است"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        entry_year_str = student_id[:2]
        major_code_str = student_id[2:5]
        
        try:
            entry_year_int = int(entry_year_str)
            if entry_year_int >= 92:
                entry_year = 1300 + entry_year_int
            else:
                entry_year = 1400 + entry_year_int
        except (ValueError, IndexError):
            return Response(
                {"error": "خطا در تجزیه شماره دانشجویی"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        major_mapping = {
            '210': 'CS', '213': 'EE', '201': 'CE', '211': 'ME', '220': 'SE',
        }
        major = major_mapping.get(major_code_str)
        
        if not major:
            return Response(
                {"error": f"رشته {major_code_str} شناخته شده نیست"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        chart = ChartSchema.objects.filter(
            major=major,
            entry_year_start__lte=entry_year,
            entry_year_end__gte=entry_year
        ).first()
        
        if not chart:
            return Response(
                {"error": "چارت یافت نشد"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Next semester (calculate from passed courses in StudentCourseHistory)
        completed_semesters = StudentCourseHistory.objects.filter(
            student=user
        ).values('semester').distinct().count()
        next_semester = (completed_semesters or 0) + 1
        
        if next_semester > 8:
            return Response({
                "next_semester": next_semester,
                "recommendations": [],
                "message": "دانشجو تمام ترم‌ها را تکمیل کرده است"
            })
        
        # Get courses in next semester
        nodes = ChartNode.objects.filter(
            schema=chart,
            semester=next_semester
        ).select_related('course', 'course_group')
        
        recommendations = []
        
        for node in nodes:
            if node.course:
                course = node.course
                is_elective = False
            else:
                # For elective slots, pick the best elective
                if not node.course_group:
                    continue
                course = node.course_group.courses.first()
                is_elective = True
            
            if not course:
                continue
            
            # Check if already passed
            if course.id in passed_courses:
                continue
            
            # Calculate priority score
            score = calculate_priority_score(
                course=course,
                passed_courses=passed_courses,
                target_semester=next_semester,
                chart=chart
            )
            
            # Get unlocked courses (courses that have this as prerequisite)
            unlocked = list(
                CourseRequirement.objects.filter(
                    prerequisite=course
                ).values_list('course_id', flat=True)
            )
            
            recommendations.append({
                'course_id': course.id,
                'code': course.code,
                'name': course.name,
                'credits': course.credits,
                'priority_score': score['total'],
                'reason': score['reason'],
                'unlocks': unlocked,
                'prerequisites_met': score['prerequisites_met'],
                'is_mandatory': not is_elective,
                'is_elective': is_elective,
            })
        
        # Sort by priority score (descending)
        recommendations.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return Response({
            'next_semester': next_semester,
            'recommendations': recommendations
        })


def calculate_priority_score(course, passed_courses, target_semester, chart):
    """
    Calculate priority score for a course.
    
    Score = Base_Weight + Dependency_Weight + Semester_Alignment
    
    Base_Weight = 50 (all courses have base importance)
    Dependency_Weight = (number of courses that require this) × 10
    Semester_Alignment = (course is in target semester?) ? 25 : 0
    
    If prerequisites not met: Score = 0 (blocked)
    """
    
    # Check prerequisites
    prerequisites = CourseRequirement.objects.filter(course=course)
    prerequisites_met = True
    
    for req in prerequisites:
        if req.prerequisite_id not in passed_courses:
            prerequisites_met = False
            break
    
    if not prerequisites_met:
        return {
            'total': 0,
            'prerequisites_met': False,
            'reason': 'پیشنیازهای درس تکمیل نشده است'
        }
    
    # Base weight
    base_weight = 50
    
    # Dependency weight: courses that need this course as prerequisite
    dependent_count = CourseRequirement.objects.filter(
        prerequisite=course
    ).count()
    dependency_weight = dependent_count * 10
    
    # Semester alignment: is this course in the target semester?
    is_in_target_sem = ChartNode.objects.filter(
        schema=chart,
        course=course,
        semester=target_semester
    ).exists()
    semester_weight = 25 if is_in_target_sem else 0
    
    # Bonus for elective importance
    elective_bonus = 0
    if course.is_elective:
        elective_bonus = 10
    
    total_score = base_weight + dependency_weight + semester_weight + elective_bonus
    
    # Cap at 100
    total_score = min(total_score, 100)
    
    reason_parts = []
    if dependent_count > 0:
        reason_parts.append(f'پیشنیاز برای {dependent_count} درس')
    if is_in_target_sem:
        reason_parts.append('درس مقرر این ترم')
    
    reason = ' | '.join(reason_parts) if reason_parts else 'درس مهم'
    
    return {
        'total': total_score,
        'prerequisites_met': True,
        'reason': reason,
        'base': base_weight,
        'dependency': dependency_weight,
        'semester': semester_weight,
        'elective_bonus': elective_bonus,
    }
