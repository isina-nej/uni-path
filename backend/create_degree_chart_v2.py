#!/usr/bin/env python
"""
Create Computer Engineering Degree Chart (Version 2)
For entry years 1392-1402 (92-402)
Uses new DegreeChart fields: start_year, end_year, field_code, level
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
        {'id': 401, 'name': 'الگوریتم', 'credits': 3},
        {'id': 402, 'name': 'معماری کامپیوتر', 'credits': 3},
        {'id': 403, 'name': 'سیگنال ها و سیستم ها', 'credits': 3},
        {'id': 404, 'name': 'جبر خطی', 'credits': 3},
        {'id': 405, 'name': 'آزمایشگاه مدار منطقی', 'credits': 1},
        {'id': 406, 'name': 'درس گروه معارف اسلامی', 'credits': 2},
        {'id': 407, 'name': 'فلسفه علم و روش پژوهش', 'credits': 2},
    ],
    # Semester 5
    5: [
        {'id': 501, 'name': 'سیستم عامل', 'credits': 3},
        {'id': 502, 'name': 'پایگاه داده', 'credits': 3},
        {'id': 503, 'name': 'نظریه زبان های برنامه نویسی', 'credits': 3},
        {'id': 504, 'name': 'آزمایشگاه معماری کامپیوتر', 'credits': 1},
        {'id': 505, 'name': 'تئوری محاسبات', 'credits': 3},
        {'id': 506, 'name': 'اخلاق و مسئولیت های اجتماعی', 'credits': 2},
        {'id': 507, 'name': 'درس گروه معارف اسلامی', 'credits': 2},
    ],
    # Semester 6
    6: [
        {'id': 601, 'name': 'کامپایلر', 'credits': 3},
        {'id': 602, 'name': 'شبکه های کامپیوتری', 'credits': 3},
        {'id': 603, 'name': 'هوش مصنوعی', 'credits': 3},
        {'id': 604, 'name': 'آزمایشگاه سیستم عامل', 'credits': 1},
        {'id': 605, 'name': 'آزمایشگاه پایگاه داده', 'credits': 1},
        {'id': 606, 'name': 'امنیت اطلاعات', 'credits': 3},
        {'id': 607, 'name': 'درس اختیاری', 'credits': 3},
    ],
    # Semester 7
    7: [
        {'id': 701, 'name': 'پردازش تصویر', 'credits': 3},
        {'id': 702, 'name': 'محاسبات موازی', 'credits': 3},
        {'id': 703, 'name': 'یادگیری ماشینی', 'credits': 3},
        {'id': 704, 'name': 'آزمایشگاه شبکه', 'credits': 1},
        {'id': 705, 'name': 'تحقق', 'credits': 1},
        {'id': 706, 'name': 'درس اختیاری 1', 'credits': 3},
        {'id': 707, 'name': 'درس اختیاری 2', 'credits': 3},
    ],
    # Semester 8
    8: [
        {'id': 801, 'name': 'گرافیکس کامپیوتری', 'credits': 3},
        {'id': 802, 'name': 'توزیع شده سیستم های', 'credits': 3},
        {'id': 803, 'name': 'پروژه خاتمه تحصیل', 'credits': 4},
        {'id': 804, 'name': 'درس اختیاری 3', 'credits': 3},
        {'id': 805, 'name': 'درس اختیاری 4', 'credits': 3},
    ],
}

# Prerequisites (course code -> list of prerequisite codes)
PREREQUISITES = {
    201: [101, 102, 107],  # Advanced Programming needs basics
    203: [102],  # Discrete Math needs Math 1
    204: [101],  # Physics 2 needs Physics 1
    301: [107, 201],  # Data Structures needs Programming
    302: [102],  # Digital Logic needs Math 1
    305: [102],  # Probability needs Math 1
    401: [301],  # Algorithms needs Data Structures
    402: [302],  # Computer Architecture needs Digital Logic
    403: [102, 204],  # Signals needs Math 1 and Physics 2
    501: [402],  # OS needs Computer Architecture
    502: [301],  # Database needs Data Structures
    503: [201],  # Programming Language Theory needs Advanced Programming
    504: [402],  # Computer Architecture Lab needs Computer Architecture
    505: [203, 401],  # Theory of Computation needs Discrete Math
    601: [503],  # Compiler needs Language Theory
    602: [402, 501],  # Networks needs Architecture and OS
    603: [305],  # AI needs Probability
    604: [501],  # OS Lab needs OS
    605: [502],  # Database Lab needs Database
    606: [501, 602],  # Security needs OS and Networks
    607: [],  # Elective has no prerequisites
    701: [603],  # Image Processing needs AI
    702: [501, 501],  # Parallel needs OS
    703: [305, 603],  # ML needs Probability and AI
    704: [602],  # Network Lab needs Networks
    801: [703],  # Graphics needs ML
    802: [602, 501],  # Distributed needs Networks and OS
    803: [701, 702, 703],  # Capstone needs 7th semester courses
}

# Corequisites (course code -> list of corequisite codes)
COREQUISITES = {
    204: [101],  # Physics 2 can be taken with Physics 1 Basics
    301: [203],  # Data Structures with Discrete Math
    304: [301],  # Physics 2 Lab with Data Structures
    404: [401],  # Linear Algebra with Algorithms
    502: [603],  # Database with AI
    601: [604],  # Compiler with OS Lab
    702: [703],  # Parallel with ML
}

def create_courses():
    """Create all courses for Computer Engineering"""
    print("\n" + "="*70)
    print("📚 Creating Courses...")
    print("="*70)
    
    created_count = 0
    for semester, courses in COURSES_DATA.items():
        for course_data in courses:
            course_id = course_data['id']
            course_code = f"CE-{course_id:03d}"
            
            course, created = Course.objects.get_or_create(
                code=course_code,
                defaults={
                    'name': course_data['name'],
                    'credits': course_data['credits'],
                    'semester': semester,
                    'is_mandatory': True,
                    'is_offered': True,
                    'description': f"کورس {course_data['name']}"
                }
            )
            
            if created:
                created_count += 1
                print(f"  ✅ {course_code}: {course_data['name']} ({course_data['credits']} credits, Sem {semester})")
    
    print(f"\n✅ Total courses created: {created_count}")
    all_courses = Course.objects.filter(code__startswith='CE-').count()
    print(f"   Total courses in system: {all_courses}")
    
    return Course.objects.filter(code__startswith='CE-')

def create_prerequisites(all_courses):
    """Create prerequisites"""
    print("\n" + "="*70)
    print("🔗 Creating Prerequisites...")
    print("="*70)
    
    created_count = 0
    for course_id, prereq_ids in PREREQUISITES.items():
        course = Course.objects.get(code=f"CE-{course_id:03d}")
        for prereq_id in prereq_ids:
            prereq_course = Course.objects.get(code=f"CE-{prereq_id:03d}")
            prereq, created = Prerequisite.objects.get_or_create(
                course=course,
                prerequisite_course=prereq_course,
                defaults={'is_corequisite': False}
            )
            if created:
                print(f"  ✅ CE-{course_id:03d} ← CE-{prereq_id:03d}")
                created_count += 1
    
    print(f"\n✅ Total prerequisites: {created_count}")

def create_corequisites(all_courses):
    """Create co-requisites"""
    print("\n" + "="*70)
    print("⚡ Creating Co-requisites...")
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

def create_degree_chart(all_courses):
    """Create DegreeChart for Computer Engineering with entry year range"""
    print("\n" + "="*70)
    print("📊 Creating Degree Chart...")
    print("="*70)
    
    # DegreeChart for entry years 1392-1402 (92-402)
    degree_chart, created = DegreeChart.objects.get_or_create(
        code='CS-BS-92-402',
        defaults={
            'name': 'مهندسی کامپیوتر - کارشناسی',
            'level': '12',  # Bachelor
            'field_code': '102',  # Computer Engineering
            'start_year': 1392,
            'end_year': 1402,
            'total_credits': 132,
            'department': 'فنی و مهندسی',
            'description': 'برنامه درسی مهندسی کامپیوتر برای ورودی‌های 1392 تا 1402',
        }
    )
    
    if created:
        print(f"✅ Created DegreeChart:")
        print(f"   Name: {degree_chart.name}")
        print(f"   Code: {degree_chart.code}")
        print(f"   Entry Years: {degree_chart.start_year}-{degree_chart.end_year}")
        print(f"   Level: {degree_chart.get_level_display()}")
        print(f"   Field Code: {degree_chart.field_code}")
        print(f"   Total Credits: {degree_chart.total_credits}")
        
        # Link courses to degree chart with semester information
        created_links = 0
        for semester, courses in COURSES_DATA.items():
            for idx, course_data in enumerate(courses, 1):
                course_code = f"CE-{course_data['id']:03d}"
                course = Course.objects.get(code=course_code)
                
                chart_course, link_created = ChartCourse.objects.get_or_create(
                    degree_chart=degree_chart,
                    course=course,
                    defaults={
                        'is_mandatory': True,
                        'recommended_semester': semester,
                    }
                )
                if link_created:
                    created_links += 1
        
        print(f"\n   ✅ Linked {created_links} courses to degree chart")
    else:
        print(f"⚪ DegreeChart already exists: {degree_chart.code}")
    
    return degree_chart

def print_summary():
    """Print summary"""
    print("\n" + "="*70)
    print("📋 SUMMARY")
    print("="*70)
    
    courses_count = Course.objects.filter(code__startswith='CE-').count()
    degrees_count = DegreeChart.objects.filter(code='CS-BS-92-402').count()
    chart_courses = ChartCourse.objects.filter(degree_chart__code='CS-BS-92-402').count()
    prereqs_count = Prerequisite.objects.filter(is_corequisite=False).count()
    coreqs_count = Prerequisite.objects.filter(is_corequisite=True).count()
    
    print(f"\n📚 Computer Science Courses: {courses_count}")
    print(f"📊 Degree Charts: {degrees_count}")
    print(f"🔗 Courses in Chart: {chart_courses}")
    print(f"📌 Prerequisites: {prereqs_count}")
    print(f"⚡ Co-requisites: {coreqs_count}")

if __name__ == '__main__':
    print("\n🎓 COMPUTER ENGINEERING DEGREE CHART CREATION (V2)")
    print("="*70)
    print("Using new DegreeChart fields: start_year, end_year, field_code, level")
    
    try:
        all_courses = create_courses()
        create_prerequisites(all_courses)
        create_corequisites(all_courses)
        degree_chart = create_degree_chart(all_courses)
        print_summary()
        
        print("\n" + "="*70)
        print("✅ Degree chart creation completed successfully!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
