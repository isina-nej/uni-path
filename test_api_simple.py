#!/usr/bin/env python3
"""
اسکریپت تست برای تمام Endpoints Mock API Server
"""

import requests
import json
from datetime import datetime
import time

BASE_URL = 'http://localhost:8001/api'
TIMEOUT = 5

def print_header(title):
    print(f"\n{'='*60}")
    print(f"▶  {title}")
    print(f"{'='*60}\n")

def print_success(text):
    print(f"✓ {text}")

def print_error(text):
    print(f"✗ {text}")

def test_endpoint(method, endpoint, data=None):
    """تست یک Endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"📤 {method} {endpoint}")
    
    try:
        if method == 'GET':
            response = requests.get(url, timeout=TIMEOUT)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=TIMEOUT)
        else:
            return False
        
        print(f"✓ Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)[:200]}...")
        
        return 200 <= response.status_code < 300
    
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def main():
    """اجرای تست‌ها"""
    print(f"\n╔{'='*58}╗")
    print(f"║  تست Mock API Server - Unipath Project            ║")
    print(f"║  زمان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):38s}  ║")
    print(f"╚{'='*58}╝\n")
    
    results = {'passed': 0, 'failed': 0}
    
    tests = [
        ('GET', '/health', None, "سلامتی سرور"),
        ('POST', '/auth/login', {'username': 'test', 'password': 'pass'}, "ورود"),
        ('GET', '/auth/user', None, "پروفایل"),
        ('GET', '/courses', None, "دروس"),
        ('GET', '/courses/1', None, "درس خاص"),
        ('GET', '/enrollments', None, "ثبت‌نام‌ها"),
        ('POST', '/enrollments', {'student': 1, 'course': 3}, "ثبت‌نام جدید"),
        ('GET', '/grades', None, "نمرات"),
        ('GET', '/students/1/grades', None, "نمرات دانشجو"),
        ('GET', '/recommendations', None, "توصیه‌ها"),
        ('GET', '/statistics', None, "آمار"),
        ('GET', '/students', None, "دانشجویان"),
    ]
    
    for i, (method, endpoint, data, desc) in enumerate(tests, 1):
        print_header(f"{i}️⃣  {desc}")
        if test_endpoint(method, endpoint, data):
            results['passed'] += 1
        else:
            results['failed'] += 1
        time.sleep(0.5)
    
    # Report
    print_header("📊 گزارش نهایی")
    total = results['passed'] + results['failed']
    pct = (results['passed'] / total * 100) if total > 0 else 0
    
    print(f"✓ موفق: {results['passed']}")
    print(f"✗ ناموفق: {results['failed']}")
    print(f"💯 درصد: {pct:.1f}%\n")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
