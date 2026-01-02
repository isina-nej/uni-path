#!/usr/bin/env python
"""
Generate test data for Computer Engineering program
Student ID Format: xxyyzzznnn or xxxyyzzznnn
xx/xxx: Entry year (last 2-3 digits of year like 1400 -> 40 or 1399 -> 399)
yy: Education level (12=bachelor, 13=masters, 14=phd)
zzz: Field code (102 for computer engineering)
nnn: Sequential number
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unipath.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Profile
from courses.models import Course, DegreeChart
from students.models import StudentSelection

User = get_user_model()

# Field codes
FIELD_CODES = {
    'computer_engineering': '102',  # مهندسی کامپیوتر
}

# Education level codes
LEVELS = {
    12: 'کارشناسی',           # Bachelor
    13: 'کارشناسی ارشد',      # Masters
    14: 'دکتری',               # PhD
}

# Course data for Computer Engineering Bachelor (year 1400, semester 1-2)
COURSES = [
    # اول پایه
    {
        'code': 'CE-101',
        'name': 'ریاضیات ۱',
        'credits': 3,
        'level': 12,
        'prerequisite': None,
    },
    {
        'code': 'CE-102',
        'name': 'فیزیک ۱',
        'credits': 3,
        'level': 12,
        'prerequisite': None,
    },
    {
        'code': 'CE-103',
        'name': 'شیمی',
        'credits': 3,
        'level': 12,
        'prerequisite': None,
    },
    {
        'code': 'CE-104',
        'name': 'برنامه‌نویسی ۱ (Python)',
        'credits': 3,
        'level': 12,
        'prerequisite': None,
    },
    {
        'code': 'CE-105',
        'name': 'منطق و مدارهای دیجیتال',
        'credits': 3,
        'level': 12,
        'prerequisite': None,
    },
    # دوم پایه
    {
        'code': 'CE-201',
        'name': 'ریاضیات ۲',
        'credits': 3,
        'level': 12,
        'prerequisite': 'CE-101',
    },
    {
        'code': 'CE-202',
        'name': 'فیزیک ۲',
        'credits': 3,
        'level': 12,
        'prerequisite': 'CE-102',
    },
    {
        'code': 'CE-203',
        'name': 'معادلات دیفرانسیل',
        'credits': 3,
        'level': 12,
        'prerequisite': 'CE-201',
    },
    {
        'code': 'CE-204',
        'name': 'ساختمان داده‌ها',
        'credits': 3,
        'level': 12,
        'prerequisite': 'CE-104',
    },
    {
        'code': 'CE-205',
        'name': 'معماری کامپیوتر',
        'credits': 3,
        'level': 12,
        'prerequisite': 'CE-105',
    },
    # سوم
    {
        'code': 'CE-301',
        'name': 'سیستم‌های عامل',
        'credits': 3,
        'level': 12,
        'prerequisite': 'CE-204',
    },
    {
        'code': 'CE-302',
        'name': 'مبانی پایگاه‌داده‌ها',
        'credits': 3,
        'level': 12,
        'prerequisite': 'CE-204',
    },
    {
        'code': 'CE-303',
        'name': 'طراحی الگوریتم‌ها',
        'credits': 3,
        'level': 12,
        'prerequisite': 'CE-204',
    },
    {
        'code': 'CE-304',
        'name': 'مدلسازی و شبیه‌سازی',
        'credits': 3,
        'level': 12,
        'prerequisite': 'CE-201',
    },
    {
        'code': 'CE-305',
        'name': 'نظریه زبان‌های برنامه‌نویسی',
        'credits': 3,
        'level': 12,
        'prerequisite': 'CE-204',
    },
    # چهارم
    {
        'code': 'CE-401',
        'name': 'شبکه‌های کامپیوتری',
        'credits': 3,
        'level': 12,
        'prerequisite': 'CE-301',
    },
    {
        'code': 'CE-402',
        'name': 'وب و تکنولوژی وب',
        'credits': 3,
        'level': 12,
        'prerequisite': 'CE-305',
    },
    {
        'code': 'CE-403',
        'name': 'امنیت اطلاعات',
        'credits': 3,
        'level': 12,
        'prerequisite': 'CE-401',
    },
    {
        'code': 'CE-404',
        'name': 'پروژه کارشناسی',
        'credits': 4,
        'level': 12,
        'prerequisite': None,
    },
]

def create_field_and_courses():
    """Create Computer Engineering field with courses"""
    print("\n" + "="*70)
    print("📚 Creating Computer Engineering courses...")
    print("="*70)
    
    created_count = 0
    for course_data in COURSES:
        course, created = Course.objects.get_or_create(
            code=course_data['code'],
            defaults={
                'name': course_data['name'],
                'credits': course_data['credits'],
                'description': f"درس {course_data['name']}",
            }
        )
        if created:
            print(f"✅ Created course: {course.code} - {course.name}")
            created_count += 1
        else:
            print(f"⚪ Course already exists: {course.code}")
    
    print(f"\n✅ Total courses created: {created_count}")
    return created_count > 0

def generate_student_id(entry_year, level, sequence_num):
    """
    Generate student ID
    entry_year: 1399, 1400, etc.
    level: 12 (bachelor), 13 (masters), 14 (phd)
    sequence_num: 1, 2, 3, ...
    """
    # Get last 2-3 digits of entry year
    year_code = str(entry_year)[-2:]  # "40" for 1400, "99" for 1399
    level_code = str(level)  # "12", "13", "14"
    field_code = '102'  # Computer Engineering
    seq = str(sequence_num).zfill(4)  # Pad to 4 digits
    
    return f"{year_code}{level_code}{field_code}{seq}"

def create_students():
    """Create students with proper IDs"""
    print("\n" + "="*70)
    print("👥 Creating students...")
    print("="*70)
    
    students_data = [
        # Bachelor 1400
        {
            'entry_year': 1400,
            'level': 12,
            'sequence': 1,
            'first_name': 'علی',
            'last_name': 'احمدی',
            'email_suffix': 'ali.ahmadi',
        },
        {
            'entry_year': 1400,
            'level': 12,
            'sequence': 2,
            'first_name': 'فاطمه',
            'last_name': 'حسنی',
            'email_suffix': 'fateme.hasani',
        },
        {
            'entry_year': 1400,
            'level': 12,
            'sequence': 3,
            'first_name': 'محمد',
            'last_name': 'علوی',
            'email_suffix': 'mohammad.alavi',
        },
        {
            'entry_year': 1400,
            'level': 12,
            'sequence': 4,
            'first_name': 'نیما',
            'last_name': 'رحیمی',
            'email_suffix': 'nima.rahimi',
        },
        # Bachelor 1399
        {
            'entry_year': 1399,
            'level': 12,
            'sequence': 1,
            'first_name': 'سارا',
            'last_name': 'محمدی',
            'email_suffix': 'sara.mohammadi',
        },
        {
            'entry_year': 1399,
            'level': 12,
            'sequence': 2,
            'first_name': 'حسن',
            'last_name': 'پیری',
            'email_suffix': 'hassan.piri',
        },
        # Masters 1400
        {
            'entry_year': 1400,
            'level': 13,
            'sequence': 1,
            'first_name': 'دکتر علی',
            'last_name': 'کریمی',
            'email_suffix': 'dr.ali.karimi',
        },
    ]
    
    created_count = 0
    for std_data in students_data:
        # Generate student number
        student_number = generate_student_id(
            std_data['entry_year'],
            std_data['level'],
            std_data['sequence']
        )
        
        # Create or update user
        username = f"student_{student_number}"
        email = f"{std_data['email_suffix']}@uni.ir"
        
        try:
            user = User.objects.get(username=username)
            print(f"⚪ User already exists: {username}")
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                email=email,
                password='Student@123456',
                first_name=std_data['first_name'],
                last_name=std_data['last_name'],
                role='student'
            )
            print(f"✅ Created user: {username} ({email})")
            created_count += 1
        
        # Create or update profile
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'student_number': student_number,
            }
        )
        
        if created:
            print(f"   ✅ Created profile with student ID: {student_number}")
        else:
            profile.student_number = student_number
            profile.save()
            print(f"   ✅ Updated profile with student ID: {student_number}")
    
    print(f"\n✅ Total users created: {created_count}")

def assign_courses_to_students():
    """Assign courses to students based on their level"""
    print("\n" + "="*70)
    print("📖 Assigning courses to students...")
    print("="*70)
    
    # Get all bachelor students
    bachelor_users = User.objects.filter(
        role='student',
        profile__student_number__contains='12'
    )
    
    # Get all bachelor courses
    bachelor_courses = Course.objects.filter(code__startswith='CE-')
    
    assigned_count = 0
    for user in bachelor_users:
        for course in bachelor_courses[:10]:  # Assign first 10 courses
            selection, created = StudentSelection.objects.get_or_create(
                student=user,
                course=course,
                defaults={
                    'semester': 'Spring 1403',
                }
            )
            if created:
                assigned_count += 1
        
        print(f"✅ Assigned 10 courses to: {user.get_full_name()} ({user.profile.student_number})")
    
    print(f"\n✅ Total course assignments: {assigned_count}")

def print_summary():
    """Print summary of created data"""
    print("\n" + "="*70)
    print("📊 DATA SUMMARY")
    print("="*70)
    
    # Count courses
    courses_count = Course.objects.count()
    print(f"\n📚 Courses: {courses_count}")
    
    # Count users
    users_count = User.objects.filter(role='student').count()
    print(f"👥 Student Users: {users_count}")
    
    # Show students with their IDs
    print(f"\n👤 Student Details:")
    print("-" * 70)
    for profile in Profile.objects.all():
        if profile.student_number:
            print(f"  {profile.user.get_full_name():30} | ID: {profile.student_number} | {profile.user.email}")
    
    # Course samples
    print(f"\n📖 Course Samples:")
    print("-" * 70)
    for course in Course.objects.all()[:5]:
        print(f"  {course.code:10} | {course.name:30} | {course.credits} credits")

if __name__ == '__main__':
    print("\n🎓 COMPUTER ENGINEERING DATA GENERATION")
    print("="*70)
    
    try:
        create_field_and_courses()
        create_students()
        assign_courses_to_students()
        print_summary()
        
        print("\n" + "="*70)
        print("✅ Data generation completed successfully!")
        print("="*70)
        
        print("\n🔐 Test credentials:")
        print("  Username: student_40120210001")
        print("  Password: Student@123456")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
