from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in ("GET", "HEAD", "OPTIONS") or
            request.user and request.user.is_staff
        )

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user