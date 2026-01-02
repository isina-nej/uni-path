#!/usr/bin/env python
"""Test API endpoints"""
import urllib.request
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def test_api_login(username, label):
    """Test login via API"""
    print(f"\n{'='*70}")
    print(f"🧪 TEST: Login with {label}")
    print(f"{'='*70}")
    
    data = {
        'username': username,
        'password': 'Student@123456'
    }
    
    json_data = json.dumps(data).encode('utf-8')
    
    try:
        req = urllib.request.Request(
            f'{BASE_URL}/auth/login/',
            data=json_data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"✅ SUCCESS (Status: {response.status})")
            print(f"   Access Token: {result.get('access', 'N/A')[:40]}...")
            print(f"   User: {result.get('user', {})}")
            return True
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"❌ FAILED (Status: {e.code})")
        print(f"   Response: {error_body}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Run tests
print("\n" + "🔐 TESTING LOGIN WITH BOTH USERNAME AND EMAIL" + "\n")

test1 = test_api_login('student1', 'USERNAME (student1)')
test2 = test_api_login('student1@unipath.ir', 'EMAIL (student1@unipath.ir)')

print(f"\n{'='*70}")
print(f"📊 RESULTS:")
print(f"   Username login: {'✅ PASS' if test1 else '❌ FAIL'}")
print(f"   Email login:    {'✅ PASS' if test2 else '❌ FAIL'}")
print(f"{'='*70}\n")

if test1 and test2:
    print("🎉 ALL TESTS PASSED! Email-to-username fix is working perfectly!")
