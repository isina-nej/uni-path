#!/usr/bin/env python
"""Test serializer directly in Django"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unipath.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from accounts.views import CustomTokenObtainPairView

print("\n" + "🔐 API TEST WITH HTTP CLIENT" + "\n")

factory = APIRequestFactory()

# Test 1: Login with username
print("="*70)
print("✅ TEST 1: Login with USERNAME (student1)")
print("="*70)

request1 = factory.post('/api/auth/login/', {
    'username': 'student1',
    'password': 'Student@123456'
}, format='json')

view1 = CustomTokenObtainPairView.as_view()
response1 = view1(request1)

print(f"Status: {response1.status_code}")
if response1.status_code == 200:
    print(f"✅ SUCCESS!")
    print(f"   Access Token: {response1.data.get('access', 'N/A')[:40]}...")
    user_data = response1.data.get('user', {})
    print(f"   User: {user_data}")
else:
    print(f"❌ FAILED!")
    print(f"   Response: {response1.data}")

# Test 2: Login with email
print("\n" + "="*70)
print("✅ TEST 2: Login with EMAIL (student1@unipath.ir)")
print("="*70)

request2 = factory.post('/api/auth/login/', {
    'username': 'student1@unipath.ir',
    'password': 'Student@123456'
}, format='json')

view2 = CustomTokenObtainPairView.as_view()
response2 = view2(request2)

print(f"Status: {response2.status_code}")
if response2.status_code == 200:
    print(f"✅ SUCCESS!")
    print(f"   Access Token: {response2.data.get('access', 'N/A')[:40]}...")
    user_data = response2.data.get('user', {})
    print(f"   User: {user_data}")
else:
    print(f"❌ FAILED!")
    print(f"   Response: {response2.data}")

print("\n" + "="*70)
if response1.status_code == 200 and response2.status_code == 200:
    print("🎉 ALL TESTS PASSED! Both username and email login work!")
else:
    print(f"⚠️  Some tests failed")
print("="*70 + "\n")
