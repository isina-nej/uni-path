#!/usr/bin/env python3
"""
اسکریپت تست برای تمام Endpoints Mock API Server
استفاده: python test_api.py
"""

import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000/api'

class Colors:
    """رنگ‌های Terminal"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(title):
    """چاپ سرصفحه"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}▶  {title}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    """چاپ موفق"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    """چاپ خطا"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_request(method, endpoint):
    """چاپ درخواست"""
    print(f"{Colors.YELLOW}📤 {method} {endpoint}{Colors.RESET}")

def print_response(status_code, data):
    """چاپ پاسخ"""
    if 200 <= status_code < 300:
        color = Colors.GREEN
        icon = "✓"
    else:
        color = Colors.RED
        icon = "✗"
    print(f"{color}{icon} Status: {status_code}{Colors.RESET}")
    print(f"{Colors.BOLD}Response:{Colors.RESET}")
    print(json.dumps(data, indent=2, ensure_ascii=False))

def test_endpoint(method, endpoint, data=None, description=""):
    """تست یک Endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    print_request(method, endpoint)
    if description:
        print(f"📝 {description}")
    
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data)
        elif method == 'PUT':
            response = requests.put(url, json=data)
        else:
            return False
        
        print_response(response.status_code, response.json())
        
        if 200 <= response.status_code < 300:
            print_success(f"{method} {endpoint} - موفق")
            return True
        else:
            print_error(f"{method} {endpoint} - ناموفق")
            return False
    
    except Exception as e:
        print_error(f"خطا: {str(e)}")
        return False

def main():
    """اجرای تمام تست‌ها"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║        تست Mock API Server - Unipath Project         ║")
    print("║                  زمان: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "                 ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    
    results = {
        'passed': 0,
        'failed': 0
    }
    
    # Test 1: Health Check
    print_header("1️⃣  تست سلامتی سرور (Health Check)")
    if test_endpoint('GET', '/health', description="بررسی اینکه سرور فعال است"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 2: Login
    print_header("2️⃣  ورود به سیستم (Login)")
    if test_endpoint('POST', '/auth/login', 
                     {'username': 'testuser', 'password': 'password123'},
                     "ورود با نام‌کاربری و رمز"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 3: User Profile
    print_header("3️⃣  دریافت پروفایل کاربر (User Profile)")
    if test_endpoint('GET', '/auth/user', description="دریافت اطلاعات کاربر جاری"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 4: Get Courses
    print_header("4️⃣  دریافت لیست دروس (Courses List)")
    if test_endpoint('GET', '/courses', description="دریافت تمام دروس"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 5: Get Specific Course
    print_header("5️⃣  دریافت درس خاص (Specific Course)")
    if test_endpoint('GET', '/courses/1', description="دریافت درس با ID=1"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 6: Get Enrollments
    print_header("6️⃣  دریافت ثبت‌نام‌های دانشجو (Enrollments)")
    if test_endpoint('GET', '/enrollments', description="دریافت تمام ثبت‌نام‌ها"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 7: Enroll in Course
    print_header("7️⃣  ثبت‌نام در درس (Enroll)")
    if test_endpoint('POST', '/enrollments',
                     {'student': 1, 'course': 3},
                     "ثبت‌نام دانشجو در درس"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 8: Get Grades
    print_header("8️⃣  دریافت نمرات (Grades)")
    if test_endpoint('GET', '/grades', description="دریافت تمام نمرات"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 9: Get Student Grades
    print_header("9️⃣  دریافت نمرات دانشجو (Student Grades)")
    if test_endpoint('GET', '/students/1/grades', description="دریافت نمرات دانشجوی شماره 1"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 10: Get Recommendations
    print_header("🔟 دریافت توصیه‌های دروس (Recommendations)")
    if test_endpoint('GET', '/recommendations', description="دریافت دروس توصیه‌شده"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 11: Get Statistics
    print_header("1️⃣1️⃣  دریافت آمار دانشجو (Statistics)")
    if test_endpoint('GET', '/statistics', description="دریافت آمار و اطلاعات دانشجو"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 12: Get Students
    print_header("1️⃣2️⃣  دریافت لیست دانشجویان (Students List)")
    if test_endpoint('GET', '/students', description="دریافت تمام دانشجویان"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 13: API Info
    print_header("1️⃣3️⃣  اطلاعات API (API Info)")
    if test_endpoint('GET', '', description="دریافت اطلاعات کلی API"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Final Report
    print_header("📊 گزارش نهایی")
    total = results['passed'] + results['failed']
    percentage = (results['passed'] / total * 100) if total > 0 else 0
    
    print(f"{Colors.GREEN}✓ موفق: {results['passed']}{Colors.RESET}")
    print(f"{Colors.RED}✗ ناموفق: {results['failed']}{Colors.RESET}")
    print(f"{Colors.BLUE}📈 کل تست: {total}{Colors.RESET}")
    print(f"{Colors.BOLD}💯 درصد موفقیت: {percentage:.1f}%{Colors.RESET}\n")
    
    if results['failed'] == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 تمام تست‌ها موفق بودند!{Colors.RESET}\n")
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  تعدادی از تست‌ها ناموفق بودند.{Colors.RESET}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}برنامه متوقف شد{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}خطای کلی: {str(e)}{Colors.RESET}")
