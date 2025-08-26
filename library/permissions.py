from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admin users have full access.
    Normal users only have read-only access.
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS for everyone authenticated
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only admins can create/update/delete
        return request.user and request.user.is_staff


class IsAdmin(permissions.BasePermission):
    """
    Only admin users can access.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Users can view/update their own record.
    Admins can access all.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff
