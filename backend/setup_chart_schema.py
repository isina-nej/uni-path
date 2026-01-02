#!/usr/bin/env python
"""
Populate Computer Engineering Degree Chart (PRD 2.2 - Chart Schema Version)
Creates ChartSchema with versioning and CourseGroups for electives.
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unipath.settings')
django.setup()

from courses.models import (
    Course, ChartSchema, CourseGroup, ChartNode, Prerequisite
)

def create_chart_schema():
    """Create ChartSchema for Computer Engineering Bachelor"""
    print("\n" + "="*70)
    print("📊 Creating Chart Schema for Computer Engineering...")
    print("="*70)
    
    schema, created = ChartSchema.objects.get_or_create(
        major='CS',
        degree='12',
        entry_year_start=1392,
        entry_year_end=1402,
        defaults={
            'name': 'مهندسی کامپیوتر - کارشناسی (ورودی ۹۲-۴۰۲)',
            'code': 'CS-BS-92-402',
            'description': 'برنامه درسی مهندسی کامپیوتر برای ورودی‌های ۱۳۹۲ تا ۱۴۰۲',
            'total_credits': 132,
            'is_active': True,
        }
    )
    
    if created:
        print(f"✅ Created ChartSchema:")
        print(f"   Name: {schema.name}")
        print(f"   Code: {schema.code}")
        print(f"   Entry Years: {schema.entry_year_start}-{schema.entry_year_end}")
        print(f"   Degree: {schema.get_degree_display()}")
        print(f"   Total Credits: {schema.total_credits}")
    else:
        print(f"⚪ ChartSchema already exists: {schema.code}")
    
    return schema


def create_elective_groups():
    """Create elective groups for degree program"""
    print("\n" + "="*70)
    print("🎯 Creating Elective Course Groups...")
    print("="*70)
    
    # Technical Electives Group
    tech_electives, created = CourseGroup.objects.get_or_create(
        code='TECH-ELECTIVE',
        defaults={
            'name': 'دروس اختیاری فنی',
            'description': 'دروس اختیاری تخصصی برای رشته کامپیوتر'
        }
    )
    
    if created:
        print(f"✅ Created CourseGroup: {tech_electives.name}")
    else:
        print(f"⚪ CourseGroup already exists: {tech_electives.code}")
    
    # Add technical elective courses (701, 703, 705, 706, 707)
    tech_codes = ['CE-701', 'CE-703', 'CE-705', 'CE-706', 'CE-707']
    for code in tech_codes:
        try:
            course = Course.objects.get(code=code)
            tech_electives.courses.add(course)
        except Course.DoesNotExist:
            print(f"   ⚠️  Course {code} not found")
    
    if created:
        print(f"   ✅ Added {tech_electives.courses.count()} technical elective courses")
    
    # General Electives Group
    gen_electives, created = CourseGroup.objects.get_or_create(
        code='GEN-ELECTIVE',
        defaults={
            'name': 'دروس اختیاری عمومی',
            'description': 'دروس اختیاری عمومی برای تعمیق دانش'
        }
    )
    
    if created:
        print(f"✅ Created CourseGroup: {gen_electives.name}")
    else:
        print(f"⚪ CourseGroup already exists: {gen_electives.code}")
    
    # Add general elective courses (607, 804, 805)
    gen_codes = ['CE-607', 'CE-804', 'CE-805']
    for code in gen_codes:
        try:
            course = Course.objects.get(code=code)
            gen_electives.courses.add(course)
        except Course.DoesNotExist:
            print(f"   ⚠️  Course {code} not found")
    
    if created:
        print(f"   ✅ Added {gen_electives.courses.count()} general elective courses")
    
    return tech_electives, gen_electives


def create_chart_structure(schema, tech_electives, gen_electives):
    """Create ChartNodes for the schema"""
    print("\n" + "="*70)
    print("📋 Building Chart Structure (Semester Layout)...")
    print("="*70)
    
    # Define chart structure: (semester, position, course_code, is_mandatory)
    chart_structure = [
        # Semester 1
        (1, 1, 'CE-101', True),   # Physics 1
        (1, 2, 'CE-102', True),   # Math 1
        (1, 3, 'CE-103', True),   # Islamic Studies
        (1, 4, 'CE-104', True),   # Family Knowledge
        (1, 5, 'CE-105', True),   # Persian
        (1, 6, 'CE-107', True),   # Programming Basics
        (1, 7, 'CE-106', True),   # Physical Education
        
        # Semester 2
        (2, 1, 'CE-201', True),
        (2, 2, 'CE-202', True),
        (2, 3, 'CE-203', True),
        (2, 4, 'CE-204', True),
        (2, 5, 'CE-205', True),
        (2, 6, 'CE-206', True),
        (2, 7, 'CE-207', True),
        (2, 8, 'CE-208', True),
        
        # Semester 3
        (3, 1, 'CE-301', True),
        (3, 2, 'CE-302', True),
        (3, 3, 'CE-303', True),
        (3, 4, 'CE-304', True),
        (3, 5, 'CE-305', True),
        (3, 6, 'CE-306', True),
        (3, 7, 'CE-307', True),
        
        # Semester 4
        (4, 1, 'CE-401', True),
        (4, 2, 'CE-402', True),
        (4, 3, 'CE-403', True),
        (4, 4, 'CE-404', True),
        (4, 5, 'CE-405', True),
        (4, 6, 'CE-406', True),
        (4, 7, 'CE-407', True),
        
        # Semester 5
        (5, 1, 'CE-501', True),
        (5, 2, 'CE-502', True),
        (5, 3, 'CE-503', True),
        (5, 4, 'CE-504', True),
        (5, 5, 'CE-505', True),
        (5, 6, 'CE-506', True),
        (5, 7, 'CE-507', True),
        
        # Semester 6
        (6, 1, 'CE-601', True),
        (6, 2, 'CE-602', True),
        (6, 3, 'CE-603', True),
        (6, 4, 'CE-604', True),
        (6, 5, 'CE-605', True),
        (6, 6, 'CE-606', True),
        (6, 7, None, True),  # Elective placeholder
        
        # Semester 7
        (7, 1, 'CE-701', True),
        (7, 2, 'CE-702', True),
        (7, 3, 'CE-703', True),
        (7, 4, 'CE-704', True),
        (7, 5, 'CE-705', True),
        (7, 6, 'CE-706', True),
        (7, 7, 'CE-707', True),
        
        # Semester 8
        (8, 1, 'CE-801', True),
        (8, 2, 'CE-802', True),
        (8, 3, 'CE-803', True),
        (8, 4, None, True),  # Elective placeholder
        (8, 5, None, True),  # Elective placeholder
    ]
    
    created_count = 0
    for sem, pos, course_code, mandatory in chart_structure:
        # Determine if this should be a specific course or group
        if course_code:
            # Specific required course
            try:
                course = Course.objects.get(code=course_code)
                node, created = ChartNode.objects.get_or_create(
                    schema=schema,
                    semester=sem,
                    position=pos,
                    defaults={
                        'course': course,
                        'is_mandatory': mandatory,
                    }
                )
                if created:
                    created_count += 1
            except Course.DoesNotExist:
                print(f"   ⚠️  Course {course_code} not found for Semester {sem}")
        else:
            # Elective placeholder
            if sem == 6 and pos == 7:
                group = gen_electives
            else:
                group = gen_electives
            
            node, created = ChartNode.objects.get_or_create(
                schema=schema,
                semester=sem,
                position=pos,
                defaults={
                    'course_group': group,
                    'is_mandatory': mandatory,
                }
            )
            if created:
                created_count += 1
    
    print(f"✅ Created {created_count} chart nodes")
    return created_count


def print_summary():
    """Print summary of data"""
    print("\n" + "="*70)
    print("📋 SUMMARY")
    print("="*70)
    
    schemas = ChartSchema.objects.filter(code='CS-BS-92-402')
    courses = Course.objects.filter(code__startswith='CE-')
    groups = CourseGroup.objects.all()
    nodes = ChartNode.objects.all()
    prereqs = Prerequisite.objects.filter(is_corequisite=False)
    coreqs = Prerequisite.objects.filter(is_corequisite=True)
    
    print(f"\n📚 Courses: {courses.count()}")
    print(f"📊 Chart Schemas: {schemas.count()}")
    print(f"🎯 Elective Groups: {groups.count()}")
    print(f"📋 Chart Nodes: {nodes.count()}")
    print(f"🔗 Prerequisites: {prereqs.count()}")
    print(f"⚡ Co-requisites: {coreqs.count()}")


if __name__ == '__main__':
    print("\n🎓 COMPUTER ENGINEERING DEGREE CHART SETUP (PRD 2.2)")
    print("="*70)
    print("Creating ChartSchema with version control and elective groups")
    
    try:
        schema = create_chart_schema()
        tech_electives, gen_electives = create_elective_groups()
        nodes_created = create_chart_structure(schema, tech_electives, gen_electives)
        print_summary()
        
        print("\n" + "="*70)
        print("✅ Chart setup completed successfully!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
