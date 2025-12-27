# Change Proposal: Authentication & User Management System

**Change ID:** `auth-system-setup`  
**Status:** Ready for Implementation  
**Date:** 2025-12-27  
**Priority:** P0 (Critical)

## Overview

Implement comprehensive authentication system with role-based access control (RBAC) for Unipath. This provides the foundation for user management, permissions, and profile management required by FR-1, FR-2, and FR-3.

## Problem Statement

The application requires different user roles (Student, Admin, Professor, HOD) with distinct permissions and workflows. A robust authentication and authorization system is essential before implementing any other features.

## Scope

### In Scope
- Custom User model with role support
- User registration & login
- JWT token-based authentication
- Role-Based Access Control (RBAC)
- User profile management
- Password reset flow
- Token refresh mechanism

### Out of Scope
- OAuth/Social login (Phase 2)
- Two-factor authentication (Phase 2)
- Email verification (Phase 1)
- External SSO integration

## Requirements

### ADDED Requirements

#### Requirement: User Model with Roles
```
The system must support a custom User model that extends Django's
AbstractUser with role-based distinction (Student, Admin, Professor, HOD).
```

**Scenario 1:** Admin creates a new user with role "Student"
- User is created with role designation
- User can only access Student-level endpoints
- User record is linked to a Profile

**Scenario 2:** User views their own profile
- User sees role, major, student number, contact info
- User can edit non-protected fields
- Changes are validated and saved

#### Requirement: JWT Authentication
```
The system must use JWT tokens for stateless authentication
across all API endpoints.
```

**Scenario 1:** User logs in with credentials
- Valid credentials return JWT access & refresh tokens
- Tokens are short-lived (15 minutes access, 7 days refresh)
- Tokens contain role information

**Scenario 2:** User accesses protected endpoint with token
- Token is validated and not expired
- User identity is verified
- Request is processed with user context

#### Requirement: Role-Based Access Control
```
The system must enforce permissions based on user roles
for all operations.
```

**Scenario 1:** Student tries to create a course
- Request is rejected with 403 Forbidden
- Student role lacks "add_course" permission
- Error message indicates insufficient permissions

**Scenario 2:** Admin accesses course management
- Admin role has "add_course", "change_course", "delete_course" permissions
- Admin can perform CRUD operations
- All changes are logged with admin identity

#### Requirement: Profile Management
```
Users must be able to view and edit their profile information
while maintaining data integrity.
```

**Scenario 1:** Student updates profile
- Can change: Name, student number, phone, email
- Cannot change: Student ID, enrollment year (protected)
- Changes require validation (email format, unique constraints)

## Data Model

### User Model
```python
class User(AbstractUser):
    ROLES = [
        ('student', 'Student'),
        ('professor', 'Professor'),
        ('admin', 'Admin'),
        ('hod', 'Head of Department'),
    ]
    role = CharField(max_length=20, choices=ROLES)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

### Profile Model
```python
class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    student_number = CharField(max_length=20, unique=True, null=True)
    phone = CharField(max_length=20, null=True)
    major = ForeignKey(DegreeChart, on_delete=SET_NULL, null=True)
    bio = TextField(blank=True)
    avatar = ImageField(upload_to='avatars/', null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

## API Endpoints

```
Authentication:
  POST /api/auth/register
    Request: {email, password, first_name, last_name, role, student_number?}
    Response: {user_id, email, role, token, refresh_token}
    
  POST /api/auth/login
    Request: {email, password}
    Response: {access_token, refresh_token, user: {id, email, role}}
    
  POST /api/auth/refresh
    Request: {refresh_token}
    Response: {access_token}
    
  POST /api/auth/logout
    Request: {refresh_token}
    Response: {detail: "Successfully logged out"}

Profile:
  GET /api/user/profile/
    Response: {user_id, email, role, student_number, phone, major, bio, avatar}
    
  PUT /api/user/profile/
    Request: {first_name?, last_name?, phone?, bio?, avatar?}
    Response: Updated profile
    
  POST /api/user/change-password/
    Request: {old_password, new_password}
    Response: {detail: "Password changed successfully"}
```

## Implementation Checklist

### Backend (Django)
- [ ] Create custom User model
- [ ] Create Profile model
- [ ] Configure JWT authentication
- [ ] Create serializers (UserSerializer, ProfileSerializer)
- [ ] Create authentication views (register, login, refresh)
- [ ] Create profile views (get, update)
- [ ] Set up RBAC permissions
- [ ] Create signals for Profile creation
- [ ] Add authentication tests

### Frontend (Flutter)
- [ ] Create authentication service
- [ ] Create login screen
- [ ] Create registration screen
- [ ] Implement token storage
- [ ] Create profile management screen
- [ ] Add authentication guards/middleware
- [ ] Implement auto-login on app start
- [ ] Create logout functionality

## Dependencies

- djangorestframework
- djangorestframework-simplejwt
- django-cors-headers
- python-decouple (for env variables)

## Acceptance Criteria

1. User can register with email, password, and role selection
2. User can login with credentials and receive JWT tokens
3. Protected endpoints reject requests without valid tokens
4. Admin can access admin-only endpoints
5. Student cannot access admin endpoints (403 Forbidden)
6. User can view and update their profile
7. Password change works correctly
8. Tokens refresh without requiring re-login
9. User roles are properly enforced in permissions
10. All sensitive data (passwords) are hashed

## Testing Strategy

- Unit tests for User/Profile models
- Integration tests for authentication endpoints
- Permission tests for RBAC
- Token expiration tests
- Edge cases: invalid credentials, expired tokens, missing fields

## Security Considerations

- Passwords hashed with Argon2 or PBKDF2
- JWT tokens signed with SECRET_KEY
- CORS configured for trusted origins only
- Rate limiting on login/register endpoints
- Secure token storage on client (HTTPOnly cookies preferred over localStorage)
- Input validation on all endpoints
- SQL injection prevention via ORM

## Performance

- Profile queries optimized with select_related
- Token validation cached for 5 minutes
- No N+1 queries in list endpoints

## Future Enhancements

- OAuth2 integration
- Social login (Google, GitHub)
- Two-factor authentication
- Email verification
- Password reset via email
- Account recovery

---

**Estimated Effort:** 20-25 hours  
**Team:** Full stack (Backend + Frontend)  
**Timeline:** 2-3 days
