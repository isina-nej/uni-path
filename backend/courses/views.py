from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

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
from accounts.permissions import IsAdmin, IsAdminOrHOD, IsAdminOrReadOnly


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
