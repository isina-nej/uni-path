"""
Test script for PRD 3.1 API endpoints

Run this after:
1. pip install -r requirements.txt
2. python manage.py migrate courses
3. python create_degree_chart_v2.py
4. python setup_chart_schema.py
5. Create a test student with ID 992101001
6. python manage.py runserver

Then:
python test_prd3.1_api.py
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

User = get_user_model()

def get_tokens_for_user(user):
    """Get access token for user"""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

def test_api():
    """Test the API endpoints"""
    print("=" * 60)
    print("PRD 3.1 API Tests")
    print("=" * 60)
    
    # Try to get test user
    try:
        user = User.objects.get(email='student1@unipath.ir')
        print(f"\n✅ Found test user: {user.email}")
    except User.DoesNotExist:
        print("\n❌ Test user not found: student1@unipath.ir")
        print("   Create test student first")
        return
    
    # Check if user has a profile with student_number
    try:
        profile = user.profile
        print(f"✅ User profile found")
        print(f"   Student Number: {profile.student_number}")
    except:
        print("❌ User profile not found")
        return
    
    # Get access token
    token = get_tokens_for_user(user)
    print(f"✅ Got access token: {token[:20]}...")
    
    # Test with Django test client
    client = Client()
    
    # Test 1: GET /api/courses/degrees/my-chart/
    print("\n📊 Testing GET /api/courses/degrees/my-chart/")
    response = client.get(
        '/api/courses/degrees/my-chart/',
        HTTP_AUTHORIZATION=f'Bearer {token}'
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
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"   Error: {response.json()}")
    
    # Test 2: GET /api/courses/degrees/recommendations/
    print("\n💡 Testing GET /api/courses/degrees/recommendations/")
    response = client.get(
        '/api/courses/degrees/recommendations/',
        HTTP_AUTHORIZATION=f'Bearer {token}'
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
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"   Error: {response.json()}")
    
    print("\n" + "=" * 60)
    print("✅ Tests completed")
    print("=" * 60)

if __name__ == "__main__":
    test_api()

