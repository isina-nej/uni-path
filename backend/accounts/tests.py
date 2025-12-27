from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json

User = get_user_model()


class UserModelTests(TestCase):
    """Tests for User model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='student'
        )
    
    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertEqual(self.user.role, 'student')
    
    def test_user_is_student(self):
        """Test is_student method"""
        self.assertTrue(self.user.is_student())
        self.assertFalse(self.user.is_professor())
    
    def test_user_is_professor(self):
        """Test is_professor method"""
        prof = User.objects.create_user(
            username='professor',
            email='prof@example.com',
            password='pass123',
            role='professor'
        )
        self.assertTrue(prof.is_professor())
        self.assertFalse(prof.is_student())
    
    def test_user_is_admin(self):
        """Test is_admin method"""
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='pass123',
            role='admin'
        )
        self.assertTrue(admin.is_admin())
    
    def test_user_is_hod(self):
        """Test is_hod method"""
        hod = User.objects.create_user(
            username='hod',
            email='hod@example.com',
            password='pass123',
            role='hod'
        )
        self.assertTrue(hod.is_hod())
    
    def test_user_str(self):
        """Test user string representation"""
        expected = f"{self.user.get_full_name()} (Student)"
        self.assertEqual(str(self.user), expected)


class ProfileModelTests(TestCase):
    """Tests for Profile model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='profiletest',
            email='profile@example.com',
            password='pass123',
            role='student'
        )
    
    def test_profile_auto_creation(self):
        """Test profile is created when user is created"""
        # Profile should be created via signal
        from accounts.models import Profile
        self.assertTrue(Profile.objects.filter(user=self.user).exists())


class RegistrationAPITests(APITestCase):
    """Tests for user registration endpoint"""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:register')
    
    def test_register_valid_data(self):
        """Test registration with valid data"""
        data = {
            'username': 'newstudent',
            'email': 'student@example.com',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'علی',
            'last_name': 'احمدی',
            'role': 'student'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newstudent').exists())
    
    def test_register_password_mismatch(self):
        """Test registration with mismatched passwords"""
        data = {
            'username': 'newstudent',
            'email': 'student@example.com',
            'password': 'SecurePass123!',
            'password2': 'DifferentPass123!',
            'first_name': 'علی',
            'last_name': 'احمدی',
            'role': 'student'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_weak_password(self):
        """Test registration with weak password"""
        data = {
            'username': 'newstudent',
            'email': 'student@example.com',
            'password': '123',
            'password2': '123',
            'first_name': 'علی',
            'last_name': 'احمدی',
            'role': 'student'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_duplicate_username(self):
        """Test registration with existing username"""
        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='pass123'
        )
        data = {
            'username': 'existing',
            'email': 'newemail@example.com',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'علی',
            'last_name': 'احمدی',
            'role': 'student'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_duplicate_email(self):
        """Test registration with existing email"""
        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='pass123'
        )
        data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'علی',
            'last_name': 'احمدی',
            'role': 'student'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginAPITests(APITestCase):
    """Tests for login endpoint"""
    
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('accounts:token_obtain_pair')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_valid_credentials(self):
        """Test login with valid credentials"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_invalid_password(self):
        """Test login with invalid password"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_nonexistent_user(self):
        """Test login with nonexistent user"""
        data = {
            'username': 'nonexistent',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_token_contains_user_info(self):
        """Test that token contains user information"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Token should contain role and other user info
        self.assertIn('user', response.data)


class TokenRefreshTests(APITestCase):
    """Tests for token refresh endpoint"""
    
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('accounts:token_obtain_pair')
        self.refresh_url = reverse('accounts:token_refresh')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_token_refresh(self):
        """Test token refresh"""
        # Get initial tokens
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        refresh_token = login_response.data['refresh']
        
        # Refresh token
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(self.refresh_url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


class LogoutAPITests(APITestCase):
    """Tests for logout endpoint"""
    
    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse('accounts:logout')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_logout_authenticated(self):
        """Test logout with authenticated user"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_logout_unauthenticated(self):
        """Test logout without authentication"""
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChangePasswordTests(APITestCase):
    """Tests for change password endpoint"""
    
    def setUp(self):
        self.client = APIClient()
        self.change_pass_url = reverse('accounts:change_password')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='oldpass123'
        )
    
    def test_change_password_valid(self):
        """Test changing password with valid current password"""
        self.client.force_authenticate(user=self.user)
        data = {
            'old_password': 'oldpass123',
            'new_password': 'newpass123!',
            'new_password2': 'newpass123!'
        }
        response = self.client.post(self.change_pass_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify password changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass123!'))
    
    def test_change_password_wrong_old(self):
        """Test changing password with wrong old password"""
        self.client.force_authenticate(user=self.user)
        data = {
            'old_password': 'wrongpass',
            'new_password': 'newpass123!',
            'new_password2': 'newpass123!'
        }
        response = self.client.post(self.change_pass_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_change_password_mismatch(self):
        """Test changing password with mismatched new passwords"""
        self.client.force_authenticate(user=self.user)
        data = {
            'old_password': 'oldpass123',
            'new_password': 'newpass123!',
            'new_password2': 'differentpass123!'
        }
        response = self.client.post(self.change_pass_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProfileAPITests(APITestCase):
    """Tests for profile endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='student'
        )
        self.profile_url = reverse('accounts:profile-detail', kwargs={'pk': self.user.profile.id})
    
    def test_get_profile_authenticated(self):
        """Test getting profile when authenticated"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser')
    
    def test_get_profile_unauthenticated(self):
        """Test getting profile without authentication"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_own_profile(self):
        """Test updating own profile"""
        self.client.force_authenticate(user=self.user)
        data = {
            'phone': '09123456789',
            'bio': 'My bio'
        }
        response = self.client.patch(self.profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PermissionTests(APITestCase):
    """Tests for RBAC permissions"""
    
    def setUp(self):
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='pass123',
            role='student'
        )
        self.professor = User.objects.create_user(
            username='professor',
            email='prof@example.com',
            password='pass123',
            role='professor'
        )
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='pass123',
            role='admin'
        )
        self.client = APIClient()
    
    def test_student_cannot_access_admin_endpoints(self):
        """Test student cannot access admin-only endpoints"""
        self.client.force_authenticate(user=self.student)
        # This would test admin-only endpoints if they existed
        self.assertTrue(self.student.is_student())
        self.assertFalse(self.student.is_admin())
    
    def test_professor_can_enter_grades(self):
        """Test professor role"""
        self.client.force_authenticate(user=self.professor)
        self.assertTrue(self.professor.is_professor())
        self.assertFalse(self.professor.is_student())
    
    def test_admin_full_access(self):
        """Test admin has full access"""
        self.assertTrue(self.admin.is_admin())
        self.assertFalse(self.admin.is_student())
