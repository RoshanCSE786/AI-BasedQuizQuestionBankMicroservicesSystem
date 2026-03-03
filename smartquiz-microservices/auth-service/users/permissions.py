from rest_framework.permissions import BasePermission

class IsAdminUserRole(BasePermission):
    """
    Custom permission:
    Allows access only to users with role = 'admin'
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'