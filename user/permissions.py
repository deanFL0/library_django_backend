from rest_framework import permissions

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.role == "user" or request.user.role == 'admin'
        return False
    
    def has_object_permission(self, request, view, obj):
            return request.user.role == "user" or request.user.role == 'admin'
    
class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.role == "librarian" or request.user.role == 'admin'
        return False
    
    def has_object_permission(self, request, view, obj):
        return request.user.role == "librarian" or request.user.role == 'admin'
    
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.role == "admin"
        return False
    def has_object_permission(self, request, view, obj):
        return request.user.role == "admin"
    
class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "user", obj) == request.user
    
class IsOwnerOrLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == "user" or request.user.role == "librarian" or request.user.role == 'admin'
        )

    def has_object_permission(self, request, view, obj):
        if request.user.role == "librarian" or request.user.role == 'admin':
            return True
        return getattr(obj, "user", obj) == request.user 
    
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        return getattr(obj, "user", obj) == request.user