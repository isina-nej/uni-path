"""
Grade management for Professors

FR-11: Professors must be able to input/upload grades for students enrolled in their specific courses.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from students.models import StudentCourseHistory
from students.serializers import StudentCourseHistorySerializer
from courses.models import Course
from accounts.permissions import IsProfessor

User = get_user_model()


class GradeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for grade management by professors.
    
    FR-11: Professors must be able to input/upload grades for students 
    enrolled in their specific courses.
    
    GET    /api/grades/                  - List grades (professor's courses)
    POST   /api/grades/                  - Submit a grade
    GET    /api/grades/my-courses/       - List courses taught by professor
    GET    /api/grades/{student_id}/     - Get student grades in professor's courses
    """
    
    serializer_class = StudentCourseHistorySerializer
    permission_classes = [IsAuthenticated, IsProfessor]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course', 'semester']
    search_fields = ['student__username', 'student__email', 'course__code', 'course__name']
    ordering_fields = ['semester', 'student__username']
    ordering = ['-semester']
    
    def get_queryset(self):
        """
        Professors can only see grades for courses they teach.
        """
        user = self.request.user
        
        if user.role != 'professor':
            return StudentCourseHistory.objects.none()
        
        # Get courses taught by this professor
        courses = Course.objects.filter(instructor=user.get_full_name())
        
        return StudentCourseHistory.objects.filter(course__in=courses)
    
    def create(self, request, *args, **kwargs):
        """
        Submit a grade for a student in a course.
        
        POST /api/grades/
        {
            "student_id": 1,
            "course_id": 1,
            "grade": "B+",
            "semester": "Fall 1402"
        }
        
        FR-11: Professor-only endpoint
        """
        if request.user.role != 'professor':
            return Response(
                {'error': 'فقط اساتید می‌توانند نمرات را وارد کنند'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        student_id = request.data.get('student_id')
        course_id = request.data.get('course_id')
        grade = request.data.get('grade')
        semester = request.data.get('semester', 'Fall 1402')
        
        # Validation
        if not all([student_id, course_id, grade]):
            return Response(
                {'error': 'student_id, course_id, and grade are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            student = User.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)
            
            # Verify professor teaches this course
            if course.instructor != request.user.get_full_name():
                return Response(
                    {'error': 'شما این درس را تدریس نمی‌کنید'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Grade point mapping
            grade_points_map = {
                'A': 4.0,
                'A-': 3.7,
                'B+': 3.3,
                'B': 3.0,
                'B-': 2.7,
                'C+': 2.3,
                'C': 2.0,
                'C-': 1.7,
                'D+': 1.3,
                'D': 1.0,
                'F': 0.0,
            }
            
            grade_points = grade_points_map.get(grade, 0.0)
            is_passed = grade != 'F'
            
            # Create or update history
            history, created = StudentCourseHistory.objects.get_or_create(
                student=student,
                course=course,
                semester=semester,
                defaults={
                    'grade': grade,
                    'grade_points': grade_points,
                    'credits_earned': course.credits if is_passed else 0,
                    'is_passed': is_passed,
                }
            )
            
            if not created:
                history.grade = grade
                history.grade_points = grade_points
                history.credits_earned = course.credits if is_passed else 0
                history.is_passed = is_passed
                history.save()
            
            serializer = StudentCourseHistorySerializer(history)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except User.DoesNotExist:
            return Response(
                {'error': 'دانشجو پیدا نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Course.DoesNotExist:
            return Response(
                {'error': 'درس پیدا نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def my_courses(self, request):
        """
        Get list of courses taught by this professor.
        GET /api/grades/my_courses/
        """
        if request.user.role != 'professor':
            return Response(
                {'error': 'فقط اساتید می‌توانند اطلاعات خود را ببینند'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        courses = Course.objects.filter(instructor=request.user.get_full_name())
        
        course_data = []
        for course in courses:
            students = StudentCourseHistory.objects.filter(course=course).values_list(
                'student__id',
                'student__username',
                'student__email',
                'grade',
                'semester'
            )
            
            course_data.append({
                'id': course.id,
                'code': course.code,
                'name': course.name,
                'credits': course.credits,
                'students_count': len(students),
                'students': [
                    {
                        'id': s[0],
                        'username': s[1],
                        'email': s[2],
                        'grade': s[3],
                        'semester': s[4],
                    }
                    for s in students
                ]
            })
        
        return Response({
            'count': len(course_data),
            'courses': course_data
        })
    
    @action(detail=False, methods=['get'])
    def course_students(self, request):
        """
        Get students in a specific course.
        GET /api/grades/course_students/?course_id=1
        """
        if request.user.role != 'professor':
            return Response(
                {'error': 'فقط اساتید می‌توانند اطلاعات خود را ببینند'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        course_id = request.query_params.get('course_id')
        semester = request.query_params.get('semester', 'Fall 1402')
        
        if not course_id:
            return Response(
                {'error': 'course_id الزامی است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            course = Course.objects.get(id=course_id)
            
            # Verify professor teaches this course
            if course.instructor != request.user.get_full_name():
                return Response(
                    {'error': 'شما این درس را تدریس نمی‌کنید'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Get students enrolled in this course
            students_data = StudentCourseHistory.objects.filter(
                course=course,
                semester=semester
            ).select_related('student')
            
            return Response({
                'course_id': course.id,
                'course_code': course.code,
                'course_name': course.name,
                'semester': semester,
                'students': StudentCourseHistorySerializer(
                    students_data,
                    many=True
                ).data
            })
        
        except Course.DoesNotExist:
            return Response(
                {'error': 'درس پیدا نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
