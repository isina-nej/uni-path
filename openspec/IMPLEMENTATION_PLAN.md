# Unipath Implementation Master Plan

**Status:** In Progress  
**Last Updated:** December 27, 2025

## Overview

This document defines the structured approach to implementing Unipath based on the PRD. We follow OpenSpec methodology for all changes and features.

## Implementation Strategy

### Phase 1: Foundation (Current)
- [x] Project structure initialized
- [ ] Database models & schema design
- [ ] API authentication & user management
- [ ] RBAC (Role-Based Access Control)

### Phase 2: Core Features
- [ ] Curriculum & Course management
- [ ] Student course history & progress
- [ ] Schedule management
- [ ] Recommendation engine

### Phase 3: UI/UX Implementation
- [ ] Flutter screens & components
- [ ] API integration
- [ ] Offline capability
- [ ] Dark mode & RTL support

### Phase 4: Testing & Optimization
- [ ] Unit & integration tests
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Deployment preparation

## Key Features from PRD

### Core Capabilities

1. **Authentication & Authorization** (FR-1, FR-2, FR-3)
   - User registration/login
   - RBAC implementation
   - Profile management

2. **Curriculum Management** (FR-4, FR-5, FR-6)
   - Course CRUD operations
   - Prerequisite/co-requisite relationships
   - Chart management by admins

3. **Student Course Selection** (FR-7, FR-8, FR-9)
   - Mark passed courses
   - Automatic filtering based on prerequisites
   - Calculate importance scores

4. **Recommendation Engine** (FR-8, FR-9)
   - Importance score calculation
   - Course ranking algorithm
   - Dependency analysis

5. **Schedule Management** (UC-02)
   - Weekly schedule visualization
   - Conflict detection
   - Schedule optimization

## OpenSpec Change Proposals Required

1. **auth-system** - Authentication & RBAC
2. **course-management** - Curriculum & course operations
3. **recommendation-engine** - Smart recommendation algorithm
4. **schedule-management** - Weekly schedule features
5. **student-progress** - Course history & tracking

## Database Schema Overview

```
Core Models:
├── User (Custom with roles)
├── Profile (Student/Admin/Professor/HOD)
├── Course
├── CoursePrerequisite
├── CoRequisite
├── DegreeChart
├── ChartCourse
├── StudentSelection
├── StudentCourseHistory
├── Notification
└── Schedule
```

## API Endpoints Structure

```
Authentication:
  POST   /api/auth/register
  POST   /api/auth/login
  POST   /api/auth/refresh

Courses:
  GET    /api/courses/
  GET    /api/courses/{id}/
  POST   /api/courses/ (admin)
  PUT    /api/courses/{id}/ (admin)
  DELETE /api/courses/{id}/ (admin)

Student:
  GET    /api/student/progress/
  POST   /api/student/progress/
  GET    /api/student/recommendations/
  GET    /api/student/schedule/
  POST   /api/student/schedule/

Chart:
  GET    /api/chart/{major_id}/
  GET    /api/chart/{major_id}/courses/

Notifications:
  GET    /api/notifications/
  PUT    /api/notifications/{id}/mark-read/
```

## Technology Stack Confirmed

- **Frontend:** Flutter 3.x, Dart
- **Backend:** Django 4.2, Python 3.10+
- **Database:** PostgreSQL (production) / SQLite (development)
- **Authentication:** JWT tokens
- **API:** Django REST Framework
- **Features:** CORS, Multilingual (Persian RTL), Dark Mode

## Risk Mitigation

- **Circular Dependencies:** Validate on course creation
- **Performance:** Cache recommendation results
- **Data Integrity:** Comprehensive validation & constraints
- **Security:** Role-based permissions, input validation

## Success Criteria

1. Students can register and login
2. Students can view their major's curriculum
3. Smart recommendations show correct course importance
4. Weekly schedule shows no conflicts
5. All CRUD operations work correctly
6. System handles 200+ courses efficiently

---

**Next Step:** Create OpenSpec change proposals for Phase 1 features
