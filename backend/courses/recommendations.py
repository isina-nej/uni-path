"""
Course Recommendation Engine

بر اساس PRD-2.4:
1. امتیاز برای هر درس بر اساس تعداد دروس وابسته (تعدیل درجات)
2. فیلتر کردن بر اساس پیش‌نیازها
3. ترتیب بر اساس امتیاز و اهمیت
4. بررسی دورهای وابستگی (Cycle Detection)
"""

from typing import List, Dict, Set, Tuple
from django.db.models import Count, Q
from courses.models import Course, Prerequisite, ChartCourse
from students.models import StudentCourseHistory, StudentSelection


class RecommendationEngine:
    """
    محرک توصیه‌های دروس برای دانشجویان.
    
    الگوریتم:
    1. بازسازی گراف وابستگی‌ها
    2. محاسبه Importance Score برای هر درس
    3. فیلتر کردن پیش‌نیازها
    4. مرتب‌سازی نهایی
    5. محدود کردن نتایج
    """
    
    def __init__(self, student, degree_chart):
        self.student = student
        self.degree_chart = degree_chart
        self._dependency_cache = {}
        self._visited = set()
    
    def get_recommendations(self, semester: str, limit: int = 10) -> List[Dict]:
        """
        دریافت توصیه‌های دروسی برای دانشجو.
        
        Args:
            semester: نام ترم (مثال: 'Spring 1403')
            limit: حداکثر تعداد توصیه‌ها
        
        Returns:
            لیستی از دروس توصیه‌شده با امتیازات
        """
        
        # 1. دریافت دروسی که دانشجو قبلاً پاس کرده است
        passed_courses = self._get_passed_courses()
        
        # 2. دریافت دروسی که انتخاب کرده است
        selected_courses = self._get_selected_courses(semester)
        
        # 3. دریافت دروس شروع (بدون پیش‌نیاز)
        available_courses = self._get_available_courses(
            passed_courses,
            selected_courses
        )
        
        # 4. محاسبه امتیاز برای هر درس
        scored_courses = []
        for course in available_courses:
            score = self._calculate_importance_score(course, available_courses)
            scored_courses.append({
                'course': course,
                'score': score,
                'importance': course.chartcourse_set.filter(
                    degree_chart=self.degree_chart
                ).first().importance_score if hasattr(course, 'chartcourse_set') else 0
            })
        
        # 5. مرتب‌سازی بر اساس امتیاز
        scored_courses.sort(
            key=lambda x: (-x['score'], -x['importance']),
            reverse=False
        )
        
        # 6. برگرداندن نتایج محدود
        recommendations = []
        for item in scored_courses[:limit]:
            recommendations.append({
                'id': item['course'].id,
                'code': item['course'].code,
                'name': item['course'].name,
                'credits': item['course'].credits,
                'unit_type': item['course'].unit_type,
                'instructor': item['course'].instructor,
                'importance_score': item['score'],
                'description': item['course'].description,
                'start_time': str(item['course'].start_time) if item['course'].start_time else None,
                'end_time': str(item['course'].end_time) if item['course'].end_time else None,
            })
        
        return recommendations
    
    def _get_passed_courses(self) -> Set[int]:
        """دریافت شناسه‌های دروسی که دانشجو پاس کرده است"""
        passed = StudentCourseHistory.objects.filter(
            student=self.student,
            is_passed=True
        ).values_list('course_id', flat=True)
        return set(passed)
    
    def _get_selected_courses(self, semester: str) -> Set[int]:
        """دریافت شناسه‌های دروسی که دانشجو برای ترم انتخاب کرده است"""
        selected = StudentSelection.objects.filter(
            student=self.student,
            semester=semester
        ).values_list('course_id', flat=True)
        return set(selected)
    
    def _get_available_courses(
        self,
        passed_courses: Set[int],
        selected_courses: Set[int]
    ) -> List[Course]:
        """
        دریافت دروسی که دانشجو می‌تواند انتخاب کند
        (پیش‌نیازهای آن پاس شده‌اند و انتخاب نشده‌اند)
        """
        
        # دریافت تمام دروسی که در این نمودار درجات هستند
        chart_courses = ChartCourse.objects.filter(
            degree_chart=self.degree_chart
        ).values_list('course_id', flat=True)
        
        available = []
        
        for course_id in chart_courses:
            # اگر قبلاً انتخاب شده، نادیده بگیر
            if course_id in selected_courses:
                continue
            
            course = Course.objects.get(id=course_id)
            
            # بررسی پیش‌نیازها
            if self._check_prerequisites(course, passed_courses):
                available.append(course)
        
        return available
    
    def _check_prerequisites(
        self,
        course: Course,
        passed_courses: Set[int]
    ) -> bool:
        """
        بررسی اینکه دانشجو پیش‌نیازهای یک درس را پاس کرده است
        """
        prerequisites = Prerequisite.objects.filter(course=course)
        
        for prereq in prerequisites:
            # اگر corequisite است، اگر فعلاً انجام شود قابل قبول است
            if prereq.is_corequisite:
                continue
            
            # پیش‌نیاز باید پاس شده باشد
            if prereq.prerequisite_course_id not in passed_courses:
                return False
        
        return True
    
    def _calculate_importance_score(
        self,
        course: Course,
        available_courses: List[Course]
    ) -> int:
        """
        محاسبه امتیاز اهمیت یک درس
        
        Score = تعداد دروسی که این درس پیش‌نیاز آن‌ها هستند
        
        منطق:
        - هر درسی که بیشتر دروس دیگر به آن وابسته‌اند، اهمیت بیشتری دارد
        - دروسی که پایه‌ای‌تر هستند (بیشتر دروس به آن‌ها بستگی دارند) پیشنهاد داده می‌شوند
        """
        
        # تعداد دروسی که این درس برای آن‌ها پیش‌نیاز است
        direct_dependents = Prerequisite.objects.filter(
            prerequisite_course=course,
            is_corequisite=False
        ).count()
        
        # تعداد دروسی که بطور غیرمستقیم به این درس وابسته‌اند
        indirect_dependents = self._count_indirect_dependents(course, available_courses)
        
        # امتیاز نهایی: مستقیم + غیرمستقیم
        return direct_dependents + indirect_dependents
    
    def _count_indirect_dependents(
        self,
        course: Course,
        available_courses: List[Course]
    ) -> int:
        """
        محاسبه تعداد دروسی که بطور غیرمستقیم به یک درس وابسته‌اند
        
        مثال:
        اگر A → B → C
        C برای B پیش‌نیاز است
        B برای A پیش‌نیاز است
        درنتیجه A به C وابسته است (غیرمستقیم)
        """
        
        # از حداقل 1 استفاده کن تا از دروسی که پایه‌ای نیستند اجتناب شود
        count = 0
        available_ids = {c.id for c in available_courses}
        
        # دروسی که مستقیماً به این درس وابسته‌اند
        direct = Prerequisite.objects.filter(
            prerequisite_course=course,
            is_corequisite=False
        ).values_list('course_id', flat=True)
        
        for dependent_id in direct:
            if dependent_id in available_ids:
                count += 1
        
        return count
    
    def detect_circular_dependencies(self) -> List[Tuple[int, int]]:
        """
        تشخیص دورهای وابستگی در سیستم
        
        Returns:
            لیستی از (course_id, prerequisite_id) هایی که دور تشکیل می‌دهند
        """
        
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node: int, path: Set[int]) -> bool:
            visited.add(node)
            path.add(node)
            
            # دریافت دروسی که این درس برای آن‌ها پیش‌نیاز است
            dependents = Prerequisite.objects.filter(
                prerequisite_course_id=node,
                is_corequisite=False
            ).values_list('course_id', flat=True)
            
            for dependent in dependents:
                if dependent not in visited:
                    if dfs(dependent, path):
                        return True
                elif dependent in path:
                    # دور پیدا شد
                    cycles.append((node, dependent))
                    return True
            
            path.remove(node)
            return False
        
        # شروع DFS از هر درس
        for course in Course.objects.all():
            if course.id not in visited:
                dfs(course.id, set())
        
        return cycles
