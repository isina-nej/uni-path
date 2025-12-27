from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model

from .serializers import (
    UserSerializer,
    ProfileSerializer,
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    UpdateProfileSerializer,
)
from .models import Profile
from .permissions import IsOwnerOrAdmin

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain view with additional user information.
    """
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    User registration endpoint.
    
    POST /api/auth/register
    {
        "username": "student1",
        "email": "student1@example.com",
        "password": "SecurePass123!",
        "password2": "SecurePass123!",
        "first_name": "علی",
        "last_name": "احمدی",
        "role": "student"
    }
    """
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        # Create profile automatically via signal
        
        return Response({
            'message': 'کاربر با موفقیت ثبت نام شد',
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout endpoint (token blacklisting is handled by JWT settings).
    
    POST /api/auth/logout
    """
    return Response({
        'message': 'با موفقیت خارج شدید'
    }, status=status.HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user profile management.
    
    GET    /api/user/profile/       - Get current user's profile
    PUT    /api/user/profile/       - Update current user's profile
    PATCH  /api/user/profile/       - Partial update
    """
    
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def get_queryset(self):
        """
        Return only the current user's profile.
        """
        if self.request.user.is_authenticated:
            return Profile.objects.filter(user=self.request.user)
        return Profile.objects.none()
    
    def get_object(self):
        """
        Return the current user's profile.
        """
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        self.check_object_permissions(self.request, profile)
        return profile
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get current user's profile.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """
        Update current user's profile.
        """
        instance = self.get_object()
        serializer = UpdateProfileSerializer(
            instance,
            data=request.data,
            partial=kwargs.get('partial', False),
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            ProfileSerializer(instance).data,
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    Change password endpoint.
    
    POST /api/user/change-password/
    {
        "old_password": "CurrentPass123!",
        "new_password": "NewPass123!",
        "new_password2": "NewPass123!"
    }
    """
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'رمز عبور با موفقیت تغییر کرد'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

