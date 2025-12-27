# Change Proposal: Student API System

**Author:** System  
**Date:** 2025-12-27  
**Status:** In Progress  
**Priority:** High  
**Effort:** 8 hours

## Summary

Complete implementation of student-facing API endpoints for course selection, history tracking, schedule management, and intelligent course recommendations. This proposal includes building three ViewSets for student operations and an advanced recommendation engine using dependency-based scoring.

## Requirements

### FR-14: Student Course History API
**Requirement:** Track and retrieve student's past course performance

**API Endpoints:**
- `GET /api/students/history/` - List student's course history (filtered by semester, passed status)
- `POST /api/students/history/` - Add course to history (admin only)
- `PUT /api/students/history/{id}/` - Update history entry (admin)
- `GET /api/students/history/passed_courses/` - Get all passed courses
- `GET /api/students/history/statistics/` - Get GPA, credits, course counts

**Data Structure:**
```
StudentCourseHistory:
- student: ForeignKey(User)
- course: ForeignKey(Course)
- grade: 'A' | 'B+' | 'B' | 'C+' | 'C' | 'D+' | 'D' | 'F'
- grade_points: Decimal (0.0 - 4.0)
- credits_earned: Integer
- semester: String (e.g., "Spring 1403")
- is_passed: Boolean
- notes: Text (optional)
```

**Permissions:**
- Students: Read-only their own history
- Admins: Full CRUD for all students

### FR-15: Student Course Selection API
**Requirement:** Allow students to select courses for upcoming semesters

**API Endpoints:**
- `GET /api/students/selections/` - List current selections
- `POST /api/students/selections/` - Select a course
- `DELETE /api/students/selections/{id}/` - Remove selection
- `POST /api/students/selections/confirm_selections/` - Confirm all selections for semester

**Data Structure:**
```
StudentSelection:
- student: ForeignKey(User)
- course: ForeignKey(Course)
- semester: String (e.g., "Spring 1403")
- selected_at: DateTime (auto_now_add)
- is_confirmed: Boolean (default=False)
- confirmed_at: DateTime (nullable)
- notes: Text (optional)
```

**Permissions:**
- Students: Can select/modify their own selections
- Admins: Full CRUD for all students

### FR-16: Student Schedule API
**Requirement:** Manage and view student weekly schedules with conflict detection

**API Endpoints:**
- `GET /api/students/schedule/` - Get student's schedule
- `POST /api/students/schedule/` - Create schedule entry
- `GET /api/students/schedule/conflicts/` - Get all scheduling conflicts
- `DELETE /api/students/schedule/{id}/` - Remove from schedule

**Data Structure:**
```
Schedule:
- student: ForeignKey(User)
- course: ForeignKey(Course)
- day_of_week: Integer (0=Saturday ... 4=Wednesday, 5=Thursday)
- start_time: TimeField
- end_time: TimeField
- location: String
- semester: String

Property: has_conflict - Detects overlapping times on same day
```

**Permissions:**
- Students: Manage their own schedule
- Admins: Full CRUD for all students

### FR-8: Intelligent Course Recommendations
**Requirement:** Provide smart course recommendations based on prerequisites and importance

**Non-Functional Requirements (NFR):**
- Response time < 2 seconds for 200+ courses
- Accuracy: Prevent recommending courses with unmet prerequisites
- Circular dependency detection

**Algorithm Design:**

**Stage 1: Graph Building**
```
For each course:
1. Retrieve all prerequisites and co-requisites
2. Build dependency graph
3. Validate for circular dependencies
```

**Stage 2: Score Calculation**
```
For each course:
1. Count direct dependents: Course X → Course Y
2. Count indirect dependents: Course X → Course Y → Course Z
3. Importance Score = direct_dependents + indirect_dependents

Example:
- CS101 (Intro) → CS201 (OOP), CS202 (Data Structures) [score = 2]
- CS201 (OOP) → CS301 (Design Patterns) [score = 1]
- CS202 (Data Structures) → CS301 (Design Patterns) [score = 1]
- CS301 inherits dependency from CS101 (indirect) [+1 to CS101]
```

**Stage 3: Filtering**
```
For each course:
1. Check if student passed all non-co-requisite prerequisites
2. Check if student hasn't already selected it
3. Include only available courses
```

**Stage 4: Ordering**
```
Sort by: (-importance_score, -chart_importance)
Return top N results
```

**API Endpoint:**
```
POST /api/courses/recommendations/recommend/
{
    "degree_chart_id": 1,
    "semester": "Spring 1403",
    "limit": 10
}

Response:
{
    "success": true,
    "semester": "Spring 1403",
    "degree_chart": {...},
    "total_recommendations": 5,
    "recommendations": [
        {
            "id": 1,
            "code": "CS101",
            "name": "مقدمه برنامه‌نویسی",
            "credits": 3,
            "unit_type": "theoretical",
            "instructor": "دکتر احمدی",
            "importance_score": 5,
            "description": "...",
            "start_time": "08:00:00",
            "end_time": "09:30:00"
        }
    ]
}
```

### UC-02: View Weekly Schedule
**Requirement:** Students can view and manage their weekly schedule

**User Flow:**
1. Student navigates to Schedule tab
2. System displays week view (Saturday-Thursday)
3. Student selects course from recommendations
4. System automatically detects time conflicts
5. If conflict exists, highlight in red and show warning
6. Student can confirm or reject selection

**Schedule Conflict Logic:**
```python
has_conflict = (
    Another course on same day AND
    Time overlap: not (course.end_time <= other.start_time OR 
                       course.start_time >= other.end_time)
)
```

## Implementation Approach

### Phase 1: Student ViewSets (3 hours)
1. Create `StudentCourseHistoryViewSet` with filtering and statistics
2. Create `StudentSelectionViewSet` with confirmation flow
3. Create `ScheduleViewSet` with conflict detection
4. Implement permission classes for access control
5. Add custom actions for statistics and conflicts
6. Create serializers for each model
7. Update URL routing

### Phase 2: Recommendation Engine (4 hours)
1. Create `RecommendationEngine` class with:
   - Dependency graph builder
   - Importance score calculator
   - Prerequisite validator
   - Circular dependency detector
2. Optimize for < 2 second response time with:
   - Query optimization using select_related/prefetch_related
   - Caching for frequently accessed data
   - Efficient graph traversal algorithms
3. Create `RecommendationViewSet` with POST endpoint
4. Add comprehensive error handling
5. Add API documentation

### Phase 3: Testing & Documentation (1 hour)
1. Write unit tests for recommendation algorithm
2. Test edge cases (circular deps, no prerequisites, etc.)
3. Performance test with large datasets
4. Write API documentation with examples
5. Create OpenAPI/Swagger specifications

## Data Model Changes

**New Models:** None (all exist)

**Model Relationships:**
```
StudentCourseHistory
├── student → User (ForeignKey)
└── course → Course (ForeignKey)

StudentSelection
├── student → User (ForeignKey)
└── course → Course (ForeignKey)

Schedule
├── student → User (ForeignKey)
└── course → Course (ForeignKey)
```

## Database Changes

No schema changes required. All models exist and have migrations.

## API Endpoints Summary

| Method | Endpoint | Permission | Purpose |
|--------|----------|-----------|---------|
| GET | `/api/students/history/` | Student (own) / Admin | List course history |
| POST | `/api/students/history/` | Admin | Add to history |
| GET | `/api/students/history/passed_courses/` | Student (own) | Get passed courses |
| GET | `/api/students/history/statistics/` | Student (own) | Get GPA stats |
| GET | `/api/students/selections/` | Student (own) / Admin | List selections |
| POST | `/api/students/selections/` | Student (own) | Select course |
| DELETE | `/api/students/selections/{id}/` | Student (own) / Admin | Remove selection |
| POST | `/api/students/selections/confirm/` | Student (own) | Confirm all for semester |
| GET | `/api/students/schedule/` | Student (own) / Admin | View schedule |
| POST | `/api/students/schedule/` | Student (own) | Add to schedule |
| GET | `/api/students/schedule/conflicts/` | Student (own) | Get conflicts |
| DELETE | `/api/students/schedule/{id}/` | Student (own) / Admin | Remove from schedule |
| POST | `/api/courses/recommendations/recommend/` | Student | Get recommendations |

## Risk Mitigation

**Risk 1: Performance (Recommendation < 2 sec)**
- Mitigation: Use efficient graph algorithms, caching, query optimization
- Validation: Load test with 200+ courses

**Risk 2: Circular Dependencies**
- Mitigation: Implement cycle detection before recommendations
- Validation: Test with intentional circular dependencies

**Risk 3: Permission Leaks**
- Mitigation: Use granular permission classes, test all endpoints
- Validation: Manual permission testing for all roles

**Risk 4: Data Integrity**
- Mitigation: Use transactions for bulk operations
- Validation: Test concurrent selections/confirmations

## Success Criteria

✅ All 12 API endpoints working and tested  
✅ Permission checks working for all roles  
✅ Recommendation algorithm accurate and < 2 seconds  
✅ Schedule conflict detection working  
✅ Student statistics calculating correctly  
✅ API documentation complete  
✅ Swagger/OpenAPI specs generated  

## Files Created/Modified

**Created:**
- `backend/students/views.py` - StudentCourseHistoryViewSet, StudentSelectionViewSet, ScheduleViewSet
- `backend/courses/recommendations.py` - RecommendationEngine class

**Modified:**
- `backend/students/urls.py` - Add router configuration
- `backend/courses/views.py` - Add RecommendationViewSet
- `backend/courses/urls.py` - Register recommendations router

## Testing Plan

### Unit Tests
```python
test_recommendation_engine.py:
- test_calculate_importance_score()
- test_prerequisite_validation()
- test_circular_dependency_detection()
- test_schedule_conflict_detection()
- test_corequisite_handling()

test_student_views.py:
- test_student_can_view_own_history()
- test_admin_can_view_all_history()
- test_student_cannot_view_others_history()
- test_select_course_with_unmet_prerequisites()
- test_confirm_selections_batch()
- test_schedule_conflict_detection()
```

### Integration Tests
```python
test_student_api.py:
- test_student_full_workflow() # register → select → schedule → recommend
- test_permission_enforcement()
- test_bulk_operations()
```

### Performance Tests
```python
test_performance.py:
- test_recommendation_response_time() # < 2 seconds
- test_large_dataset_performance() # 200+ courses
```

## Rollback Plan

1. Revert ViewSet files to previous versions
2. Remove RecommendationViewSet from URL configuration
3. Run `python manage.py migrate` if any schema changes needed
4. Restart server

## Notes

- Recommendation engine uses in-memory graph traversal for performance
- Could add Redis caching in production for even faster results
- Schedule conflicts are checked in-memory to avoid N+1 queries
- All timestamps use UTC internally, converted to user timezone on response
