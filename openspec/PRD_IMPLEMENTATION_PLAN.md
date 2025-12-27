# PRD Implementation Plan - Unipath

**Date:** December 27, 2025  
**Status:** Starting Implementation  
**Estimated Duration:** 2-3 days for MVP

## Current Backend Status

✅ **Already Complete:**
- Custom User model with roles (Student, Professor, Admin, HOD)
- JWT authentication system (7 endpoints)
- Course models (DegreeChart, Course, ChartCourse, Prerequisite, CoRequisite)
- Student models (StudentCourseHistory, StudentSelection, Schedule)
- Student API ViewSets with 11 endpoints
- Recommendation Engine with importance scoring
- Permission classes and access control
- Database migrations and Swagger documentation

## What's Missing (To Complete PRD)

### Phase 1: Backend Enhancements (3-4 hours)
1. **FR-7: Toggle Passed Status** - Endpoint to mark courses as passed
2. **FR-11: Professor Grade Input** - Grades endpoint with professor-only access
3. **FR-12: HOD Prerequisite Management** - HOD-specific modification endpoints
4. **Data Validation** - Circular dependency prevention on course creation
5. **Acceptance Criteria Validation** - API tests for all 6 criteria

### Phase 2: Flutter Frontend (2-3 days)
1. Authentication screens (Login, Register)
2. Curriculum Chart visualization
3. Passed courses management
4. Recommendation display
5. Schedule visualization (weekly grid)
6. Profile management
7. Grade input (Professor view)
8. RTL support and Dark Mode

### Phase 3: Testing & Optimization (1-2 days)
1. Load testing (< 2 seconds for 200 courses)
2. Integration testing
3. Security audit
4. Performance optimization

## PRD Acceptance Criteria Mapping

| Criteria | Current Status | Action Required |
|----------|---|---|
| 1. Login & see Major chart | ✅ Backend ready | Frontend needed |
| 2. Mark course passed → unlocks others | ⚠️ Partial | Complete FR-7 endpoint |
| 3. Importance scoring | ✅ Complete | Test & verify |
| 4. Schedule rendering | ✅ API ready | Frontend screens |
| 5. Admin can add courses | ✅ Complete | Frontend form |
| 6. Block course without prerequisite | ✅ Complete | Verify logic |

## Implementation Order

### Today (Dec 27)
1. ✅ Complete Student API system
2. **Complete FR-7: Toggle Passed Courses** (30 min)
3. **Add FR-11: Professor Grade Input** (30 min)
4. **Add FR-12: HOD Prerequisite Edit** (30 min)
5. **Add Circular Dependency Detection** (30 min)
6. **Write acceptance criteria tests** (1 hour)
7. Create comprehensive API documentation

### Tomorrow (Dec 28)
1. Start Flutter screens (Authentication)
2. API integration with backend
3. Chart visualization
4. Passed courses management

### Day 3 (Dec 29)
1. Schedule visualization
2. Recommendation display
3. Final testing & bug fixes
4. Dark Mode & RTL support

## Backend Tasks - Detailed

### Task 1: FR-7 Toggle Passed Courses (30 min)
```
POST /api/students/history/mark-passed/
{
    "course_id": 1,
    "semester": "Fall 1402",
    "grade": "A",
    "grade_points": 4.0
}

Response: Creates StudentCourseHistory with is_passed=True
```

### Task 2: FR-11 Professor Grade Input (30 min)
```
POST /api/grades/submit/
{
    "student_id": 1,
    "course_id": 1,
    "grade": "B+",
    "semester": "Fall 1402"
}

Permission: Professor only
Only for courses taught by professor
```

### Task 3: FR-12 HOD Prerequisite Management (30 min)
```
PUT /api/courses/{id}/prerequisites/
{
    "prerequisites": [2, 3],
    "corequisites": [4]
}

Permission: HOD only for their department
Updates prerequisite relationships
```

### Task 4: Circular Dependency Detection (30 min)
```
- Prevent creating cyclic prerequisites
- Validate on course creation/modification
- Return meaningful error messages
- Already implemented in RecommendationEngine, need to use in API
```

### Task 5: Acceptance Criteria Tests (1 hour)
```
- Test 1: Student login → see chart
- Test 2: Mark course passed → recommendations updated
- Test 3: Importance score verified
- Test 4: Schedule rendering works
- Test 5: Admin add course
- Test 6: Prerequisite blocking works
```

## Files to Create/Modify

### New Endpoints

**Student Passed Courses:**
- POST /api/students/mark-passed/ → Create StudentCourseHistory
- PUT /api/students/history/{id}/ → Update grade (already exists)

**Professor Grading:**
- POST /api/grades/submit/ → New ViewSet
- GET /api/grades/my-courses/ → Professor's courses

**HOD Management:**
- PUT /api/courses/{id}/prerequisites/ → Modify prerequisites
- DELETE /api/courses/{id}/prerequisites/{prereq_id}/ → Remove prerequisite

### Modified Files

**backend/students/views.py**
- Add mark_passed custom action
- Add mark_failed custom action

**backend/accounts/views.py**
- Add GradeViewSet (Professor only)

**backend/courses/views.py**
- Add prerequisite modification endpoint
- Add circular dependency check

**backend/courses/models.py**
- Add validation in save() method

## Testing Strategy

### Acceptance Criteria Tests

```python
test_student_login_sees_chart()
test_mark_course_passed_unlocks_dependents()
test_importance_score_ranking()
test_schedule_rendering()
test_admin_add_course()
test_prerequisite_blocking()
```

### API Endpoint Tests

```python
test_mark_passed_creates_history()
test_professor_grade_submission()
test_hod_prerequisite_modification()
test_circular_dependency_rejection()
test_prerequisite_validation()
```

### Performance Tests

```python
test_recommendation_response_time()  # < 2 seconds for 200 courses
test_schedule_conflict_detection()  # < 100ms
test_circular_dependency_detection()  # < 500ms
```

## Success Metrics

✅ All 6 acceptance criteria passing  
✅ All 12+ API endpoints tested  
✅ Recommendation engine < 2 seconds  
✅ Zero critical security issues  
✅ 100% permission enforcement  
✅ Circular dependency prevention working  

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Circular dependencies | DFS detection + validation on save |
| Data integrity | Transactions on grade/prerequisite updates |
| Permission bypass | Test all endpoints with different roles |
| Performance | Cache recommendations, optimize queries |
| Data entry load | Accept CSV import (not in MVP) |

## Next Steps

1. Implement FR-7, FR-11, FR-12 backend endpoints
2. Write acceptance criteria tests
3. Verify all 6 acceptance criteria
4. Start Flutter frontend
5. Complete end-to-end testing
