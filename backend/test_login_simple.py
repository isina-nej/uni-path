#!/usr/bin/env python
"""Simple test login"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unipath.settings')
django.setup()

from django.contrib.auth import authenticate
from accounts.serializers import CustomTokenObtainPairSerializer

print("\n" + "="*70)
print("🧪 TEST AUTHENTICATION LOCALLY")
print("="*70)

# Test 1: Username only
print("\n📌 TEST 1: Authenticate with USERNAME (student1)")
print("-" * 70)
user1 = authenticate(username='student1', password='Student@123456')
if user1:
    print(f"✅ User authenticated: {user1.username}")
    print(f"   Email: {user1.email}")
else:
    print(f"❌ Authentication failed")

# Test 2: Email (this is what our fix should handle)
print("\n📌 TEST 2: Authenticate with EMAIL (student1@unipath.ir)")
print("-" * 70)
user2 = authenticate(username='student1@unipath.ir', password='Student@123456')
if user2:
    print(f"✅ User authenticated: {user2.username}")
    print(f"   Email: {user2.email}")
else:
    print(f"❌ Authentication failed (this is normal - Django doesn't support email by default)")

# Test 3: Test our custom serializer fix
print("\n📌 TEST 3: Test CustomTokenObtainPairSerializer with EMAIL")
print("-" * 70)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import User

try:
    user = User.objects.get(email='student1@unipath.ir')
    print(f"✅ Found user by email: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   Role: {user.role}")
    
    # Now test if our serializer can handle it
    serializer = CustomTokenObtainPairSerializer(data={
        'username': 'student1@unipath.ir',
        'password': 'Student@123456'
    })
    
    if serializer.is_valid():
        print(f"\n✅ Serializer VALID! Email-to-username fix is working!")
        print(f"   Access Token: {serializer.validated_data['access'][:30]}...")
        print(f"   User Data: {serializer.validated_data.get('user', {})}")
    else:
        print(f"\n❌ Serializer invalid: {serializer.errors}")
        
except User.DoesNotExist:
    print(f"❌ User with email 'student1@unipath.ir' not found")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("✅ Tests completed!")
print("="*70)
