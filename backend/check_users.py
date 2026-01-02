#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unipath.settings')
django.setup()

from accounts.models import User

print('\n' + '='*50)
print('📊 کاربران موجود در دیتابیس:')
print('='*50 + '\n')

users = User.objects.all()

if users.exists():
    for user in users:
        print(f'👤 نام کاربری: {user.username}')
        print(f'   📧 ایمیل: {user.email}')
        print(f'   🔐 نقش: {user.role if hasattr(user, "role") else "N/A"}')
        print(f'   ✓ Admin: {user.is_staff}\n')
else:
    print('❌ هیچ کاربری یافت نشد!\n')

print('='*50)
print(f'✅ کل کاربران: {users.count()}')
print('='*50 + '\n')

# Check courses
from courses.models import Course

print('='*50)
print('📚 درس‌های موجود:')
print('='*50 + '\n')

courses = Course.objects.all()
if courses.exists():
    for course in courses[:10]:  # Show first 10
        print(f'• {course.name} ({course.code})')
else:
    print('❌ هیچ درسی یافت نشد!\n')

print(f'\n✅ کل درس‌ها: {courses.count()}\n')
