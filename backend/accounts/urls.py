from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views_grades import GradeViewSet

# Create router
router = DefaultRouter()
router.register(r'profile', views.UserProfileViewSet, basename='profile')
router.register(r'grades', GradeViewSet, basename='grades')

app_name = 'accounts'

urlpatterns = [
    # JWT Tokens
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),
    
    # Profile routes
    path('', include(router.urls)),
]
