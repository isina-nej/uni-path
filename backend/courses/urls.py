from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Create router
router = DefaultRouter()
router.register(r'charts', views.DegreeChartViewSet, basename='chart')
router.register(r'list', views.CourseViewSet, basename='course')
router.register(r'prerequisites', views.PrerequisiteViewSet, basename='prerequisite')
router.register(r'corequisites', views.CoRequisiteViewSet, basename='corequisite')

app_name = 'courses'

urlpatterns = [
    path('', include(router.urls)),
]
