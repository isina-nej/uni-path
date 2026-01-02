#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unipath.settings')
django.setup()

from accounts.models import User
from courses.models import Course

print('\n' + '='*60)
print('🔧 ایجاد داده‌های تست...')
print('='*60 + '\n')

# 1. Create test users
print('👥 ایجاد کاربران تست...\n')

test_users = [
    {
        'username': 'student1',
        'email': 'student1@unipath.ir',
        'password': 'Student@123456',
        'first_name': 'محمد',
        'last_name': 'احمدی',
        'role': 'student'
    },
    {
        'username': 'student2',
        'email': 'student2@unipath.ir',
        'password': 'Student@123456',
        'first_name': 'فاطمه',
        'last_name': 'حسینی',
        'role': 'student'
    },
    {
        'username': 'professor1',
        'email': 'professor1@unipath.ir',
        'password': 'Professor@123456',
        'first_name': 'دکتر',
        'last_name': 'علی‌زاده',
        'role': 'professor'
    }
]

created_users = []
for user_data in test_users:
    password = user_data.pop('password')
    username = user_data['username']
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        print(f'  ⚠️  {username} قبلاً وجود دارد.')
    else:
        user = User.objects.create_user(**user_data, password=password)
        created_users.append(user)
        print(f'  ✅ {username} ایجاد شد')
        print(f'      📧 {user.email}')
        print(f'      🔐 {password}')

print()

# 2. Create courses
print('📚 ایجاد درس‌های تست...\n')

courses_data = [
    {
        'name': 'ریاضی 1',
        'code': 'MATH101',
        'credits': 3,
        'is_mandatory': True,
        'semester': 1,
        'instructor': 'دکتر علی‌زاده'
    },
    {
        'name': 'فیزیک 1',
        'code': 'PHYS101',
        'credits': 4,
        'is_mandatory': True,
        'semester': 1,
        'instructor': 'دکتر محمدی'
    },
    {
        'name': 'برنامه‌نویسی با Python',
        'code': 'CS101',
        'credits': 3,
        'is_mandatory': True,
        'semester': 1,
        'instructor': 'دکتر حسنی'
    },
    {
        'name': 'شیمی عمومی',
        'code': 'CHEM101',
        'credits': 4,
        'is_mandatory': True,
        'semester': 2,
        'instructor': 'دکتر رضایی'
    },
    {
        'name': 'جبر خطی',
        'code': 'MATH201',
        'credits': 3,
        'is_mandatory': False,
        'semester': 2,
        'instructor': 'دکتر احمدی'
    }
]

for course_data in courses_data:
    course, created = Course.objects.get_or_create(
        code=course_data['code'],
        defaults=course_data
    )
    status = '✅ ایجاد شد' if created else '⚠️  موجود'
    print(f'  {status}: {course.name} ({course.code}) - {course.credits} واحد')

print()
print('='*60)
print('✅ داده‌های تست ایجاد شد!')
print('='*60)
print()
print('📋 اطلاعات ورود برای تست:')
print('='*60)
for user_data in test_users:
    if not User.objects.filter(username=user_data['username']).filter(password__startswith='pbkdf2_sha256').exists():
        print(f'\n  👤 {user_data["username"]}')
        print(f'     📧 {user_data["email"]}')
        # Note: password removed from test_users dict above, showing from original
        idx = [u['username'] for u in test_users].index(user_data['username'])
        print(f'     🔐 Student@123456' if idx < 2 else f'     🔐 Professor@123456')
