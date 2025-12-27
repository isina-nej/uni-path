from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    """
    Permission to check if user is a student.
    """
    message = 'فقط دانشجویان می‌تواند این عملیات را انجام دهند'
    
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and 
                request.user.role == 'student')


class IsProfessor(BasePermission):
    """
    Permission to check if user is a professor.
    """
    message = 'فقط اساتید می‌تواند این عملیات را انجام دهند'
    
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and 
                request.user.role == 'professor')


class IsAdmin(BasePermission):
    """
    Permission to check if user is an admin.
    """
    message = 'فقط مدیران می‌تواند این عملیات را انجام دهند'
    
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and 
                request.user.role == 'admin')


class IsHOD(BasePermission):
    """
    Permission to check if user is Head of Department.
    """
    message = 'فقط مدیران گروه می‌تواند این عملیات را انجام دهند'
    
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and 
                request.user.role == 'hod')


class IsAdminOrReadOnly(BasePermission):
    """
    Permission to allow admin full access, others read-only.
    """
    
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        return (request.user and 
                request.user.is_authenticated and 
                request.user.role == 'admin')


class IsAdminOrHOD(BasePermission):
    """
    Permission for admin or HOD access.
    """
    message = 'فقط مدیران و مدیران گروه می‌تواند این عملیات را انجام دهند'
    
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and 
                request.user.role in ['admin', 'hod'])


class IsOwnerOrAdmin(BasePermission):
    """
    Permission to allow users to edit their own profile or admin to edit any.
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user and request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        # Users can edit their own profile
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return obj == request.user
