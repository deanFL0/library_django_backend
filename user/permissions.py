from rest_framework import permissions

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.role == "user"
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            return obj.user == request.user
        return False
    
class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.role == "librarian"
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            return request.user.role == "librarian"
        return False
    
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.role == "admin"
        return False
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            return request.user.role == "admin"
        return False
    
class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.role == "user"
        return
    
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            return obj.user == request.user
        return False
    
class IsOwnerOrLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == "user" or request.user.role == "librarian"
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.role == "librarian" or obj.user == request.user
        )
    
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.role == "user" or request.user.role == "admin"
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            return obj.user == request.user or request.user.role == "admin"
        return False