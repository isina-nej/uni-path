#!/usr/bin/env python
"""Test login with email and username"""
import requests
import json

# Disable SSL verification warnings
import urllib3
urllib3.disable_warnings()

# Create a session with SSL verification disabled
session = requests.Session()
session.verify = False

BASE_URL = 'http://127.0.0.1:8000/api'

def test_login_username():
    """Test login with username"""
    print("\n" + "="*60)
    print("✅ TEST 1: Login with USERNAME (student1)")
    print("="*60)
    
    data = {
        'username': 'student1',
        'password': 'Student@123456'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login/', json=data, verify=False)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Access Token: {result.get('access', 'N/A')[:30]}...")
            print(f"User: {result.get('user', {})}")
        else:
            print(f"❌ FAILED!")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_login_email():
    """Test login with email"""
    print("\n" + "="*60)
    print("✅ TEST 2: Login with EMAIL (student1@unipath.ir)")
    print("="*60)
    
    data = {
        'username': 'student1@unipath.ir',
        'password': 'Student@123456'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login/', json=data, verify=False)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Access Token: {result.get('access', 'N/A')[:30]}...")
            print(f"User: {result.get('user', {})}")
        else:
            print(f"❌ FAILED!")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_login_username()
    test_login_email()
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60)
