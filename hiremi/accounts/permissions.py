from rest_framework.permissions import BasePermission


class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user  # obj is the user instance


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user  # obj is owned the user instance
