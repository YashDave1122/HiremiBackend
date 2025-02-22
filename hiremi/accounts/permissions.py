from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return True
        # return obj == request.user  # obj is the user instance


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return True
        # return obj.user == request.user  # obj is owned the user instance

class IsSelfOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return True
        # return bool(request.method in SAFE_METHODS or obj == request.user )

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return True
        # return bool(request.method in SAFE_METHODS or obj.user == request.user )

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    
class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff