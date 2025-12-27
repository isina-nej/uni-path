from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import DegreeChart, Course, ChartCourse, Prerequisite, CoRequisite
from .serializers import (
    DegreeChartSerializer,
    DegreeChartDetailSerializer,
    CourseSerializer,
    CourseDetailSerializer,
    ChartCourseSerializer,
    PrerequisiteSerializer,
    CoRequisiteSerializer,
)
from accounts.permissions import IsAdmin, IsAdminOrHOD, IsAdminOrReadOnly, IsStudent
from .recommendations import RecommendationEngine


class DegreeChartViewSet(viewsets.ModelViewSet):
    """
    ViewSet for DegreeChart (Major programs).
    
    GET    /api/courses/charts/           - List all charts
    POST   /api/courses/charts/           - Create chart (admin/HOD)
    GET    /api/courses/charts/{id}/      - Chart details with all courses
    PUT    /api/courses/charts/{id}/      - Update chart (admin/HOD)
    DELETE /api/courses/charts/{id}/      - Delete chart (admin)
    """
    
    queryset = DegreeChart.objects.all()
    serializer_class = DegreeChartSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department']
    search_fields = ['name', 'code', 'department']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        """Use detailed serializer for retrieve action."""
        if self.action == 'retrieve':
            return DegreeChartDetailSerializer
        return DegreeChartSerializer
    
    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        """
        Get all courses for a specific degree chart.
        GET /api/courses/charts/{id}/courses/
        """
        chart = self.get_object()
        chart_courses = ChartCourse.objects.filter(degree_chart=chart).select_related('course')
        serializer = ChartCourseSerializer(chart_courses, many=True)
        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Course management.
    
    GET    /api/courses/list/             - List all courses
    POST   /api/courses/list/             - Create course (admin)
    GET    /api/courses/list/{id}/        - Course details with prerequisites
    PUT    /api/courses/list/{id}/        - Update course (admin)
    DELETE /api/courses/list/{id}/        - Delete course (admin)
    
    FR-12: HOD must be able to modify the prerequisite structure for their specific department.
    """
    
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_offered', 'is_mandatory', 'unit_type', 'semester']
    search_fields = ['name', 'code', 'instructor', 'description']
    ordering_fields = ['code', 'name', 'credits', 'semester', 'created_at']
    ordering = ['code']
    
    def get_serializer_class(self):
        """Use detailed serializer for retrieve action."""
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer
    
    @action(detail=True, methods=['get'])
    def prerequisites(self, request, pk=None):
        """
        Get all prerequisites for a specific course.
        GET /api/courses/list/{id}/prerequisites/
        """
        course = self.get_object()
        prerequisites = Prerequisite.objects.filter(course=course)
        serializer = PrerequisiteSerializer(prerequisites, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def corequisites(self, request, pk=None):
        """
        Get all co-requisites for a specific course.
        GET /api/courses/list/{id}/corequisites/
        """
        course = self.get_object()
        corequisites = CoRequisite.objects.filter(course=course)
        serializer = CoRequisiteSerializer(corequisites, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put', 'patch'])
    def update_prerequisites(self, request, pk=None):
        """
        FR-12: Update prerequisites for a course (HOD only).
        
        PUT /api/courses/list/{id}/update_prerequisites/
        {
            "prerequisites": [1, 2, 3],
            "corequisites": [4, 5]
        }
        """
        # Check HOD permission
        if request.user.role not in ['hod', 'admin']:
            return Response(
                {'error': 'فقط سرپرستان دپارتمان می‌توانند این کار را انجام دهند'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        course = self.get_object()
        prerequisites_ids = request.data.get('prerequisites', [])
        corequisites_ids = request.data.get('corequisites', [])
        
        try:
            # Delete existing prerequisites and corequisites
            Prerequisite.objects.filter(course=course).delete()
            CoRequisite.objects.filter(course=course).delete()
            
            # Add new prerequisites
            for prereq_id in prerequisites_ids:
                prereq_course = Course.objects.get(id=prereq_id)
                
                # Check for circular dependency
                if self._has_circular_dependency(course, prereq_course):
                    return Response(
                        {'error': f'وابستگی دایره‌ای تشخیص داده شد با درس {prereq_course.code}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                Prerequisite.objects.create(
                    course=course,
                    prerequisite_course=prereq_course,
                    is_corequisite=False
                )
            
            # Add new corequisites
            for coreq_id in corequisites_ids:
                coreq_course = Course.objects.get(id=coreq_id)
                CoRequisite.objects.create(
                    course=course,
                    corequisite_course=coreq_course
                )
            
            # Return updated prerequisites
            prerequisites = Prerequisite.objects.filter(course=course)
            corequisites = CoRequisite.objects.filter(course=course)
            
            return Response({
                'course_id': course.id,
                'course_code': course.code,
                'prerequisites': PrerequisiteSerializer(prerequisites, many=True).data,
                'corequisites': CoRequisiteSerializer(corequisites, many=True).data,
                'message': 'پیش‌نیازها با موفقیت بروزرسانی شدند',
            }, status=status.HTTP_200_OK)
        
        except Course.DoesNotExist:
            return Response(
                {'error': 'یکی از دروس پیدا نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def _has_circular_dependency(self, course, new_prereq):
        """
        Check if adding new_prereq as a prerequisite for course would create a circular dependency.
        """
        visited = set()
        
        def dfs(current):
            if current.id in visited:
                return False
            if current.id == course.id:
                return True
            visited.add(current.id)
            
            dependents = Prerequisite.objects.filter(
                prerequisite_course=current,
                is_corequisite=False
            ).values_list('course_id', flat=True)
            
            for dependent_id in dependents:
                dependent = Course.objects.get(id=dependent_id)
                if dfs(dependent):
                    return True
            
            return False
        
    
    def _has_circular_dependency(self, course, new_prereq):
        """
        Check if adding new_prereq as a prerequisite for course would create a circular dependency.
        """
        visited = set()
        
        def dfs(current):
            if current.id in visited:
                return False
            if current.id == course.id:
                return True
            visited.add(current.id)
            
            dependents = Prerequisite.objects.filter(
                prerequisite_course=current,
                is_corequisite=False
            ).values_list('course_id', flat=True)
            
            for dependent_id in dependents:
                dependent = Course.objects.get(id=dependent_id)
                if dfs(dependent):
                    return True
            
            return False
        
        return dfs(new_prereq)


class PrerequisiteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Prerequisite management.
    
    GET    /api/courses/prerequisites/     - List prerequisites
    POST   /api/courses/prerequisites/     - Create prerequisite (admin)
    """
    
    queryset = Prerequisite.objects.all()
    serializer_class = PrerequisiteSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'prerequisite_course', 'is_corequisite']
    
    def create(self, request, *args, **kwargs):
        """
        Create a new prerequisite relationship.
        Validates that a course cannot be a prerequisite for itself.
        """
        serializer = self.get_serializer(data=request.data)
        

        if serializer.is_valid():
            course = serializer.validated_data['course']
            prerequisite = serializer.validated_data['prerequisite_course']
            
            if course == prerequisite:
                return Response(
                    {'error': 'یک درس نمی‌تواند پیش‌نیاز خود باشد'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoRequisiteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CoRequisite management.
    
    GET    /api/courses/corequisites/     - List co-requisites
    POST   /api/courses/corequisites/     - Create co-requisite (admin)
    """
    
    queryset = CoRequisite.objects.all()
    serializer_class = CoRequisiteSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'corequisite_course']
    
    def create(self, request, *args, **kwargs):
        """
        Create a new co-requisite relationship.
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            course = serializer.validated_data['course']
            corequisite = serializer.validated_data['corequisite_course']
            
            if course == corequisite:
                return Response(
                    {'error': 'یک درس نمی‌تواند هم‌نیاز خود باشد'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendationViewSet(viewsets.ViewSet):
    """
    ViewSet for course recommendations.
    
    POST   /api/courses/recommendations/   - Get recommendations for student
    """
    
    permission_classes = [IsAuthenticated, IsStudent]
    
    @action(detail=False, methods=['post'])
    def recommend(self, request):
        """
        Get course recommendations for the student.
        
        POST /api/courses/recommendations/recommend/
        {
            "degree_chart_id": 1,
            "semester": "Spring 1403",
            "limit": 10
        }
        
        Returns:
            {
                "success": true,
                "semester": "Spring 1403",
                "recommendations": [
                    {
                        "id": 1,
                        "code": "CS101",
                        "name": "مقدمه برنامه‌نویسی",
                        "credits": 3,
                        "unit_type": "theoretical",
                        "instructor": "دکتر احمدی",
                        "importance_score": 5,
                        "description": "...",
                        "start_time": "08:00:00",
                        "end_time": "09:30:00"
                    }
                ]
            }
        """
        
        # تأیید اینکه کاربر دانشجو است
        if request.user.role != 'student':
            return Response(
                {'error': 'فقط دانشجویان می‌توانند توصیه‌ها دریافت کنند'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # دریافت پارامترهای ورودی
        degree_chart_id = request.data.get('degree_chart_id')
        semester = request.data.get('semester', 'Spring 1403')
        limit = int(request.data.get('limit', 10))
        
        # اعتبارسنجی
        if not degree_chart_id:
            return Response(
                {'error': 'degree_chart_id الزامی است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # دریافت نمودار درجات
        degree_chart = get_object_or_404(DegreeChart, id=degree_chart_id)
        
        try:
            # ایجاد موتور توصیه‌ها
            engine = RecommendationEngine(request.user, degree_chart)
            
            # دریافت توصیه‌ها
            recommendations = engine.get_recommendations(semester, limit)
            
            return Response({
                'success': True,
                'semester': semester,
                'degree_chart': {
                    'id': degree_chart.id,
                    'name': degree_chart.name,
                    'code': degree_chart.code,
                },
                'total_recommendations': len(recommendations),
                'recommendations': recommendations,
            })
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def help(self, request):
        """
        لیست پیامهای API توصیه‌ها
        GET /api/courses/recommendations/help/
        """
        return Response({
            'endpoints': {
                'recommend': {
                    'method': 'POST',
                    'path': '/api/courses/recommendations/recommend/',
                    'description': 'دریافت توصیه‌های دروس برای دانشجو',
                    'required_fields': ['degree_chart_id'],
                    'optional_fields': ['semester', 'limit'],
                }
            }
        })
