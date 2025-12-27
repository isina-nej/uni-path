from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentCourseHistoryViewSet, StudentSelectionViewSet, ScheduleViewSet

app_name = 'students'

router = DefaultRouter()
router.register(r'history', StudentCourseHistoryViewSet, basename='history')
router.register(r'selections', StudentSelectionViewSet, basename='selections')
router.register(r'schedule', ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('', include(router.urls)),
]
