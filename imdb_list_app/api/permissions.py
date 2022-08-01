
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        
        return request.method in permissions.SAFE_METHODS or request.user.is_staff

class ReviewUserOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff or obj.review_user == request.user