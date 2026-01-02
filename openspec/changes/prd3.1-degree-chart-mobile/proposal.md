# PRD 3.1: Degree Chart Mobile Integration & Smart Course Recommendation
## OpenSpec Proposal

**Issue:** دانشجویان نیازمند درک بصری چارت درسی خود (با توجه به سال ورود و رشته) و سیستم پیشنهاد هوشمند دروس برای ترم بعد هستند.

**Scope:** 
- تشخیص خودکار ChartSchema بر اساس شماره دانشجویی
- نمایش دوگانه: List View (ترم به ترم) و Diagram View (گراف وابستگی‌ها)
- موتور توصیه دروس بر اساس اولویت و پیشنیازها
- رابط کاربری رنگی (سبز=پاس، آبی=مجاز، خاکستری=مسدود، نارنجی=پیشنهادی)

---

## ۱. Problem Analysis

### کاربران موجود
- دانشجویان تصور دقیقی از «کدام دروس در کدام ترم» و «چه ترتیبی» ندارند
- نمی‌دانند که تا کنون کدام درس‌ها پاس داده‌اند و چه دروسی مجاز برای انتخاب هستند
- نیاز به توصیه‌های اولویت‌دار ندارند

### مشکلات فنی موجود
- Flutter app: فقط authenticated user route دارد، درس‌هایی نمایش می‌دهد
- Backend: ChartSchema و ChartNode برای نسخه‌گذاری چارت آماده است
- هیچ API endpoint برای دریافت ChartSchema با پیش‌نیازها وجود ندارد

---

## ۲. Technical Design

### ۲.۱ API Endpoints (Backend)

**GET `/api/degrees/my-chart/`**
- کاربر authenticated را به ChartSchema منطبق متصل کند
- شماره دانشجویی را parse کند: `entry_year = student_id[0:2]`, `major_code = student_id[2:5]`
- Response: ChartSchema + تمام ChartNodes + Prerequisites/Corequisites

```python
{
  "chart": {
    "id": 1,
    "code": "CS-BS-92-402",
    "name": "کامپیوتر - کارشناسی",
    "major": "CS",
    "degree": "12",
    "entry_year_start": 1392,
    "entry_year_end": 1402,
    "total_credits": 132
  },
  "semesters": [
    {
      "number": 1,
      "nodes": [
        {
          "id": 1,
          "position": 1,
          "course": {
            "id": 1,
            "code": "CE-101",
            "name": "فیزیک 1",
            "credits": 3,
            "prerequisites": [],
            "corequisites": [],
            "is_elective": false
          },
          "course_group": null
        },
        // ... elective slots
      ]
    },
    // ... semester 2-8
  ],
  "passed_courses": [1, 5, 7],  // course IDs student passed
  "completed_semesters": 2
}
```

**GET `/api/degrees/recommendations/`**
- دریافت دروس پیشنهادی برای ترم بعد
- بر اساس دروس پاس شده و الگوریتم اولویت‌بندی
- Response: لیست دروس مرتب شده با score و دلیل پیشنهاد

```python
{
  "next_semester": 3,
  "recommendations": [
    {
      "course_id": 15,
      "code": "CE-301",
      "name": "ساختمان‌های داده",
      "credits": 3,
      "priority_score": 95,  // 0-100
      "reason": "پیشنیاز برای 5 درس بعدی",
      "unlocks": [18, 22, 25, 31],  // course IDs
      "prerequisites_met": true,
      "is_mandatory": true
    },
    // ... more courses
  ]
}
```

### ۲.۲ Recommendation Algorithm

```
Score = Base_Weight + Dependency_Weight + Semester_Alignment

Base_Weight = 50
Dependency_Weight = (تعداد دروسی که این درس برای آن‌ها پیشنیاز است) × 10
Semester_Alignment = (درس در ترم انتظار شده است؟) ? 50 : 0

محدود‌کننده:
- اگر پیشنیاز‌های درس پاس نشده > Score = 0 (غیرمجاز)
- اگر درس اختیاری باشد > +20 به score
```

### ۲.۳ Flutter Architecture

**Models:**
```dart
// lib/models/degree_chart.dart
class ChartSchema {
  int id;
  String code;
  String name;
  String major;
  String degree;
  List<Semester> semesters;
  List<int> passedCourses;
  int completedSemesters;
}

class Semester {
  int number;
  List<ChartNode> nodes;
}

class ChartNode {
  int id;
  int position;
  Course? course;
  CourseGroup? courseGroup;
}

class Course {
  int id;
  String code;
  String name;
  int credits;
  List<int> prerequisites;
  List<int> corequisites;
  bool isElective;
}

class CourseRecommendation {
  int courseId;
  String code;
  String name;
  int credits;
  int priorityScore;
  String reason;
  List<int> unlocks;
  bool prerequisitesMet;
  bool isMandatory;
}
```

**Providers (State Management):**
```dart
// lib/providers/degree_chart_provider.dart
class DegreeChartProvider extends ChangeNotifier {
  late ChartSchema chart;
  List<CourseRecommendation> recommendations = [];
  
  Future<void> loadMyChart() async { ... }
  Future<void> loadRecommendations() async { ... }
  void markCoursePassed(int courseId) { ... }
  void markCourseFailed(int courseId) { ... }
}
```

**Screens:**
- `DegreeChartScreen`: دو تب (List View / Diagram View)
- `ListViewTab`: نمایش ترم به ترم
- `DiagramViewTab`: گراف تعاملی با `graphview` package
- `RecommendationsScreen`: دروس پیشنهادی

---

## ۳. Implementation Plan

### Phase 1: Backend (2-3 hours)
- [ ] APIView برای `/api/degrees/my-chart/`
- [ ] APIView برای `/api/degrees/recommendations/`
- [ ] Serializers برای ChartSchema, ChartNode, Course
- [ ] Recommendation algorithm

### Phase 2: Frontend (4-5 hours)
- [ ] Models و Providers
- [ ] API service integration
- [ ] List View UI
- [ ] Diagram View UI (graphview)
- [ ] Recommendations UI
- [ ] Color coding & interactions

### Phase 3: Testing & Polish (2 hours)
- [ ] Integration tests
- [ ] UI/UX testing
- [ ] Performance optimization

---

## ۴. Success Criteria

1. ✅ دانشجو با ورود، ChartSchema منطبق خود را بدون خطا می‌بیند
2. ✅ لیست view: دروس به ترتیب ترم‌ها (۱-۸) نمایش داده می‌شوند
3. ✅ Diagram view: گراف تعاملی با کلیک روی درس، پیشنیازها تغییر رنگ می‌دهند
4. ✅ Recommendations: دروس مرتب شده با score و دلیل پیشنهاد
5. ✅ رنگ‌بندی: سبز (پاس)، آبی (مجاز)، خاکستری (مسدود)، نارنجی (پیشنهادی)

---

## ۵. Risks & Mitigation

| ریسک | احتمال | تاثیر | راه حل |
|------|-------|--------|--------|
| شماره‌های خاص (مهمان/انتقالی) | متوسط | کم | دستی selection |
| عملکرد گراف برای ۵۵ نود | کم | زیاد | Lazy loading + caching |
| تغییرات دروس از سمت ادمین | کم | متوسط | Cache invalidation |

---

## ۶. File Structure

```
backend/
  courses/
    views_chart.py (NEW)
    serializers_chart.py (NEW)
    
lib/
  models/
    degree_chart.dart (NEW)
    course_recommendation.dart (NEW)
  
  providers/
    degree_chart_provider.dart (NEW)
    recommendation_provider.dart (NEW)
  
  screens/
    degree_chart_screen.dart (NEW)
    list_view_tab.dart (NEW)
    diagram_view_tab.dart (NEW)
    recommendations_screen.dart (NEW)
  
  widgets/
    course_tile.dart (NEW)
    semester_section.dart (NEW)
    graph_node.dart (NEW)
```
