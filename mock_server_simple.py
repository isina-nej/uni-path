#!/usr/bin/env python3
"""
Mock API Server برای تست Front-end بدون Backend Server
استفاده: python mock_server_simple.py
سرور به صورت پیش‌فرض بر روی http://localhost:5000 اجرا می‌شود
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import urllib.parse

# Load Mock Data
def load_mock_data():
    db_path = os.path.join(os.path.dirname(__file__), 'backend', 'mock_api_db.json')
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

MOCK_DATA = load_mock_data()

class MockAPIHandler(BaseHTTPRequestHandler):
    """Handler برای Mock API Requests"""
    
    def send_json_response(self, data, status_code=200):
        """Send JSON response with proper headers"""
        response_body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Content-Length', str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        path = self.path.split('?')[0]  # Remove query params
        
        # Health check
        if path == '/api/health' or path == '/api':
            return self.send_json_response({
                "status": "ok",
                "message": "Mock API Server is running",
                "version": "1.0"
            })
        
        # User endpoints
        elif path == '/api/auth/user' or path == '/api/users/profile':
            users = MOCK_DATA.get('users', [])
            if users:
                return self.send_json_response(users[0])
            return self.send_json_response({"error": "Not found"}, 404)
        
        # Courses
        elif path == '/api/courses':
            courses = MOCK_DATA.get('courses', [])
            return self.send_json_response({
                "results": courses,
                "count": len(courses)
            })
        
        elif path.startswith('/api/courses/'):
            course_id = path.split('/')[-1]
            courses = MOCK_DATA.get('courses', [])
            course = next((c for c in courses if str(c.get('id')) == course_id), None)
            if course:
                return self.send_json_response(course)
            return self.send_json_response({"error": "Not found"}, 404)
        
        # Enrollments
        elif path == '/api/enrollments':
            enrollments = MOCK_DATA.get('enrollments', [])
            return self.send_json_response({
                "results": enrollments,
                "count": len(enrollments)
            })
        
        # Grades
        elif path == '/api/grades':
            grades = MOCK_DATA.get('grades', [])
            return self.send_json_response({
                "results": grades,
                "count": len(grades)
            })
        
        elif path.startswith('/api/students/') and path.endswith('/grades'):
            student_id = path.split('/')[3]
            grades = MOCK_DATA.get('grades', [])
            student_grades = [g for g in grades if str(g.get('student')) == student_id]
            return self.send_json_response({
                "results": student_grades,
                "count": len(student_grades)
            })
        
        # Recommendations
        elif path == '/api/recommendations':
            recommendations = MOCK_DATA.get('recommendations', [])
            return self.send_json_response({
                "results": recommendations,
                "count": len(recommendations)
            })
        
        # Statistics
        elif path == '/api/statistics' or path == '/api/students/statistics':
            stats = MOCK_DATA.get('statistics', {})
            return self.send_json_response(stats)
        
        # Students
        elif path == '/api/students':
            students = MOCK_DATA.get('users', [])
            student_list = [s for s in students if s.get('role') == 'student']
            return self.send_json_response({
                "results": student_list,
                "count": len(student_list)
            })
        
        else:
            return self.send_json_response({
                "error": "Endpoint not found",
                "path": path
            }, 404)
    
    def do_POST(self):
        """Handle POST requests"""
        path = self.path.split('?')[0]
        content_length = int(self.headers.get('Content-Length', 0))
        
        try:
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
        except:
            data = {}
        
        # Login
        if path == '/api/auth/login':
            return self.send_json_response({
                "access": "mock_token_" + str(datetime.now().timestamp()),
                "refresh": "mock_refresh_token",
                "user": {
                    "id": 1,
                    "username": data.get('username', 'testuser'),
                    "email": "test@example.com",
                    "first_name": "تست",
                    "last_name": "کاربر"
                }
            })
        
        # Register
        elif path == '/api/auth/register':
            return self.send_json_response({
                "id": 1,
                "username": data.get('username'),
                "email": data.get('email'),
                "message": "ثبت‌نام موفق"
            }, 201)
        
        # Refresh token
        elif path == '/api/auth/refresh':
            return self.send_json_response({
                "access": "new_mock_token_" + str(datetime.now().timestamp())
            })
        
        # Enrollments
        elif path == '/api/enrollments':
            return self.send_json_response({
                "id": 3,
                "student": data.get('student'),
                "course": data.get('course'),
                "status": "active",
                "message": "ثبت‌نام موفق"
            }, 201)
        
        else:
            return self.send_json_response({"error": "Not found"}, 404)
    
    def do_PUT(self):
        """Handle PUT requests"""
        path = self.path.split('?')[0]
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body) if body else {}
        
        return self.send_json_response({
            "message": "به‌روز شد",
            "data": data
        })
    
    def log_message(self, format, *args):
        """Suppress logs"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {self.client_address[0]} - {format % args}")

def main():
    """Main function"""
    port = 8001  # تغییر به پورت دیگری
    server = HTTPServer(('0.0.0.0', port), MockAPIHandler)
    
    print("\n" + "="*60)
    print("🚀 Mock API Server شروع شد")
    print("="*60)
    print(f"📡 آدرس Local: http://localhost:{port}")
    print(f"📡 آدرس شبکه: http://0.0.0.0:{port}")
    print(f"📱 تست: curl http://localhost:{port}/api/health")
    print("⚠️  برای توقف: Ctrl+C")
    print("="*60 + "\n")
    sys.stdout.flush()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 سرور متوقف شد")
        server.server_close()
        sys.exit(0)
    except Exception as e:
        print(f"خطا: {e}")
        server.server_close()
        sys.exit(1)

if __name__ == '__main__':
    main()

