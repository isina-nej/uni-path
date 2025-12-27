"""
Integration tests for Student APIs and Recommendation Engine

Tests for:
1. Student course history operations
2. Course selection workflow
3. Schedule management and conflict detection
4. Recommendation algorithm accuracy
"""

import json
from datetime import time
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from courses.models import Course, DegreeChart, ChartCourse, Prerequisite
from students.models import StudentCourseHistory, StudentSelection, Schedule
from courses.recommendations import RecommendationEngine

User = get_user_model()


class StudentWorkflowIntegrationTest(APITestCase):
    """Integration tests for complete student workflow"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create users
        self.student = User.objects.create_user(
            username='student1',
            email='student@test.com',
            password='testpass123',
            role='student'
        )
        
        self.admin = User.objects.create_user(
            username='admin1',
            email='admin@test.com',
            password='testpass123',
            role='admin'
        )
        
        # Create degree chart
        self.degree_chart = DegreeChart.objects.create(
            name='Computer Science',
            code='CS',
            department='Engineering',
            total_credits=120
        )
        
        # Create courses
        self.course1 = Course.objects.create(
            code='CS101',
            name='Introduction to Programming',
            credits=3,
            unit_type='theoretical',
            instructor='Dr. Smith',
            semester=1,
            is_mandatory=True,
            is_offered=True,
            capacity=30
        )
        
        self.course2 = Course.objects.create(
            code='CS201',
            name='Object-Oriented Programming',
            credits=3,
            unit_type='theoretical',
            instructor='Dr. Jones',
            semester=2,
            is_mandatory=True,
            is_offered=True,
            capacity=25
        )
        
        # Add courses to degree chart
        ChartCourse.objects.create(
            degree_chart=self.degree_chart,
            course=self.course1,
            is_mandatory=True,
            recommended_semester=1
        )
        ChartCourse.objects.create(
            degree_chart=self.degree_chart,
            course=self.course2,
            is_mandatory=True,
            recommended_semester=2
        )
        
        # Create prerequisite
        Prerequisite.objects.create(
            course=self.course2,
            prerequisite_course=self.course1
        )
    
    def test_student_full_workflow(self):
        """Test complete student workflow: login -> select -> schedule -> get recommendations"""
        
        # 1. Student login
        login_response = self.client.post('/api/auth/login/', {
            'username': 'student1',
            'password': 'testpass123'
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # 2. Student marks first course as passed
        history = StudentCourseHistory.objects.create(
            student=self.student,
            course=self.course1,
            grade='A',
            grade_points=4.0,
            credits_earned=3,
            semester='Fall 1402',
            is_passed=True
        )
        self.assertIsNotNone(history.id)
        
        # 3. Student selects CS201 (now available since CS101 is passed)
        selection = StudentSelection.objects.create(
            student=self.student,
            course=self.course2,
            semester='Spring 1403'
        )
        self.assertFalse(selection.is_confirmed)
        
        # 4. Student gets schedule conflict data
        schedule1 = Schedule.objects.create(
            student=self.student,
            course=self.course2,
            day_of_week=0,  # Saturday
            start_time='08:00',
            end_time='09:30',
            location='Room 101',
            semester='Spring 1403'
        )
        self.assertFalse(schedule1.has_conflict)
        
        # 5. Get recommendations
        engine = RecommendationEngine(self.student, self.degree_chart)
        recommendations = engine.get_recommendations('Spring 1403', limit=5)
        
        # CS201 should NOT be in recommendations (already selected)
        rec_ids = [r['id'] for r in recommendations]
        self.assertNotIn(self.course2.id, rec_ids)
    
    def test_permission_student_own_data_only(self):
        """Test that students can only see their own data"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_student_token()}')
        
        # Create history for another student
        other_student = User.objects.create_user(
            username='student2',
            email='student2@test.com',
            password='testpass123',
            role='student'
        )
        StudentCourseHistory.objects.create(
            student=other_student,
            course=self.course1,
            grade='B',
            semester='Fall 1402',
            is_passed=True
        )
        
        # Current student should not see other's history
        response = self.client.get('/api/students/history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should be empty for this student
        history_count = len(response.data)
        self.assertEqual(history_count, 0)
    
    def test_admin_full_access(self):
        """Test that admins can access all student data"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_admin_token()}')
        
        # Admin can access all history
        response = self.client.get('/api/students/history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def get_student_token(self):
        """Get JWT token for student"""
        response = self.client.post('/api/auth/login/', {
            'username': 'student1',
            'password': 'testpass123'
        })
        return response.data['access']
    
    def get_admin_token(self):
        """Get JWT token for admin"""
        response = self.client.post('/api/auth/login/', {
            'username': 'admin1',
            'password': 'testpass123'
        })
        return response.data['access']


class RecommendationEngineTest(TestCase):
    """Unit tests for recommendation engine"""
    
    def setUp(self):
        """Set up test data"""
        self.student = User.objects.create_user(
            username='test_student',
            email='test@test.com',
            password='testpass',
            role='student'
        )
        
        self.degree_chart = DegreeChart.objects.create(
            name='CS',
            code='CS',
            department='Engineering',
            total_credits=120
        )
        
        # Create course hierarchy:
        # CS101 (no prereq)
        #   ├─ CS201 (prereq: CS101)
        #   └─ CS202 (prereq: CS101)
        #       ├─ CS301 (prereq: CS202)
        #       └─ CS302 (prereq: CS202)
        
        self.cs101 = Course.objects.create(
            code='CS101', name='Intro', credits=3,
            unit_type='theoretical', instructor='Dr.A',
            semester=1, is_offered=True, capacity=30
        )
        self.cs201 = Course.objects.create(
            code='CS201', name='OOP', credits=3,
            unit_type='theoretical', instructor='Dr.B',
            semester=2, is_offered=True, capacity=30
        )
        self.cs202 = Course.objects.create(
            code='CS202', name='Data Structures', credits=3,
            unit_type='theoretical', instructor='Dr.C',
            semester=2, is_offered=True, capacity=30
        )
        self.cs301 = Course.objects.create(
            code='CS301', name='Algorithms', credits=3,
            unit_type='theoretical', instructor='Dr.D',
            semester=3, is_offered=True, capacity=30
        )
        self.cs302 = Course.objects.create(
            code='CS302', name='Database', credits=3,
            unit_type='theoretical', instructor='Dr.E',
            semester=3, is_offered=True, capacity=30
        )
        
        # Add to degree chart
        for course in [self.cs101, self.cs201, self.cs202, self.cs301, self.cs302]:
            ChartCourse.objects.create(
                degree_chart=self.degree_chart,
                course=course,
                is_mandatory=True
            )
        
        # Create prerequisites
        Prerequisite.objects.create(
            course=self.cs201,
            prerequisite_course=self.cs101
        )
        Prerequisite.objects.create(
            course=self.cs202,
            prerequisite_course=self.cs101
        )
        Prerequisite.objects.create(
            course=self.cs301,
            prerequisite_course=self.cs202
        )
        Prerequisite.objects.create(
            course=self.cs302,
            prerequisite_course=self.cs202
        )
    
    def test_recommendation_without_prerequisites(self):
        """Test that only CS101 is recommended when no prerequisites are met"""
        engine = RecommendationEngine(self.student, self.degree_chart)
        recommendations = engine.get_recommendations('Spring 1403', limit=5)
        
        # Should only recommend CS101 (no prerequisites)
        rec_codes = [r['code'] for r in recommendations]
        self.assertIn('CS101', rec_codes)
        self.assertNotIn('CS201', rec_codes)
        self.assertNotIn('CS202', rec_codes)
    
    def test_recommendation_with_prerequisites(self):
        """Test recommendations after completing CS101"""
        # Mark CS101 as passed
        StudentCourseHistory.objects.create(
            student=self.student,
            course=self.cs101,
            grade='A',
            grade_points=4.0,
            credits_earned=3,
            semester='Fall 1402',
            is_passed=True
        )
        
        engine = RecommendationEngine(self.student, self.degree_chart)
        recommendations = engine.get_recommendations('Spring 1403', limit=5)
        
        # Should recommend CS201 and CS202 (their only prereq is CS101)
        rec_codes = [r['code'] for r in recommendations]
        self.assertIn('CS201', rec_codes)
        self.assertIn('CS202', rec_codes)
        self.assertNotIn('CS301', rec_codes)  # Requires CS202
    
    def test_importance_score_calculation(self):
        """Test that importance score correctly weights courses"""
        engine = RecommendationEngine(self.student, self.degree_chart)
        
        # CS101 should have higher importance (2 dependents: CS201, CS202)
        cs101_score = engine._calculate_importance_score(
            self.cs101,
            [self.cs101, self.cs201, self.cs202, self.cs301, self.cs302]
        )
        
        # CS201 should have lower importance (0 dependents)
        cs201_score = engine._calculate_importance_score(
            self.cs201,
            [self.cs101, self.cs201, self.cs202, self.cs301, self.cs302]
        )
        
        self.assertGreater(cs101_score, cs201_score)
    
    def test_exclude_already_selected(self):
        """Test that already-selected courses are not recommended"""
        # Select CS101
        StudentSelection.objects.create(
            student=self.student,
            course=self.cs101,
            semester='Spring 1403'
        )
        
        engine = RecommendationEngine(self.student, self.degree_chart)
        recommendations = engine.get_recommendations('Spring 1403', limit=5)
        
        rec_ids = [r['id'] for r in recommendations]
        self.assertNotIn(self.cs101.id, rec_ids)
    
    def test_circular_dependency_detection(self):
        """Test circular dependency detection"""
        # Create circular dependency
        Prerequisite.objects.create(
            course=self.cs101,
            prerequisite_course=self.cs301
        )
        
        engine = RecommendationEngine(self.student, self.degree_chart)
        cycles = engine.detect_circular_dependencies()
        
        # Should detect cycle
        self.assertGreater(len(cycles), 0)


class ScheduleConflictTest(TestCase):
    """Tests for schedule conflict detection"""
    
    def setUp(self):
        """Set up test data"""
        self.student = User.objects.create_user(
            username='test',
            email='test@test.com',
            password='pass',
            role='student'
        )
        
        self.course1 = Course.objects.create(
            code='CS101', name='Intro', credits=3,
            unit_type='theoretical', instructor='Dr.A',
            semester=1, is_offered=True, capacity=30
        )
        
        self.course2 = Course.objects.create(
            code='CS201', name='OOP', credits=3,
            unit_type='theoretical', instructor='Dr.B',
            semester=1, is_offered=True, capacity=30
        )
    
    def test_no_conflict_different_times(self):
        """Test no conflict with non-overlapping times"""
        schedule1 = Schedule.objects.create(
            student=self.student,
            course=self.course1,
            day_of_week=0,
            start_time=time(8, 0),
            end_time=time(9, 30),
            semester='Spring 1403'
        )
        
        schedule2 = Schedule.objects.create(
            student=self.student,
            course=self.course2,
            day_of_week=0,
            start_time=time(10, 0),
            end_time=time(11, 30),
            semester='Spring 1403'
        )
        
        self.assertFalse(schedule1.has_conflict)
        self.assertFalse(schedule2.has_conflict)
    
    def test_conflict_overlapping_times(self):
        """Test conflict with overlapping times"""
        schedule1 = Schedule.objects.create(
            student=self.student,
            course=self.course1,
            day_of_week=0,
            start_time=time(8, 0),
            end_time=time(9, 30),
            semester='Spring 1403'
        )
        
        schedule2 = Schedule.objects.create(
            student=self.student,
            course=self.course2,
            day_of_week=0,
            start_time=time(9, 0),
            end_time=time(10, 30),
            semester='Spring 1403'
        )
        
        self.assertTrue(schedule1.has_conflict)
        self.assertTrue(schedule2.has_conflict)
    
    def test_no_conflict_different_days(self):
        """Test no conflict with same time but different days"""
        schedule1 = Schedule.objects.create(
            student=self.student,
            course=self.course1,
            day_of_week=0,  # Saturday
            start_time=time(8, 0),
            end_time=time(9, 30),
            semester='Spring 1403'
        )
        
        schedule2 = Schedule.objects.create(
            student=self.student,
            course=self.course2,
            day_of_week=1,  # Sunday
            start_time=time(8, 0),
            end_time=time(9, 30),
            semester='Spring 1403'
        )
        
        self.assertFalse(schedule1.has_conflict)
        self.assertFalse(schedule2.has_conflict)
