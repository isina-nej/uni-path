"""
Test script for PRD 3.1 API endpoints

Run this after:
1. pip install -r requirements.txt
2. python manage.py migrate courses
3. python create_degree_chart_v2.py
4. python setup_chart_schema.py
5. python test_prd3.1_api.py

This script will automatically:
- Find or create a test student
- Ensure student_number is set (992101001)
- Test the API endpoints
"""

import sys
import django
import os

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unipath.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import Profile

User = get_user_model()

def get_tokens_for_user(user):
    """Get access token for user"""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

def setup_test_user():
    """Setup or update test user with student_number"""
    try:
        user = User.objects.get(email='student1@unipath.ir')
        print(f"✅ Found test user: {user.email}")
    except User.DoesNotExist:
        print(f"📝 Creating test user...")
        user = User.objects.create_user(
            username='student1',
            email='student1@unipath.ir',
            password='Student@123456',
            role='student'
        )
        print(f"✅ Created test user: {user.email}")
    
    # Get or create profile
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        print(f"📝 Creating profile for user...")
        profile = Profile.objects.create(user=user)
    
    # Ensure student_number is set
    if not profile.student_number:
        profile.student_number = '992101001'  # Entry year 99, Major 210 (CS)
        profile.save()
        print(f"📝 Set student_number: {profile.student_number}")
    else:
        print(f"✅ Student number: {profile.student_number}")
    
    return user

def test_api():
    """Test the API endpoints"""
    print("=" * 60)
    print("PRD 3.1 API Tests")
    print("=" * 60)
    
    # Setup test user
    user = setup_test_user()
    
    # Check profile
    profile = user.profile
    if not profile.student_number:
        print("❌ Student number not set!")
        return
    
    print(f"✅ User profile verified")
    print(f"   Email: {user.email}")
    print(f"   Student Number: {profile.student_number}")
    
    # Get access token
    token = get_tokens_for_user(user)
    print(f"✅ Got access token: {token[:20]}...")
    
    # Test with Django test client
    client = Client()
    
    # Test 1: GET /api/courses/degrees/my-chart/
    print("\n📊 Testing GET /api/courses/degrees/my-chart/")
    try:
        response = client.get(
            '/api/courses/degrees/my-chart/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
            SERVER_NAME='testserver'
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chart loaded successfully")
            print(f"   Chart Code: {data['code']}")
            print(f"   Chart Name: {data['name']}")
            print(f"   Major: {data['major']}")
            print(f"   Semesters: {len(data['semesters'])}")
            print(f"   Total Credits: {data['total_credits']}")
            print(f"   Passed Courses: {len(data['passed_courses'])}")
            return data
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Content-Type: {response.get('Content-Type', 'N/A')}")
            if response.status_code == 400:
                try:
                    print(f"   Error: {response.json()}")
                except:
                    print(f"   Response: {response.content[:200]}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_recommendations(token):
    """Test GET /api/courses/degrees/recommendations/"""
    print("\n💡 Testing GET /api/courses/degrees/recommendations/")
    
    client = Client()
    try:
        response = client.get(
            '/api/courses/degrees/recommendations/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
            SERVER_NAME='testserver'
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Recommendations loaded successfully")
            print(f"   Next Semester: {data['next_semester']}")
            print(f"   Total Recommendations: {len(data['recommendations'])}")
            
            if data['recommendations']:
                print(f"\n   Top 3 Recommendations:")
                for i, rec in enumerate(data['recommendations'][:3], 1):
                    print(f"   {i}. {rec['code']} - {rec['name']}")
                    print(f"      Score: {rec['priority_score']}/100")
                    print(f"      Reason: {rec['reason']}")
            return data
        else:
            print(f"❌ Failed: {response.status_code}")
            if response.status_code == 400:
                try:
                    print(f"   Error: {response.json()}")
                except:
                    print(f"   Response: {response.content[:200]}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    # Setup test user
    user = setup_test_user()
    token = get_tokens_for_user(user)
    
    # Run tests
    chart_data = test_api()
    
    if chart_data:
        rec_data = test_recommendations(token)
    
    print("\n" + "=" * 60)
    print("✅ Tests completed")
    print("=" * 60)


