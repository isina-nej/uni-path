#!/usr/bin/env python
"""
Clean up all old course and degree chart data
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unipath.settings')
django.setup()

from courses.models import Course, DegreeChart, ChartCourse, Prerequisite
from students.models import StudentSelection

print("\n" + "="*70)
print("🧹 Cleaning up old data...")
print("="*70)

# Delete in order to avoid foreign key issues
selections_deleted, _ = StudentSelection.objects.all().delete()
print(f"✅ Deleted {selections_deleted} student selections")

chart_courses_deleted, _ = ChartCourse.objects.all().delete()
print(f"✅ Deleted {chart_courses_deleted} chart courses")

prereqs_deleted, _ = Prerequisite.objects.all().delete()
print(f"✅ Deleted {prereqs_deleted} prerequisites")

charts_deleted, _ = DegreeChart.objects.all().delete()
print(f"✅ Deleted {charts_deleted} degree charts")

courses_deleted, _ = Course.objects.all().delete()
print(f"✅ Deleted {courses_deleted} courses")

print("\n" + "="*70)
print("✅ Cleanup completed!")
print("="*70 + "\n")
