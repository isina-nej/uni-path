"""
Test script for PRD 3.1 API endpoints

Run this after:
1. python manage.py migrate courses
2. python create_degree_chart_v2.py
3. python setup_chart_schema.py
4. Create a test student with ID 992101001
5. python manage.py runserver

Then:
python test_prd3.1_api.py
"""

import requests
import json
from pathlib import Path

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_KEY = None

# Test student
TEST_STUDENT = {
    "email": "student1@unipath.ir",
    "password": "Student@123456"
}

def login():
    """Login and get access token"""
    print("🔐 Logging in...")
    response = requests.post(
        f"{BASE_URL}/api/auth/login/",
        json=TEST_STUDENT
    )
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        return None
    
    data = response.json()
    token = data.get('access')
    print(f"✅ Logged in as {TEST_STUDENT['email']}")
    print(f"   Token: {token[:20]}...")
    return token

def get_my_chart(token):
    """Test GET /api/courses/degrees/my-chart/"""
    print("\n📊 Testing GET /api/courses/degrees/my-chart/")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/courses/degrees/my-chart/",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return None
    
    data = response.json()
    print(f"✅ Chart loaded successfully")
    print(f"   Chart Code: {data['code']}")
    print(f"   Chart Name: {data['name']}")
    print(f"   Major: {data['major']}")
    print(f"   Semesters: {len(data['semesters'])}")
    print(f"   Total Credits: {data['total_credits']}")
    
    # Print semester summary
    print("\n   Semester Overview:")
    for sem in data['semesters']:
        total_credits = sem.get('total_credits', 0)
        node_count = len(sem.get('nodes', []))
        print(f"   - ترم {sem['number']}: {node_count} nodes, {total_credits} credits")
    
    print(f"\n   Passed Courses: {len(data['passed_courses'])}")
    print(f"   Completed Semesters: {data['completed_semesters']}")
    
    return data

def get_recommendations(token):
    """Test GET /api/courses/degrees/recommendations/"""
    print("\n💡 Testing GET /api/courses/degrees/recommendations/")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/courses/degrees/recommendations/",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return None
    
    data = response.json()
    print(f"✅ Recommendations loaded successfully")
    print(f"   Next Semester: {data['next_semester']}")
    print(f"   Total Recommendations: {len(data['recommendations'])}")
    
    # Print top 5 recommendations
    print("\n   Top 5 Recommendations (by priority):")
    for i, rec in enumerate(data['recommendations'][:5], 1):
        print(f"   {i}. {rec['code']} - {rec['name']}")
        print(f"      Score: {rec['priority_score']}/100")
        print(f"      Reason: {rec['reason']}")
        print(f"      Unlocks: {len(rec['unlocks'])} courses")
        print(f"      Status: {'✅ Ready' if rec['prerequisites_met'] else '❌ Blocked'}")
    
    if len(data['recommendations']) > 5:
        print(f"   ... and {len(data['recommendations']) - 5} more")
    
    return data

def validate_response_structure(data, expected_keys):
    """Validate response has expected keys"""
    missing = []
    for key in expected_keys:
        if key not in data:
            missing.append(key)
    return missing

def main():
    print("=" * 60)
    print("PRD 3.1 API Tests")
    print("=" * 60)
    
    # Login
    token = login()
    if not token:
        print("\n❌ Cannot proceed without token")
        return
    
    # Test chart endpoint
    chart_data = get_my_chart(token)
    if chart_data:
        # Validate structure
        required_keys = [
            'id', 'code', 'name', 'major', 'degree',
            'entry_year_start', 'entry_year_end', 'total_credits',
            'semesters', 'passed_courses', 'completed_semesters'
        ]
        missing = validate_response_structure(chart_data, required_keys)
        if missing:
            print(f"\n⚠️  Missing keys in chart response: {missing}")
        else:
            print("\n✅ Chart response structure validated")
    
    # Test recommendations endpoint
    rec_data = get_recommendations(token)
    if rec_data:
        # Validate structure
        required_keys = ['next_semester', 'recommendations']
        missing = validate_response_structure(rec_data, required_keys)
        if missing:
            print(f"\n⚠️  Missing keys in recommendations response: {missing}")
        else:
            print("\n✅ Recommendations response structure validated")
        
        # Validate recommendation structure
        if rec_data['recommendations']:
            rec = rec_data['recommendations'][0]
            required_keys = [
                'course_id', 'code', 'name', 'credits', 'priority_score',
                'reason', 'unlocks', 'prerequisites_met', 'is_mandatory'
            ]
            missing = validate_response_structure(rec, required_keys)
            if missing:
                print(f"⚠️  Missing keys in recommendation item: {missing}")
            else:
                print("✅ Recommendation item structure validated")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        print(f"   Make sure Django is running on {BASE_URL}")
        print("   Run: python manage.py runserver")
    except Exception as e:
        print(f"❌ Error: {e}")
