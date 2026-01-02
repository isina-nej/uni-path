from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views_chart import DegreeChartViewSet

# Create router
router = DefaultRouter()
router.register(r'charts', views.DegreeChartViewSet, basename='chart')
router.register(r'degrees', DegreeChartViewSet, basename='degree-chart')
router.register(r'list', views.CourseViewSet, basename='course')
router.register(r'prerequisites', views.PrerequisiteViewSet, basename='prerequisite')
router.register(r'corequisites', views.CoRequisiteViewSet, basename='corequisite')
router.register(r'recommendations', views.RecommendationViewSet, basename='recommendation')

app_name = 'courses'

urlpatterns = [
    path('', include(router.urls)),
]
