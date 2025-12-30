#!/usr/bin/env python3
"""
Mock API Server برای تست Front-end بدون Backend Server
استفاده: python mock_server.py
سرور به صورت پیش‌فرض بر روی http://localhost:5000 اجرا می‌شود
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import urllib.parse
from functools import wraps
import mimetypes

# مسیر فایل Mock Database
MOCK_DB_PATH = os.path.join(os.path.dirname(__file__), 'backend', 'mock_api_db.json')

# Load Mock Data
def load_mock_data():
    if os.path.exists(MOCK_DB_PATH):
        with open(MOCK_DB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Global Mock Data
MOCK_DATA = load_mock_data()

class MockAPIHandler(BaseHTTPRequestHandler):
    """Handler برای Mock API Requests"""
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS, PATCH')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.end_headers()
    
    def send_json_response(self, data, status_code=200):
        """Send JSON response with proper headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        print(f"[{datetime.now()}] GET {path}")
        
        # Login endpoint (mock)
        if path == '/api/auth/login':
            response = {
                "access": "mock_access_token_12345",
                "refresh": "mock_refresh_token_67890",
                "user": MOCK_DATA.get('users', [{}])[0]
            }
            return self.send_json_response(response)
        
        # User profile endpoint
        elif path == '/api/auth/user' or path == '/api/users/profile':
            users = MOCK_DATA.get('users', [])
            if users:
                return self.send_json_response(users[0])
            return self.send_json_response({"error": "User not found"}, 404)
        
        # Courses list
        elif path == '/api/courses':
            courses = MOCK_DATA.get('courses', [])
            return self.send_json_response({"results": courses, "count": len(courses)})
        
        # Specific course
        elif path.startswith('/api/courses/'):
            course_id = path.split('/')[-1]
            courses = MOCK_DATA.get('courses', [])
            course = next((c for c in courses if str(c.get('id')) == course_id), None)
            if course:
                return self.send_json_response(course)
            return self.send_json_response({"error": "Course not found"}, 404)
        
        # Enrollments
        elif path == '/api/enrollments':
            enrollments = MOCK_DATA.get('enrollments', [])
            return self.send_json_response({"results": enrollments, "count": len(enrollments)})
        
        # Grades
        elif path == '/api/grades':
            grades = MOCK_DATA.get('grades', [])
            return self.send_json_response({"results": grades, "count": len(grades)})
        
        # Student specific grades
        elif path.startswith('/api/students/') and path.endswith('/grades'):
            student_id = path.split('/')[3]
            grades = MOCK_DATA.get('grades', [])
            student_grades = [g for g in grades if str(g.get('student')) == student_id]
            return self.send_json_response({"results": student_grades, "count": len(student_grades)})
        
        # Recommendations
        elif path == '/api/recommendations':
            recommendations = MOCK_DATA.get('recommendations', [])
            return self.send_json_response({"results": recommendations, "count": len(recommendations)})
        
        # Statistics
        elif path == '/api/statistics' or path == '/api/students/statistics':
            stats = MOCK_DATA.get('statistics', {})
            return self.send_json_response(stats)
        
        # Students list
        elif path == '/api/students':
            students = MOCK_DATA.get('users', [])
            student_list = [s for s in students if s.get('role') == 'student']
            return self.send_json_response({"results": student_list, "count": len(student_list)})
        
        # Health check
        elif path == '/api/health':
            return self.send_json_response({"status": "ok", "message": "Mock API Server is running"})
        
        # Root
        elif path == '/api':
            return self.send_json_response({
                "message": "Mock API Server",
                "version": "1.0",
                "endpoints": [
                    "/api/health",
                    "/api/auth/login",
                    "/api/auth/user",
                    "/api/users/profile",
                    "/api/courses",
                    "/api/courses/{id}",
                    "/api/enrollments",
                    "/api/grades",
                    "/api/students/{id}/grades",
                    "/api/recommendations",
                    "/api/statistics",
                    "/api/students"
                ]
            })
        
        else:
            return self.send_json_response({"error": "Endpoint not found"}, 404)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        content_length = int(self.headers.get('Content-Length', 0))
        
        try:
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
        except:
            data = {}
        
        print(f"[{datetime.now()}] POST {path}")
        
        # Login endpoint
        if path == '/api/auth/login':
            # Mock login - accept any credentials
            username = data.get('username', 'testuser')
            response = {
                "access": "mock_access_token_12345",
                "refresh": "mock_refresh_token_67890",
                "user": {
                    "id": 1,
                    "username": username,
                    "email": f"{username}@example.com",
                    "first_name": "تست",
                    "last_name": "کاربر",
                    "is_active": True,
                    "role": "student"
                }
            }
            return self.send_json_response(response)
        
        # Register endpoint
        elif path == '/api/auth/register':
            response = {
                "id": 1,
                "username": data.get('username', 'newuser'),
                "email": data.get('email', 'new@example.com'),
                "message": "ثبت‌نام موفق"
            }
            return self.send_json_response(response, 201)
        
        # Refresh token
        elif path == '/api/auth/refresh':
            response = {
                "access": "new_mock_access_token_12345"
            }
            return self.send_json_response(response)
        
        # Enroll in course
        elif path == '/api/enrollments':
            response = {
                "id": 3,
                "student": data.get('student', 1),
                "course": data.get('course', 3),
                "enrolled_at": datetime.now().isoformat() + "Z",
                "status": "active",
                "message": "ثبت‌نام در دوره موفق"
            }
            return self.send_json_response(response, 201)
        
        else:
            return self.send_json_response({"error": "Endpoint not found"}, 404)
    
    def do_PUT(self):
        """Handle PUT requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body) if body else {}
        
        path = self.path
        print(f"[{datetime.now()}] PUT {path}")
        
        # Update profile
        if path.startswith('/api/users/') or path.startswith('/api/students/'):
            response = {
                "id": 1,
                "message": "پروفایل به‌روز شد",
                "data": data
            }
            return self.send_json_response(response)
        
        return self.send_json_response({"error": "Endpoint not found"}, 404)
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def run_mock_server(host='localhost', port=5000):
    """Run the mock API server"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, MockAPIHandler)
    httpd.timeout = 1
    
    print("=" * 60)
    print("🚀 Mock API Server شروع شد")
    print("=" * 60)
    print(f"📡 آدرس سرور: http://{host}:{port}")
    print(f"🌐 برای استفاده موبایل: http://YOUR_IP_ADDRESS:{port}")
    print(f"📱 تست Local: http://localhost:{port}/api")
    print(f"📊 فایل Mock Data: {MOCK_DB_PATH}")
    print("=" * 60)
    print("\n🔗 Endpoints موجود:")
    print("  - GET  /api/health")
    print("  - POST /api/auth/login")
    print("  - GET  /api/auth/user")
    print("  - GET  /api/courses")
    print("  - GET  /api/enrollments")
    print("  - POST /api/enrollments")
    print("  - GET  /api/grades")
    print("  - GET  /api/recommendations")
    print("  - GET  /api/statistics")
    print("\n⚠️  برای توقف، Ctrl+C را فشار دهید\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 سرور متوقف شد")
        httpd.server_close()
    except Exception as e:
        print(f"خطا: {e}")
        httpd.server_close()

if __name__ == '__main__':
    run_mock_server()
