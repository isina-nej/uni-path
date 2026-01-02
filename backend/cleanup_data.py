#!/usr/bin/env python
"""Delete old test data"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unipath.settings')
django.setup()

from django.contrib.auth import get_user_model
from courses.models import Course
from students.models import StudentSelection

User = get_user_model()

print("\n" + "="*70)
print("🗑️  Deleting old test data...")
print("="*70)

# Delete student selections
deleted = StudentSelection.objects.all().delete()
print(f"✅ Deleted {deleted[0]} course selections")

# Delete student users
deleted = User.objects.filter(username__startswith='student_').delete()
print(f"✅ Deleted {deleted[0]} student users")

# Delete courses
deleted = Course.objects.filter(code__startswith='CE-').delete()
print(f"✅ Deleted {deleted[0]} courses")

print("\n" + "="*70)
print("✅ Cleanup complete!")
print("="*70 + "\n")
