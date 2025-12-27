from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from .models import StudentCourseHistory, StudentSelection, Schedule
from .serializers import StudentCourseHistorySerializer, StudentSelectionSerializer, ScheduleSerializer
from accounts.permissions import IsStudent, IsAdminOrReadOnly

User = get_user_model()


class StudentCourseHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for student course history.
    
    GET    /api/students/history/        - Get own course history
    POST   /api/students/history/        - Add course to history (admin)
    PUT    /api/students/history/{id}/   - Update history entry (admin)
    """
    
    serializer_class = StudentCourseHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'semester', 'is_passed']
    search_fields = ['course__code', 'course__name']
    ordering_fields = ['semester', 'created_at']
    ordering = ['-semester']
    
    def get_queryset(self):
        """
        Students see only their own history.
        Admins see all history.
        """
        user = self.request.user
        
        if user.role == 'admin':
            return StudentCourseHistory.objects.all()
        
        return StudentCourseHistory.objects.filter(student=user)
    
    def create(self, request, *args, **kwargs):
        """
        Create course history entry (admin only).
        """
        if request.user.role != 'admin':
            return Response(
                {'error': 'فقط مدیران می‌توانند این کار را انجام دهند'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def passed_courses(self, request):
        """
        Get all passed courses for current student.
        GET /api/students/history/passed_courses/
        """
        if request.user.role != 'student':
            return Response(
                {'error': 'فقط دانشجویان می‌توانند اطلاعات خود را ببینند'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        passed = StudentCourseHistory.objects.filter(
            student=request.user,
            is_passed=True
        )
        serializer = StudentCourseHistorySerializer(passed, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get student statistics.
        GET /api/students/history/statistics/
        """
        if request.user.role != 'student':
            return Response(
                {'error': 'فقط دانشجویان می‌توانند اطلاعات خود را ببینند'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        history = StudentCourseHistory.objects.filter(student=request.user)
        
        total_courses = history.count()
        passed_courses = history.filter(is_passed=True).count()
        failed_courses = history.filter(is_passed=False).count()
        total_credits = sum(h.credits_earned for h in history)
        gpa = sum(h.grade_points for h in history) / total_courses if total_courses > 0 else 0
        
        return Response({
            'total_courses': total_courses,
            'passed_courses': passed_courses,
            'failed_courses': failed_courses,
            'total_credits': total_credits,
            'gpa': round(gpa, 2),
        })
    
    @action(detail=False, methods=['post'])
    def mark_passed(self, request):
        """
        Mark a course as passed with grade.
        FR-7: Students must be able to toggle the status of a course to "Passed"
        
        POST /api/students/history/mark_passed/
        {
            "course_id": 1,
            "semester": "Fall 1402",
            "grade": "A",
            "grade_points": 4.0
        }
        """
        if request.user.role != 'student':
            return Response(
                {'error': 'فقط دانشجویان می‌توانند دروس را تأیید کنند'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        course_id = request.data.get('course_id')
        semester = request.data.get('semester', 'Fall 1402')
        grade = request.data.get('grade', 'A')
        grade_points = request.data.get('grade_points', 4.0)
        
        if not course_id:
            return Response(
                {'error': 'course_id الزامی است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from courses.models import Course
            course = Course.objects.get(id=course_id)
            
            # Create or update history
            history, created = StudentCourseHistory.objects.get_or_create(
                student=request.user,
                course=course,
                semester=semester,
                defaults={
                    'grade': grade,
                    'grade_points': grade_points,
                    'credits_earned': course.credits,
                    'is_passed': True,
                }
            )
            
            if not created:
                history.grade = grade
                history.grade_points = grade_points
                history.credits_earned = course.credits
                history.is_passed = True
                history.save()
            
            serializer = StudentCourseHistorySerializer(history)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'])
    def mark_failed(self, request):
        """
        Mark a course as failed.
        
        POST /api/students/history/mark_failed/
        {
            "course_id": 1,
            "semester": "Fall 1402",
            "grade": "F",
            "grade_points": 0.0
        }
        """
        if request.user.role != 'student':
            return Response(
                {'error': 'فقط دانشجویان می‌توانند دروس را تأیید کنند'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        course_id = request.data.get('course_id')
        semester = request.data.get('semester', 'Fall 1402')
        
        if not course_id:
            return Response(
                {'error': 'course_id الزامی است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from courses.models import Course
            course = Course.objects.get(id=course_id)
            
            history, created = StudentCourseHistory.objects.get_or_create(
                student=request.user,
                course=course,
                semester=semester,
                defaults={
                    'grade': 'F',
                    'grade_points': 0.0,
                    'credits_earned': 0,
                    'is_passed': False,
                }
            )
            
            if not created:
                history.grade = 'F'
                history.grade_points = 0.0
                history.credits_earned = 0
                history.is_passed = False
                history.save()
            
            serializer = StudentCourseHistorySerializer(history)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class StudentSelectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for student course selection.
    
    GET    /api/students/selections/      - Get own selections
    POST   /api/students/selections/      - Select a course
    DELETE /api/students/selections/{id}/ - Remove selection
    """
    
    serializer_class = StudentSelectionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['semester', 'is_confirmed']
    ordering_fields = ['selected_at', 'semester']
    ordering = ['-selected_at']
    
    def get_queryset(self):
        """
        Students see only their own selections.
        """
        user = self.request.user
        
        if user.role == 'admin':
            return StudentSelection.objects.all()
        
        return StudentSelection.objects.filter(student=user)
    
    def create(self, request, *args, **kwargs):
        """
        Select a course for upcoming semester.
        """
        if request.user.role != 'student':
            return Response(
                {'error': 'فقط دانشجویان می‌توانند دروس را انتخاب کنند'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Add student to request data
        request.data['student'] = request.user.id
        
        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['post'])
    def confirm_selections(self, request):
        """
        Confirm all selections for a semester.
        POST /api/students/selections/confirm_selections/
        {
            "semester": "Spring 1403"
        }
        """
        if request.user.role != 'student':
            return Response(
                {'error': 'فقط دانشجویان می‌توانند دروس را تأیید کنند'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        semester = request.data.get('semester')
        if not semester:
            return Response(
                {'error': 'semester الزامی است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        selections = StudentSelection.objects.filter(
            student=request.user,
            semester=semester
        )
        
        from django.utils import timezone
        selections.update(is_confirmed=True, confirmed_at=timezone.now())
        
        serializer = StudentSelectionSerializer(selections, many=True)
        return Response({
            'message': f'{selections.count()} درس تأیید شد',
            'selections': serializer.data
        })


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for student schedule.
    
    GET    /api/students/schedule/       - Get own schedule
    POST   /api/students/schedule/       - Create schedule entry
    """
    
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['semester', 'day_of_week']
    ordering_fields = ['day_of_week', 'start_time']
    ordering = ['day_of_week', 'start_time']
    
    def get_queryset(self):
        """
        Students see only their own schedule.
        """
        user = self.request.user
        
        if user.role == 'admin':
            return Schedule.objects.all()
        
        return Schedule.objects.filter(student=user)
    
    def create(self, request, *args, **kwargs):
        """
        Create schedule entry.
        """
        if request.user.role != 'student':
            return Response(
                {'error': 'فقط دانشجویان می‌توانند برنامه درسی ایجاد کنند'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        request.data['student'] = request.user.id
        
        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def conflicts(self, request):
        """
        Get all schedule conflicts for current student.
        GET /api/students/schedule/conflicts/
        """
        if request.user.role != 'student':
            return Response(
                {'error': 'فقط دانشجویان می‌توانند برنامه خود را ببینند'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        semester = request.query_params.get('semester')
        
        schedules = Schedule.objects.filter(student=request.user)
        if semester:
            schedules = schedules.filter(semester=semester)
        
        conflicts = []
        for schedule in schedules:
            if schedule.has_conflict:
                conflicts.append(ScheduleSerializer(schedule).data)
        
        return Response({
            'total_conflicts': len(conflicts),
            'conflicts': conflicts
        })
