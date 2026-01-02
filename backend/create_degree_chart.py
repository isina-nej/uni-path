#!/usr/bin/env python
"""
Create Computer Engineering Degree Chart
For entry years 1392-1402 (92-402)
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unipath.settings')
django.setup()

from django.contrib.auth import get_user_model
from courses.models import Course, DegreeChart, Prerequisite, ChartCourse

User = get_user_model()

# Course data with semester information
COURSES_DATA = {
    # Semester 1
    1: [
        {'id': 101, 'name': 'فیزیک 1', 'credits': 3},
        {'id': 102, 'name': 'ریاضی عمومی 1', 'credits': 3},
        {'id': 103, 'name': 'دروس گروه معارف اسلامی', 'credits': 2},
        {'id': 104, 'name': 'دانش خانواده', 'credits': 2},
        {'id': 105, 'name': 'فارسی', 'credits': 3},
        {'id': 107, 'name': 'کامپیوتر و برنامه سازی مبانی', 'credits': 3},
        {'id': 106, 'name': 'تربیت بدنی', 'credits': 1},
    ],
    # Semester 2
    2: [
        {'id': 201, 'name': 'برنامه سازی پیشرفته', 'credits': 3},
        {'id': 202, 'name': 'کارگاه کامپیوتر', 'credits': 1},
        {'id': 203, 'name': 'ریاضیات گسسته', 'credits': 3},
        {'id': 204, 'name': 'فیزیک 2', 'credits': 3},
        {'id': 205, 'name': 'ریاضی عمومی 2', 'credits': 3},
        {'id': 206, 'name': 'زبان انگلیسی', 'credits': 3},
        {'id': 207, 'name': 'ورزش', 'credits': 1},
        {'id': 208, 'name': 'دروس گروه معارف اسلامی', 'credits': 2},
    ],
    # Semester 3
    3: [
        {'id': 301, 'name': 'ساختمان های داده', 'credits': 3},
        {'id': 302, 'name': 'مدار منطقی', 'credits': 3},
        {'id': 303, 'name': 'معادلات دیفرانسیل', 'credits': 3},
        {'id': 304, 'name': 'آزمایشگاه فیزیک 2', 'credits': 1},
        {'id': 305, 'name': 'آمار و احتمالات مهندسی', 'credits': 3},
        {'id': 306, 'name': 'زبان تخصصی', 'credits': 2},
        {'id': 307, 'name': 'درس گروه معارف اسلامی', 'credits': 2},
    ],
    # Semester 4
    4: [
        {'id': 401, 'name': 'طراحی الگوریتم‌ها', 'credits': 3},
        {'id': 402, 'name': 'نظریه زبان‌ها و ماشین‌ها', 'credits': 3},
        {'id': 403, 'name': 'آزمایشگاه مدار منطقی و معماری کامپیوتر', 'credits': 1},
        {'id': 404, 'name': 'معماری کامپیوتر', 'credits': 3},
        {'id': 405, 'name': 'ریاضیات مهندسی', 'credits': 3},
        {'id': 406, 'name': 'مدار الکتریکی', 'credits': 3},
        {'id': 407, 'name': 'دروس گروه معارف اسلامی', 'credits': 2},
    ],
    # Semester 5
    5: [
        {'id': 501, 'name': 'هوش مصنوعی و سیستم‌های خبره', 'credits': 3},
        {'id': 502, 'name': 'طراحی کامپایلر', 'credits': 3},
        {'id': 503, 'name': 'پایگاه داده‌ها', 'credits': 3},
        {'id': 504, 'name': 'ریزپردازنده و زبان اسمبلی', 'credits': 3},
        {'id': 505, 'name': 'سیگنال‌ها و سیستم‌ها', 'credits': 3},
        {'id': 506, 'name': 'روش پژوهش و ارائه', 'credits': 2},
        {'id': 507, 'name': 'دروس گروه معارف اسلامی', 'credits': 2},
    ],
    # Semester 6
    6: [
        {'id': 601, 'name': 'تحلیل و طراحی سیستم', 'credits': 3},
        {'id': 602, 'name': 'مبانی هوش محاسباتی', 'credits': 3},
        {'id': 603, 'name': 'طراحی زبان‌های برنامه‌سازی', 'credits': 3},
        {'id': 604, 'name': 'سیستم‌های عامل', 'credits': 3},
        {'id': 605, 'name': 'طراحی سیستم‌های دیجیتالی', 'credits': 3},
        {'id': 606, 'name': 'درس اختیاری', 'credits': 1},
        {'id': 607, 'name': 'دروس گروه معارف اسلامی', 'credits': 2},
    ],
    # Semester 7
    7: [
        {'id': 701, 'name': 'مهندسی نرم افزار', 'credits': 3},
        {'id': 702, 'name': 'درس اختیاری', 'credits': 1},
        {'id': 703, 'name': 'شبکه‌های کامپیوتری', 'credits': 3},
        {'id': 704, 'name': 'آزمایشگاه سیستم‌های عامل', 'credits': 1},
        {'id': 705, 'name': 'آزمایشگاه ریزپردازنده', 'credits': 1},
        {'id': 706, 'name': 'اصول رباتیک', 'credits': 3},
        {'id': 707, 'name': 'درس اختیاری', 'credits': 3},
    ],
    # Semester 8
    8: [
        {'id': 801, 'name': 'پروژه نرم افزار (بعد از 100 واحد)', 'credits': 3},
        {'id': 802, 'name': 'مهندسی اینترنت', 'credits': 3},
        {'id': 803, 'name': 'آزمایشگاه شبکه‌های کامپیوتری', 'credits': 1},
        {'id': 804, 'name': 'مبانی بینایی ماشین', 'credits': 3},
        {'id': 805, 'name': 'مبانی پردازش گفتار', 'credits': 3},
        {'id': 806, 'name': 'درس اختیاری', 'credits': 3},
        {'id': 807, 'name': 'کاراموزی', 'credits': 1},
    ],
}

# Prerequisites
PREREQUISITES = {
    201: [107],
    202: [107],
    204: [102],
    205: [102],
    207: [106],
    301: [203, 201],
    303: [102],
    304: [204],
    305: [205],
    306: [206],
    401: [301],
    402: [301],
    403: [302],
    404: [302],
    405: [303, 205],
    406: [303],
    501: [301],
    502: [301],
    503: [301],
    504: [404],
    505: [405],
    506: [306],
    601: [201],
    602: [201],
    603: [502],
    604: [301, 404],
    605: [404],
    701: [601],
    703: [604],
    706: [505],
    804: [602],
    802: [703],
    805: [505],
}

# Co-requisites
COREQUISITES = {
    101: [102],
    203: [107, 102],
    302: [203],
    403: [404],
    704: [604],
    705: [504],
    803: [703],
}

# Section times data
SECTIONS_DATA = [
    {'course_id': 101, 'exam': '1404-03-11T09:00:00', 'capacity': 40, 'instructor': 'دکتر احمدی', 'desc': 'سکشن ویژه'},
    {'course_id': 101, 'exam': '1404-03-20T14:00:00', 'capacity': 40, 'instructor': 'دکتر احمدی', 'desc': None},
    {'course_id': 102, 'exam': '1404-03-12T11:00:00', 'capacity': 35, 'instructor': 'دکتر رضایی', 'desc': None},
    {'course_id': 201, 'exam': '1404-03-13T15:00:00', 'capacity': 30, 'instructor': 'مهندس محمدی', 'desc': None},
    {'course_id': 203, 'exam': '1404-03-14T10:00:00', 'capacity': 45, 'instructor': 'دکتر حسینی', 'desc': None},
    {'course_id': 301, 'exam': '1404-03-17T14:00:00', 'capacity': 30, 'instructor': 'دکتر کریمی', 'desc': None},
    {'course_id': 302, 'exam': '1404-03-18T11:00:00', 'capacity': 35, 'instructor': 'دکتر محمودی', 'desc': None},
    {'course_id': 401, 'exam': '1404-03-19T10:00:00', 'capacity': 25, 'instructor': 'دکتر جعفری', 'desc': None},
]

SECTION_TIMES = [
    {'section_idx': 0, 'day': 'شنبه', 'start': '08:00', 'end': '10:00', 'location': 'کلاس 101'},
    {'section_idx': 1, 'day': 'چهارشنبه', 'start': '14:00', 'end': '16:00', 'location': 'کلاس 102'},
    {'section_idx': 2, 'day': 'یکشنبه', 'start': '10:00', 'end': '12:00', 'location': 'کلاس 201'},
    {'section_idx': 3, 'day': 'دوشنبه', 'start': '14:00', 'end': '16:00', 'location': 'کلاس 301'},
]

def create_courses():
    """Create all courses"""
    print("\n" + "="*70)
    print("📚 Creating courses...")
    print("="*70)
    
    created_count = 0
    for semester, courses in COURSES_DATA.items():
        for course_data in courses:
            course, created = Course.objects.get_or_create(
                code=f"CE-{course_data['id']}",
                defaults={
                    'name': course_data['name'],
                    'credits': course_data['credits'],
                    'description': f"{course_data['name']} - ترم {semester}",
                }
            )
            if created:
                print(f"✅ Created: CE-{course_data['id']:03d} | {course.name}")
                created_count += 1
    
    print(f"\n✅ Total courses: {created_count}")
    return Course.objects.filter(code__startswith='CE-')

def create_prerequisites(all_courses):
    """Create prerequisites"""
    print("\n" + "="*70)
    print("🔗 Creating prerequisites...")
    print("="*70)
    
    created_count = 0
    for course_id, prereq_ids in PREREQUISITES.items():
        course = Course.objects.get(code=f"CE-{course_id:03d}")
        for prereq_id in prereq_ids:
            prereq_course = Course.objects.get(code=f"CE-{prereq_id:03d}")
            prereq, created = Prerequisite.objects.get_or_create(
                course=course,
                prerequisite_course=prereq_course
            )
            if created:
                print(f"  ✅ CE-{course_id:03d} ← CE-{prereq_id:03d}")
                created_count += 1
    
    print(f"\n✅ Total prerequisites: {created_count}")

def create_corequisites(all_courses):
    """Create co-requisites"""
    print("\n" + "="*70)
    print("⚡ Creating co-requisites...")
    print("="*70)
    
    created_count = 0
    for course_id, coreq_ids in COREQUISITES.items():
        course = Course.objects.get(code=f"CE-{course_id:03d}")
        for coreq_id in coreq_ids:
            coreq_course = Course.objects.get(code=f"CE-{coreq_id:03d}")
            coreq, created = Prerequisite.objects.get_or_create(
                course=course,
                prerequisite_course=coreq_course,
                defaults={'is_corequisite': True}
            )
            if not created and not coreq.is_corequisite:
                coreq.is_corequisite = True
                coreq.save()
                print(f"  ✅ CE-{course_id:03d} ≈ CE-{coreq_id:03d} (updated)")
            elif created:
                print(f"  ✅ CE-{course_id:03d} ≈ CE-{coreq_id:03d}")
                created_count += 1
    
    print(f"\n✅ Total co-requisites: {created_count}")

def create_degree_chart():
    """Create DegreeChart for Computer Engineering"""
    print("\n" + "="*70)
    print("📊 Creating Degree Chart...")
    print("="*70)
    
    # DegreeChart for entry years 92-402 (1392-1402)
    degree_chart, created = DegreeChart.objects.get_or_create(
        name='مهندسی کامپیوتر - کارشناسی (ورودی 92-402)',
        defaults={
            'degree_level': 'bachelor',  # کارشناسی
            'field_code': '102',  # مهندسی کامپیوتر
            'start_year': 1392,
            'end_year': 1402,
            'total_units': 132,
            'description': 'برنامه درسی مهندسی کامپیوتر برای ورودی‌های 92 تا 402',
        }
    )
    
    if created:
        print(f"✅ Created DegreeChart: {degree_chart.name}")
        
        # Add all courses to degree chart
        all_courses = Course.objects.filter(code__startswith='CE-')
        for course in all_courses:
            degree_chart.courses.add(course)
        
        print(f"   ✅ Added {all_courses.count()} courses")
    else:
        print(f"⚪ DegreeChart already exists")
    
    return degree_chart

def create_sections():
    """Create course sections - skipped (model doesn't exist)"""
    print("\n" + "="*70)
    print("🎓 Sections not created (model not available)")
    print("="*70)
    
    return {}

def create_section_times(section_map):
    """Create section times - skipped (model doesn't exist)"""
    print("\n" + "="*70)
    print("⏰ Section times not created (model not available)")
    print("="*70)

def print_summary():
    """Print summary"""
    print("\n" + "="*70)
    print("📋 SUMMARY")
    print("="*70)
    
    courses_count = Course.objects.filter(code__startswith='CE-').count()
    degrees_count = DegreeChart.objects.filter(name__contains='مهندسی کامپیوتر').count()
    prereqs_count = Prerequisite.objects.count()
    coreqs_count = CoRequisite.objects.count()
    
    print(f"\n📚 Courses: {courses_count}")
    print(f"📊 Degree Charts: {degrees_count}")
    print(f"🔗 Prerequisites: {prereqs_count}")
    print(f"⚡ Co-requisites: {coreqs_count}")

if __name__ == '__main__':
    print("\n🎓 COMPUTER ENGINEERING DEGREE CHART CREATION")
    print("="*70)
    
    try:
        all_courses = create_courses()
        create_prerequisites(all_courses)
        create_corequisites(all_courses)
        degree_chart = create_degree_chart()
        section_map = create_sections()
        create_section_times(section_map)
        print_summary()
        
        print("\n" + "="*70)
        print("✅ Degree chart creation completed successfully!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
