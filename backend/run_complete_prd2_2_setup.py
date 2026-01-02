#!/usr/bin/env python
"""
Complete PRD 2.2 Setup - Run Both Course Creation and Chart Schema Setup
This script runs both create_degree_chart_v2.py and setup_chart_schema.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unipath.settings')
django.setup()

from django.core.management import call_command
import subprocess

print("\n" + "="*70)
print("🎓 PRD 2.2 COMPLETE SETUP")
print("="*70)

# Step 1: Create courses
print("\n" + "="*70)
print("Step 1: Creating 55 Computer Engineering Courses...")
print("="*70)

try:
    subprocess.run([sys.executable, 'create_degree_chart_v2.py'], check=True)
    print("✅ Courses created successfully")
except subprocess.CalledProcessError as e:
    print(f"❌ Failed to create courses: {e}")
    sys.exit(1)

# Step 2: Setup chart schema
print("\n" + "="*70)
print("Step 2: Setting up Chart Schema with Electives...")
print("="*70)

try:
    subprocess.run([sys.executable, 'setup_chart_schema.py'], check=True)
    print("✅ Chart schema setup completed")
except subprocess.CalledProcessError as e:
    print(f"❌ Failed to setup chart schema: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("✅ PRD 2.2 SETUP COMPLETE!")
print("="*70)

print("\n📋 Next Steps:")
print("1. Go to PythonAnywhere Web app dashboard")
print("2. Click 'Reload' button")
print("3. Test in browser: https://isinanej.pythonanywhere.com/admin/courses/chartschema/")
print("4. Verify all courses, groups, and chart nodes are present")

print("\n" + "="*70)
