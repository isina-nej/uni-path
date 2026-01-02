from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model with profile data.
    """
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active')
        read_only_fields = ('id',)


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model.
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ('id', 'user', 'student_number', 'phone', 'bio', 'avatar', 'major', 'department')
        read_only_fields = ('id',)


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name', 'role')
    
    def validate_email(self, value):
        """
        Validate that email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('این ایمیل قبلاً استفاده شده است')
        return value
    
    def validate(self, data):
        """
        Validate that passwords match.
        """
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({
                'password': 'رمز عبور و تکرار آن یکسان نیستند'
            })
        return data
    
    def create(self, validated_data):
        """
        Create user with hashed password.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'student')
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer with additional user information.
    Accepts both 'username' and 'email' as login identifier.
    """
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        
        return token
    
    def validate(self, attrs):
        """
        Validate credentials and return user info along with token.
        Converts email input to username automatically.
        """
        # If 'username' field contains an email, try to find user by email first
        username_input = attrs.get('username', '')
        if '@' in username_input:
            try:
                user = User.objects.get(email=username_input)
                attrs['username'] = user.username
            except User.DoesNotExist:
                pass  # Fall back to normal validation
        
        data = super().validate(attrs)
        
        # Add user information to response
        user = self.user
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change.
    """
    
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    
    new_password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, data):
        """
        Validate that new passwords match.
        """
        if data['new_password'] != data.pop('new_password2'):
            raise serializers.ValidationError({
                'new_password': 'رمزهای عبور جدید یکسان نیستند'
            })
        return data
    
    def validate_old_password(self, value):
        """
        Validate that old password is correct.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('رمز عبور قدیمی اشتباه است')
        return value
    
    def save(self):
        """
        Change user password.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    """
    
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'student_number', 'phone', 'bio', 'avatar', 'major')
    
    def update(self, instance, validated_data):
        """
        Update profile and user information.
        """
        # Update user fields
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        
        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance
